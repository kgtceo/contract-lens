"""Run the contract-lens eval suite.

Gates:
  • RECALL     — on a loaded contract, it surfaces a solid share of the planted risky clauses.
  • PRECISION  — on a fair, balanced contract, it raises no 'high' findings (doesn't cry wolf).
  • GROUNDING  — every quote appears in the document (no fabricated clauses).
  • JUDGE      — opus scores correctness / usefulness / calibration.

    python evals/run_evals.py [--no-judge]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from anthropic import Anthropic

from contract_lens.client import LLMClient
from contract_lens.config import Settings
from contract_lens.reviewer import Reviewer

from metrics import catches_enough, findings_are_grounded, high_count, material_count  # noqa: E402

DATASET = Path(__file__).parent / "dataset" / "cases.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-judge", action="store_true")
    args = ap.parse_args()

    settings = Settings.from_env()
    anthropic = Anthropic(api_key=settings.anthropic_api_key)
    client = LLMClient(settings, anthropic)
    reviewer = Reviewer(client)
    cases = json.loads(DATASET.read_text())

    failures: list[str] = []
    grades = []
    for case in cases:
        result = reviewer.review(case["contract"])
        grounded = findings_are_grounded(result, case["contract"])
        print(f"\n=== {case['name']} ===")
        print(f"  material={material_count(result)} high={high_count(result)} grounded={grounded}")

        if not grounded:
            failures.append(f"{case['name']}: a quote isn't in the contract")
        if case["expect_findings"]:
            if not catches_enough(result, case["planted"]):
                failures.append(f"{case['name']}: caught too few of the planted risky clauses")
        else:
            if high_count(result) > 0:
                failures.append(f"{case['name']}: raised 'high' findings on a fair contract (precision)")

        if not args.no_judge:
            from judge import grade  # noqa: E402

            g = grade(result, case["contract"], settings, client)
            grades.append(g)
            print(f"  JUDGE: correctness={g.correctness} usefulness={g.usefulness} calibration={g.calibration} overall={g.overall}")
            if not g.calibration or g.calibration < 3:
                failures.append(f"{case['name']}: judge flagged poor calibration / overstepping")

    if grades:
        n = len(grades)
        print(f"\n=== Judge avg === overall={sum(g.overall for g in grades)/n:.2f}")

    print("\n" + "=" * 40)
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(f"  ✗ {f}")
        return 1
    print("ALL GATES PASSED ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
