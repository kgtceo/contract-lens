import type { ReviewResult } from "./types";

const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").replace(/\/+$/, "");

export async function getExample(): Promise<{ contract: string }> {
  const res = await fetch(`${API_URL}/api/example`);
  if (!res.ok) throw new Error(`Could not load example (${res.status})`);
  return res.json();
}

export async function review(contract: string): Promise<ReviewResult> {
  const res = await fetch(`${API_URL}/api/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ contract }),
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body?.detail) detail = body.detail;
    } catch {
      /* non-JSON */
    }
    throw new Error(detail);
  }
  return res.json();
}
