# TerraLogic — Objectives & Key Results
**Spring 2026 · Project Terrapulse · Overture Maps Foundation**

*Last updated: April 2026*

---

## Team

| Role | Owner |
|------|-------|
| Pipeline + Architecture | Preetam Donepudi |
| Backend + Data + Export | Ashmita |
| Frontend + UX + Dashboard | Devesh |

---

## North Star

> "Be the go-to open-source tool for validating and improving Overture Maps Places data quality — at global scale."
>
> Every quarterly OKR moves the needle toward this vision. TerraLogic is not just a demo — it is infrastructure for real-world map accuracy.

---

## Project Overview

| Field | Value |
|-------|-------|
| **Project** | TerraLogic — Agentic Places Validator |
| **Organization** | Overture Maps Foundation |
| **Cycle** | Q2 2026 (90 days) |
| **Team Size** | 3 people |
| **Target Dataset** | Overture Maps Places (GeoParquet) |

---

## Team OKR — Shared Q2 Goal

### Objective
👥 **Prove that a trustworthy agentic AI pipeline can meaningfully improve the accuracy of Overture Maps Places data for a real city.**

Not just a pipeline that flags places — a system that reasons over evidence, cites its sources, and produces corrections humans can trust.

### Key Results

| KR | Target |
|----|--------|
| **KR 1** | Validate at least 500 Overture Places entries in a single city, with a calibrated confidence score (0–1) assigned to every entry. |
| **KR 2** | Achieve ≥90% precision in identifying stale/incorrect places, validated against a sampled ground truth set. |
| **KR 3** | Ensure 100% of flagged outputs include verifiable source citations — zero unsupported claims. |
| **KR 4** | Ship a live dashboard where the full team can review, approve, or reject corrections in <10 seconds per place. |
| **KR 5** | Export at least one Overture-compatible GeoJSON/GeoParquet correction file ready for upstream contribution. |

### Success Metrics

- **Precision target:** ≥90% (flagged places that are actually incorrect)
- **Recall target:** ≥85% (real errors the system catches)
- **False positive ceiling:** <10% of all flagged entries
- **Human review speed:** <10 seconds per place in dashboard
- **Source citation rate:** 100% of flagged outputs
- **Confidence calibration:** ≥0.8 predictions correct ≥95% of the time

---

## Individual OKR — Pipeline & Architecture

### Owner: Preetam Donepudi
🔬 **Pipeline + Architecture + GitHub**

### Objective
Build a reliable, evidence-first agentic pipeline that ingests Overture Places data, validates it against live web sources, and scores every entry with a calibrated confidence value.

Own the core brain of TerraLogic — the system that makes or breaks the project.

### Key Results

#### High-Confidence Detection

| KR | Target |
|----|--------|
| **KR 1** | Achieve ≥90% precision in identifying stale/incorrect places, validated against manually sampled ground truth by Week 8. |
| **KR 2** | Maintain ≥85% recall for the three major error types: closed, moved, and renamed. |
| **KR 3** | Deliver calibrated confidence scores (0–1) where high-confidence predictions (≥0.8) are correct ≥95% of the time. |
| **KR 4** | Reduce false positives (incorrectly flagged valid places) to <10% of all agent outputs by final demo. |

#### Trustworthy Agentic Pipeline

| KR | Target |
|----|--------|
| **KR 1** | Ensure 100% of flagged outputs include verifiable source citations — no claim without supporting evidence. |
| **KR 2** | Reduce hallucinated or unsupported agent conclusions to <5% across all outputs. |
| **KR 3** | Implement a multi-step reasoning pipeline: retrieve → verify → score → propose correction by Week 6. |
| **KR 4** | Add a self-verification step where the agent re-checks its conclusions before final output. |

#### Structural Reliability (Anti-Hallucination)

| KR | Target |
|----|--------|
| **KR 1** | Enforce evidence-first outputs — no claim produced without a supporting source citation. |
| **KR 2** | Externalize all critical logic (scoring rules, validation thresholds) outside the LLM layer. |
| **KR 3** | Implement structured JSON output formats for all agent decisions — no free-form reasoning only. |
| **KR 4** | Achieve ≥95% consistency in repeated runs on the same input (low output randomness). |

### Key Metrics

| Metric | Target |
|--------|--------|
| Precision | ≥90% |
| Recall | ≥85% across closed / moved / renamed |
| False positive rate | <10% |
| Hallucination rate | <5% of agent outputs |
| Output consistency | ≥95% across repeated runs |
| Source citation rate | 100% of flagged outputs |
| Weekly commits | ≥3 per week |

---

## Individual OKR — Backend & Data

### Owner: Ashmita
⚙️ **Backend · API + Data + Integration + Export**

### Objective
Build a robust, reliable backend that connects the AI pipeline to the frontend, stores validation results, and enables data export in Overture-compatible formats.

The glue layer — if the API breaks, nothing works end-to-end.

### Key Results

#### Backend Infrastructure

