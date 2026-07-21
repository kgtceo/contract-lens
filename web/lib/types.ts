// Mirrors the backend Pydantic models (contract_lens.models).

export type Severity = "high" | "medium" | "low";

export interface Finding {
  clause_type: string;
  severity: Severity;
  concern: string;
  recommendation: string;
  quote: string;
}

export interface Review {
  summary: string;
  overall_risk: string;
  findings: Finding[];
}

export interface ReviewResult {
  review: Review;
  clause_types: string[];
  disclaimer: string;
}
