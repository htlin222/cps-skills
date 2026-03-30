# CPS Performance Metrics

## Metric Definitions

| # | Metric | Target | How Measured |
|---|--------|--------|-------------|
| 1 | **Diagnostic Accuracy** | 1.0 | Correct=1, Partial=0.5, Incorrect=0 |
| 2 | **Pivot Efficiency** | Round 1 | Round where correct Dx enters Top 3 at >20% prob |
| 3 | **Must-Not-Miss Sensitivity** | 100% | MNM flagged / MNM applicable |
| 4 | **Hypothesis Space Coverage** | 100% | Was correct Dx ever in Top 10? |
| 5 | **LR Application Completeness** | >80% | Findings with LRs / Total actionable findings |
| 6 | **Safety Check Trigger Rate** | 100% | Fired / Applicable, per check |
| 7 | **Phase Grade Distribution** | All A | Count A/B/C/D/F per phase across cases |

## Per-Case Scorecard (`PERFORMANCE.md`)

```markdown
# Performance: {Case Title}

| Metric | Value | Notes |
|--------|-------|-------|
| Diagnostic Accuracy | {1 / 0.5 / 0} | {Correct / Partial / Incorrect} |
| Pivot Efficiency | {1-5 / Never} | Correct Dx first in Top 3 at Round ___ |
| MNM Sensitivity | ___% | {X}/{Y} flagged |
| Hypothesis Coverage | {Yes / No} | First in Top 10 at Round ___ |
| LR Completeness | ___% | {X}/{Y} findings with LRs |
| Safety Checks Fired | {list} | {which checks fired} |
| Phase Grades | P1:_ P2:_ P3:_ P4:_ P5:_ | |
| Overall Grade | {A-F} | |
```

## Cross-Case Tracker (`case/PERFORMANCE_TRACKER.md`)

```markdown
# CPS Performance Tracker

| Case | Date | Accuracy | Pivot Eff | MNM Sens | Hyp Coverage | LR % | Overall |
|------|------|----------|-----------|----------|-------------|------|---------|
| {slug} | {date} | {0/0.5/1} | {1-5} | {%} | {Y/N (Rnd)} | {%} | {A-F} |

## Aggregates (update after 5+ cases)
- Diagnostic Accuracy Rate: ___
- Mean Pivot Efficiency: ___
- MNM Sensitivity: ___
- Hypothesis Coverage Rate: ___
- Mean LR Completeness: ___
- Weakest Phase: ___
- Least-fired Safety Check: ___
```

## Trend Analysis (after 5+ cases)
- Which phase has the lowest average grade?
- Which safety check fires least often when applicable?
- Is pivot efficiency improving over time?
- Are there diagnosis categories where the skill consistently fails?
- Are reference file gaps being filled after each retrospective?