| KR | Target |
|----|--------|
| **KR 1** | Set up PostgreSQL + PostGIS schema capable of storing confidence scores, citations, and correction proposals by end of Week 4. |
| **KR 2** | Ship all FastAPI endpoints required by the frontend (review queue, approve/reject, analytics feed) by Week 7. |
| **KR 3** | Implement GeoJSON export endpoint that outputs Overture-compatible correction files by Week 9. |
| **KR 4** | Achieve zero critical API errors during the final demo run-through. |

#### Pipeline Integration & Real-World Testing

| KR | Target |
|----|--------|
| **KR 1** | Define and agree on the pipeline → API interface contract with Preetam by end of Week 3. |
| **KR 2** | Ensure the API can ingest and store 500+ validated place records without performance degradation. |
| **KR 3** | Build a benchmark dataset of ≥50 known correct/incorrect places, tested across ≥3 cities/regions with diverse data conditions, by Week 6. |
| **KR 4** | Document failure cases categorised by: missing data, conflicting sources, and ambiguous signals. Document all API endpoints with schemas in the repo by Week 8. |

#### Overture-Compatible Data Export

| KR | Target |
|----|--------|
| **KR 1** | Enable export of validated corrections in Overture-compatible GeoJSON format. |
| **KR 2** | Support GeoParquet export for large-scale dataset corrections ready for upstream Overture contribution. |
| **KR 3** | Track validation coverage (% of dataset processed) and expose it via API for dashboard consumption. |
| **KR 4** | Generate region-level error-type breakdowns queryable from the analytics feed endpoint. |

### Key Metrics

| Metric | Target |
|--------|--------|
| API uptime during demo | 100% |
| Records storable | 500+ without degradation |
| Benchmark dataset size | ≥50 verified places across ≥3 cities |
| Endpoint documentation | 100% of endpoints documented |
| Interface contract agreed | By end of Week 3 |
| Export formats supported | GeoJSON + GeoParquet |

---

## Individual OKR — Frontend & UX

### Owner: Devesh
🖥️ **Frontend · Dashboard + UX + GitHub Pages**

### Objective
Design and ship a polished, intuitive dashboard that makes TerraLogic's validation results easy to explore, act on, and trust — in under 10 seconds per review.

The face of TerraLogic — what Overture Maps Foundation actually sees.

### Key Results

#### Human-in-the-Loop Dashboard

| KR | Target |
|----|--------|
| **KR 1** | Deliver a working MapLibre GL map view with color-coded pins (red / yellow / green by confidence score) by Week 5. |
| **KR 2** | Reduce average human review time per flagged place to <10 seconds through UI design and one-click workflows (approve / reject / skip). |
| **KR 3** | Achieve ≥80% acceptance rate for high-confidence AI suggestions among team testers by Week 9. |
| **KR 4** | Display all three required UI signals per place: confidence score, evidence sources, and error type (closed / moved / renamed). |

#### Actionable Analytics at Scale

| KR | Target |
|----|--------|
| **KR 1** | Ship a review queue (approve / reject / skip) connected to the live backend API by Week 7. |
| **KR 2** | Add at least 3 analytics views: error type breakdown chart, confidence score histogram, and regional coverage heatmap. |
| **KR 3** | Track and display validation coverage (% of dataset reviewed) updating in real time from the backend. |
| **KR 4** | Publish a GitHub Pages landing page for TerraLogic that is live and shareable by Week 10. |

### Key Metrics

| Metric | Target |
|--------|--------|
| Review time per place | <10 seconds |
| AI suggestion acceptance rate | ≥80% for high-confidence items |
| Analytics views shipped | ≥3 distinct views |
| UI signals per flagged place | 3 (score, source, error type) |
| GitHub Pages | Live by Week 10 |

---

## How to Use These OKRs

### Scoring Guidelines

| Score | Interpretation |
|-------|-----------------|
| **0.0–0.3** | Did not make meaningful progress. Reassess the KR or the strategy. |
| **0.4–0.6** | Partial progress. On track but needs acceleration. Identify blockers. |
| **0.7–0.9** | Strong result. This is the target zone. 0.7 is a great OKR score. |
| **1.0** | You set the bar too low. Celebrate but raise the target next cycle. |

### Weekly Rhythm

Each person scores their KRs 0.0–1.0 at the weekly sync. Flag any KR below 0.5 immediately for the team to unblock.

OKRs are a living document — if a metric turns out to be the wrong thing to measure, update it at the Week 5 midpoint review.

**Commit regularly.** Consistent commits count toward your grade and keep the team in sync.

---

## Critical Integration Points

### Key Milestones

| Week | Milestone |
|------|-----------|
| **Week 2–3** | Preetam + Ashmita agree on the pipeline → API interface contract before any code is written. Highest-risk dependency. |
| **Week 5** | Devesh's map view should be demo-able against mock data even before the real backend is ready. |
| **Week 7** | Full end-to-end integration test — pipeline output → API → dashboard. Identify bugs early. |
| **Week 9** | Final accuracy benchmarking against ground truth. Lock the demo city and dataset. |

---

**TerraLogic · Project Terrapulse · Overture Maps Foundation · Spring 2026**