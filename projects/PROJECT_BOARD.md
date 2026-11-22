# Project Board — Data Quality & Data Science Portfolio

**Updated:** 2026-11-22  
**Scope:** Demonstration projects created with fictional data.  
**How to interpret:** "Done" describes committed files, not production readiness or job experience. GitHub's separate Projects feature is not enabled by this file; this is a repository-based Kanban board.

## ✅ Done

| Deliverable | Evidence |
|---|---|
| Healthcare claims synthetic data generator and denial-risk baseline | [Code and model guide](./healthcare-claims-data-science) |
| Financial operations (KYC, claims, disputes) queue anomaly demo | [Code and guide](./financial-operations-data-science) |
| KYC, claims, disputes data-quality rules and exception reporting | [Code and rulebook](./financial-operations-data-quality) |
| Python CSV validation and SQL profiling examples | [Validator](./data-quality-validator) · [SQL](./sql-customer-quality) |
| Add automated tests workflow configuration | [GitHub Actions workflow](../.github/workflows/portfolio-tests.yml) |

## 🔄 In Progress / Verification Required

| Item | Next check |
|---|---|
| Confirm GitHub Actions completes | [View workflow runs](../actions/workflows/portfolio-tests.yml); do not assume passing before inspecting an actual run |
| Verify documentation matches latest outputs | Re-run examples after dependency installs and check reported metrics |

## 📋 To Do

| Priority | Planned improvement | Tracking |
|---|---|---|
| High | Add quality scorecards and a dashboard for KYC, claims, and disputes | [Issue #2](../issues/2) |
| High | Improve healthcare model interpretation, threshold evaluation and subgroup checks | [Issue #1](../issues/1) |
| Medium | CI robustness, environment versions, and data dictionaries | [Issue #3](../issues/3) |
| Medium | SQL automated regression checks and edge-case tests | Planned |
| Medium | Add model drift monitoring demonstration using fictional data | Planned |

## Build & evidence workflow

1. Define an operational question and a domain data dictionary.
2. Generate **synthetic** cases, including edge cases and known exceptions.
3. Implement a baseline (rules, SQL checks, or reproducible statistical model).
4. Write tests and sample run instructions.
5. Push changes as genuinely dated commits and inspect CI checks.
6. Record limitations, metrics, review requirements, and next issues.

## Development timeline

- **November 2026:** These sample projects, README guides, tests, progress tracking and workflow configuration were added to the repository.
- **2025:** No work is attributed to 2025 here without independent support. If there are authentic 2025 notebooks, analyses or notes, they can be documented separately with their true dates.

[Back to project tracker](./PROJECT_TRACKER.md) · [Back to profile](../README.md)
