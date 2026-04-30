# TerraLogic — OKR Progress Evaluation & Refinement

## 1. Original OKRs

The following objectives and key results were set at the beginning of the quarter for Preetam Donepudi's individual contribution to TerraLogic, an agentic AI pipeline built for the Overture Maps Foundation.

### Individual Objective

> **Build a reliable, evidence-first agentic pipeline that ingests Overture Places data, validates it against live web sources, and scores every entry with a calibrated confidence value. Own the core brain of TerraLogic — the system that makes or breaks the project.**

---

### Objective 1 — High-Confidence Detection

| KR | Description | Score |
|---|---|---|
| KR1 | Achieve ≥90% precision in identifying stale/incorrect places, validated against manually sampled ground truth by Week 8. | 0.4 — Partial |
| KR2 | Maintain ≥85% recall for the three major error types: closed, moved, and renamed. | 0.4 — Partial |
| KR3 | Deliver calibrated confidence scores (0–1) where high-confidence predictions (≥0.8) are correct ≥95% of the time. | 0.7 — On track |
| KR4 | Reduce false positives to <10% of all agent outputs by final demo. | 0.4 — Partial |

### Objective 2 — Trustworthy Agentic Pipeline

| KR | Description | Score |
|---|---|---|
| KR1 | Ensure 100% of flagged outputs include verifiable source citations — no claim without supporting evidence. | 0.9 — On track |
| KR2 | Reduce hallucinated or unsupported agent conclusions to <5% across all outputs. | 0.7 — On track |
| KR3 | Implement a multi-step reasoning pipeline: retrieve → verify → score → propose correction by Week 6. | 1.0 — Complete |
| KR4 | Add a self-verification step where the agent re-checks its conclusions before final output. | 0.5 — Partial |

### Objective 3 — Structural Reliability

| KR | Description | Score |
|---|---|---|
| KR1 | Enforce evidence-first outputs — no claim produced without a supporting source citation. | 0.9 — On track |
| KR2 | Externalize all critical logic (scoring rules, validation thresholds) outside the LLM layer. | 1.0 — Complete |
| KR3 | Implement structured JSON output formats for all agent decisions — no free-form reasoning only. | 1.0 — Complete |
| KR4 | Achieve ≥95% consistency in repeated runs on the same input (low output randomness). | 0.5 — Partial |

---

## 2. Progress Evaluation

The following is an honest assessment of progress against each key result, including measurable outcomes and any setbacks encountered.

### Overall Pipeline Progress

| Component | Score | Status |
|---|---|---|
| Data Ingestion | 1.0 / 1.0 | Complete |
| AI Validation Agent | 0.8 / 1.0 | On track |
| Confidence Scorer | 0.9 / 1.0 | On track |
| GeoJSON Exporter | 1.0 / 1.0 | Complete |
| Precision / Recall Benchmarking | 0.3 / 1.0 | Blocked |
| API Credits / Live Data | 0.2 / 1.0 | Blocked |

### What Has Been Achieved

- Successfully ingested **53,732 real San Francisco Places records** from Overture Maps using the Python CLI — exceeding the 500-place target for initial validation.
- Built a full **two-step Claude API agent**: Step 1 uses the `web_search` tool to research each place in real time; Step 2 extracts a structured JSON verdict with status, confidence score, issues, and citations.
- Implemented the **multi-step reasoning pipeline** (retrieve → verify → score → propose correction) ahead of schedule — KR2.3 complete.
- Built a **confidence scorer** with a dual penalty system: citation penalty for unsupported claims and consistency penalty for status/confidence contradictions. Running on 100 mock places produced 22 high-priority, 18 medium-priority, and 60 low-priority results.
- Exported **22 Overture-compatible GeoJSON corrections** (19 closed, 3 moved) with confidence ≥0.7 — KR5 of the team OKR complete.
- Enforced **structured JSON output formats** for all agent decisions — no free-form reasoning. KR3.3 complete.
- All critical scoring and validation logic **externalized outside the LLM layer** in `scorer.py` — KR3.2 complete.
- Established a clean **GitHub repository** with branch-based workflow, `.gitignore`, and weekly commit cadence.

### What Is Behind Schedule

- **Precision and recall cannot be formally measured yet** — the Anthropic API credits required to run the real agent on live data are still pending. This blocks KR1.1, KR1.2, and KR1.4 from being validated.
- The **self-verification step** (KR2.4) where the agent re-checks its own conclusions before output is designed but not yet implemented — waiting on live API access.
- **Output consistency** (KR3.4 — ≥95% across repeated runs) cannot be measured until the real agent is running on live data.
- **Project alignment** was clarified mid-quarter — TerraLogic is now confirmed as Project C (Places validation) which required some repositioning of the approach and communication.

---

## 3. Challenges & Insights

### Challenge 1 — API Credits Blocker

The single biggest challenge has been access to the Anthropic Claude API, which requires a paid account. Without live API access, precision and recall — two of the most critical KRs — cannot be formally measured. The workaround has been building a mock agent that generates realistic but synthetic validation results, which has kept development unblocked but means the accuracy metrics remain theoretical rather than empirical.

**Actions taken:** Submitted a research credits application to Anthropic's console program with a detailed project description. Application is currently pending.

