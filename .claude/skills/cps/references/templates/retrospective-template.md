# CPS Retrospective Evaluation Template

Use when the correct diagnosis is known (e.g., NEJM reveal). Copy to `case/{slug}/RETROSPECTIVE.md`.

Invoke with: `/cps retro [case-dir] [correct-dx]`

---

# Retrospective: {Case Title}

## Case Identity

| Field | Value |
|-------|-------|
| Case | {slug} |
| Correct Diagnosis | {final answer} |
| CPS Final Diagnosis | {what the skill concluded} |
| Match | Correct / Partial / Incorrect |
| Date | {date} |

## Diagnostic Trajectory Analysis

### Q1: Was the correct Dx in the initial Top 10?
- [ ] Yes — Round 1, position ___, probability ___%
- [ ] No — first appeared in Round ___, position ___, probability ___%
- [ ] Never — correct Dx was never in the Top 10

### Q2: At which pivot did it first appear?
- **Round**: ___
- **Trigger**: {what new data or reasoning introduced it}
- **Initial probability**: ___%

### Q3: Earliest phase where enough data existed to consider it?
- **Phase**: ___
- **Data available**: {findings that should have been sufficient}
- **Why missed**: {anchoring / knowledge gap / trigger not fired / not in reference files}

### Q4: Could correct Dx have been reached without additional data?
- [ ] Yes — all necessary data present by Phase ___
- [ ] No — required data from Phase ___ (e.g., biopsy, genetic testing)

## Phase-by-Phase Grading

### Phase 1: Case Intake
- **Grade**: {A-F}
- **Done well**:
- **Failure mode**: None / Anchoring bias / Premature closure / Failed to investigate PMH etiology / Incomplete data extraction
- **Specific miss**:

### Phase 2: DDx Generation
- **Grade**: {A-F}
- **Done well**:
- **Failure mode**: None / MNM omission / Syndromic screen not triggered / Wrong chapter mapped / Correct Dx not in Top 10
- **Specific miss**:

### Phase 3: Round 1 DDx
- **Grade**: {A-F}
- **Done well**:
- **Failure mode**: None / LRs not applied / Pre-test prob poorly anchored / Rare cause not searched
- **Specific miss**:

### Phase 4: Rounds 2-3
- **Grade**: {A-F}
- **Done well**:
- **Failure mode**: None / Hypothesis space not audited / Genetic pattern missed / Wrong subspecialist / Evidence quality unchecked
- **Specific miss**:

### Phase 5: Final Dx
- **Grade**: {A-F}
- **Done well**:
- **Failure mode**: None / Convergence on wrong Dx / MNM not excluded / Unification test failed / Insufficient evidence search
- **Specific miss**:

## Safety Check Retrospective

| Safety Check | Should Have Fired? | Did Fire? | Impact If Fired |
|-------------|-------------------|-----------|-----------------|
| Red Flag History | Yes / No / NA | Yes / No | {description} |
| Syndromic Screen | Yes / No / NA | Yes / No | {description} |
| Rare Cause Search | Yes / No / NA | Yes / No | {description} |
| Hypothesis Space Audit | Yes / No / NA | Yes / No | {description} |
| Genetic Pattern Recognition | Yes / No / NA | Yes / No | {description} |

## Lessons Learned

### New Safety Checks Needed
{Any new checks this case reveals}

### Reference File Gaps
{Conditions or LR values to add to existing reference files}

### Skill Workflow Changes
{Changes to SKILL.md phases, persona selection, or validation rules}

## Summary Scorecard

| Phase | Grade | Key Failure | Earliest Fix Phase |
|-------|-------|-------------|-------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| **Overall** | | | |

**Scale**: A = Correct, no miss. B = Right direction, minor miss. C = Partially correct, significant miss. D = Wrong direction, major miss. F = Complete failure.
