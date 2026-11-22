# Portfolio Project Tracker

**Last updated: 2026-11-22**  
**Project history:** The sample code in this GitHub account was added in November 2026. This tracker does not claim that code or commits existed in 2025.

## Project status

| Project | Code available | Documentation | Automated tests included | Next milestone |
|---|---|---|---|---|
| [Healthcare claims data science](./healthcare-claims-data-science) | ✅ | ✅ | ✅ | Add interpretability, subgroup evaluation and CI |
| [Financial operations anomaly analytics](./financial-operations-data-science) | ✅ | ✅ | ✅ | Compare with transparent rule-based queue prioritization |
| [KYC, claims & disputes data quality lab](./financial-operations-data-quality) | ✅ | ✅ | ✅ | Add quality scorecard and thresholds by domain |
| [Python data quality validator](./data-quality-validator) | ✅ | ✅ | ✅ | Add robust field rules and CI |
| [SQL data profiling](./sql-customer-quality) | ✅ | ✅ | Not included | Add SQL assertions and automated tests |

**Status definition:** "Code available" means files have been committed. "Tests included" means unit test source is present; it does not mean CI has run or the model is production ready.

## How these examples are built

1. **Define the use case:** clarify why an operational reviewer needs accurate data or a prioritization signal.
2. **Specify a data contract:** list expected columns, types, ranges and identifiers.
3. **Create fictional datasets:** generate synthetic records with representative normal cases and exceptions, never use real customer or patient data.
4. **Develop the baseline:** implement deterministic rule checks or a simple modeling approach before more complex methods.
5. **Validate:** add unit tests, examine output, and retain documented assumptions.
6. **Report:** produce a structured JSON/CSV output and explain how to interpret it.
7. **Improve:** log tasks as GitHub Issues; make changes with accurately dated commits and notes.

## Reproducible walkthroughs

- [Healthcare claims walkthrough](./healthcare-claims-data-science/README.md)
- [KYC, claims and disputes anomaly walkthrough](./financial-operations-data-science/README.md)
- [Rule-based financial operations quality walkthrough](./financial-operations-data-quality/README.md)

## Roadmap and automated verification

- [Project board — Done / In Progress / To Do](./PROJECT_BOARD.md)
- [Python automated tests workflow](../.github/workflows/portfolio-tests.yml)
- [Inspect workflow runs](../actions)

The test workflow configuration has been committed. Its execution status must be verified in GitHub Actions; do not treat the presence of the workflow as a passing run.

## Roadmap (planned, not yet delivered)

### Phase 1 — Baseline code and documentation
- [x] Data-quality checks for KYC, claims and disputes
- [x] Synthetic healthcare claims data and baseline classification
- [x] Synthetic operations queue anomaly model
- [x] README instructions and test source files

### Phase 2 — Reproducibility and reporting
- [x] GitHub Actions workflow configuration for Python unit tests (passing run not yet confirmed)
- [ ] Data dictionaries and more boundary-condition tests
- [ ] Charts and clear metric definitions
- [ ] Versioned sample result snapshots

### Phase 3 — Responsible analytics
- [ ] Evaluate error rates and subgroup differences for the healthcare example
- [ ] Document model sensitivity and limitations
- [ ] Add validation drift/monitoring examples
- [ ] Use human review workflow for all high-stakes applications

## About 2025

If you genuinely completed preparatory work, research or prototypes in 2025, add an **evidence-backed historical background** section noting what was done and when. Do not backdate Git commits or represent these November 2026 sample projects as completed in 2025.