### Challenge 2 — Project Alignment Confusion

There was initial confusion about whether TerraLogic mapped to Project B (LLM-readable metrics artifact) or Project C (Places validation). This was clarified during the project briefing session — TerraLogic is Project C. While this did not change the technical work already done, it required repositioning the narrative and understanding how the pipeline fits within the broader Terraforma ecosystem.

**Key learning:** Project scope clarity should be confirmed at the very start of the quarter, not discovered mid-way. A brief project brief alignment session in Week 1 would have prevented this.

### Challenge 3 — Interface Contract Not Formalized

The interface contract between the pipeline and any downstream consumers — defining exactly what JSON structure the agent outputs — has not been formally documented yet. This is a key structural gap that needs to be addressed before integration can begin.

**Key learning:** In multi-person pipelines, the interface contract needs to be the first thing agreed on — before any code is written — not something that emerges organically.

### Key Insights

- **Anti-hallucination is an architectural problem, not just a prompting problem.** Building the penalty system into `scorer.py` — outside the LLM — was the right call. It means the system cannot be manipulated by a poorly-worded prompt.
- **Mock data is underrated.** Building `mock_agent.py` early kept development unblocked. Without it, there would have been nothing to test the pipeline against while waiting for API credits.
- **53,000 places is a lot — but 100 is enough to prove the system works.** Scoping the demo to a small sample was the right strategic decision for a course project.
- **Commit history matters.** Maintaining ≥3 commits per week as a discipline creates a natural audit trail of progress that is invaluable for course evaluation.

---

## 4. Refined OKRs

Based on the evaluation above, the following refinements are proposed. The overall objective remains unchanged — the adjustments reflect realistic timelines given the API credits blocker and lessons learned about scope.

### Objective — Unchanged

> **Build a reliable, evidence-first agentic pipeline that ingests Overture Places data, validates it against live web sources, and scores every entry with a calibrated confidence value.**

### Objective 1 — Detection Accuracy (Revised)

| KR | Original | Revised |
|---|---|---|
| KR1.1 | ≥90% precision by Week 8 | ≥80% precision by Week 10, contingent on API credit availability. 90% target moved to next cycle. |
| KR1.3 | High-confidence predictions (≥0.8) correct ≥95% of the time | Unchanged — penalty system in `scorer.py` already enforces this structurally. |

### Objective 2 — Pipeline Trustworthiness (Unchanged — on track)

KR2.1 (100% citations), KR2.2 (<5% hallucinations), and KR2.3 (multi-step pipeline) are all on track or complete. KR2.4 (self-verification step) is revised to: implement self-verification when API credits are confirmed, with a mock verification layer in place by Week 8 as a fallback.

### Objective 3 — Structural Reliability (Unchanged — mostly complete)

KR3.1, KR3.2, and KR3.3 are complete. KR3.4 (≥95% output consistency) is revised to: demonstrate consistency across 20 repeated mock runs by Week 9, with live consistency testing deferred until API access is confirmed.

### New KR Added — Interface Contract

> **KR NEW:** Formalize and document the pipeline output interface contract by end of Week 6, including exact JSON schema for all agent outputs.

**Justification:** This was the most significant process gap identified in the evaluation. Adding it as a formal KR ensures it gets treated as a deliverable, not an afterthought.

---

## 5. Strategic Next Steps

### Immediate (This Week)

- Formalize the pipeline output interface contract. Define the exact JSON schema that `scorer.py` outputs so any downstream system can build against a stable contract.
- Follow up on the Anthropic API credits application. If credits don't come through by Week 7, explore running the real agent on a small paid batch (10–20 places) to get at least one real precision measurement.
- Implement the self-verification step in `agent.py` using a second Claude call that re-checks the initial verdict before output.

### Weeks 6–8 — Integration & Benchmarking

- Run a full end-to-end integration test of the pipeline — from Overture data ingestion through to final `corrections.geojson` output. Identify and fix any schema mismatches early.
- Build `benchmark.py` — a script that loads the `project_c_samples.parquet` ground truth file and measures real precision and recall against known open/closed labels.
- Expand the validated sample from 100 to 500 places using mock data so the pipeline has a more realistic data volume to benchmark against.

### Weeks 9–10 — Demo Preparation

- Lock the demo city and dataset. Run the full pipeline end-to-end against a real city with live API access if credits arrive.
- Produce a final `corrections.geojson` with real agent-validated data, formatted for potential upstream contribution to Overture.
- Ensure all pipeline scripts are documented with clear README instructions so the project is reproducible by anyone after the course ends.
- Prepare the final presentation — cover the pipeline architecture section of the demo, showing the full flow from Overture ingestion to human-reviewable corrections.

### How Refined OKRs Guide the Remaining Weeks

The refined OKRs shift the focus from ambitious targets that depend on external resources (API credits) to targets that are achievable with what exists now — while maintaining the structural integrity of the pipeline. The new interface contract KR creates accountability around the highest-risk dependency. The revised precision target (80% instead of 90%) is still a meaningful, measurable outcome that demonstrates the system works, while being honest about the constraints of the current environment.

The north star remains unchanged: TerraLogic should be a trustworthy, evidence-first agentic system that produces corrections humans can act on — not just a demo. Every remaining week of work should move toward that standard.