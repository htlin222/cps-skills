# CPS Output Templates

## FINAL_DX.md Template

```markdown
# Final Diagnosis: {Case Title}

## Case Summary
{1-paragraph problem representation: "This is a [age][sex] with [PMH] presenting with [duration] of [CC] with [key features] concerning for [framework]."}

## Final Diagnosis
**{Diagnosis}** (Post-test probability: XX%)

### Reasoning Chain
1. {Finding} -> LR {value} -> probability updated from X% to Y%
2. {Finding} -> LR {value} -> probability updated from X% to Y%
3. ...

## Top 10 Differential Diagnosis
| Rank | Diagnosis | Final Prob | Key For | Key Against | Must-Not-Miss |
|------|-----------|-----------|---------|-------------|---------------|
| 1 | {Dx} | XX% | {supporting evidence} | {opposing evidence} | {Yes/No} |
| 2 | ... | ... | ... | ... | ... |

## Must-Not-Miss Diagnoses Ruled Out
| Diagnosis | How Excluded | Confidence |
|-----------|-------------|------------|
| {Dx} | {Test/finding that excluded it} | {High/Moderate/Low} |

## Key Likelihood Ratios Applied
| Test/Finding | Result | LR Applied | Pre->Post | Source |
|-------------|--------|-----------|----------|--------|
| {Test} | {Result} | {LR+/LR-} | {X% -> Y%} | {Citation} |

## Supporting Evidence
| Source | Finding | Level of Evidence |
|--------|---------|-------------------|
| {Guideline/Study} | {Relevant finding} | {I-V, A-D} |

## Teaching Points
1. {Key learning point from this case}
2. {Common pitfall or pearl}
3. ...

## References
1. {Citation}
2. {Citation}
```

---

## round-N.md Template

```markdown
# Round N: {Persona Name} ({Specialty})

## Key Findings Analyzed
- {finding}: {interpretation and clinical significance}
- {finding}: {interpretation and clinical significance}

## Likelihood Ratios Applied
| Finding | LR+/LR- | Pre-test | Post-test | Source |
|---------|---------|----------|-----------|--------|
| {finding} | {value} | {X%} | {Y%} | {citation or textbook} |

## Updated DDx Assessment
| Rank | Diagnosis | Updated Prob | Change | Rationale |
|------|-----------|-------------|--------|-----------|
| 1 | {Dx} | XX% | {+/-/=} | {why probability changed} |
| 2 | ... | ... | ... | ... |

## Recommendations
- {Next diagnostic step or test recommendation}
- {Management consideration if applicable}

## Summary
{Brief 2-3 sentence perspective from this persona's specialty viewpoint, highlighting the most important findings and their diagnostic implications.}
```

---

## probability-table.md Template (Running Bayesian Table)

```markdown
# Probability Tracking Table: {Case Title}

## Current Top 10 DDx with Running Probabilities

| Rank | Diagnosis | Pre-test | R1 Post | R2 Post | R3 Post | R4 Final | Must-Not-Miss |
|------|-----------|----------|---------|---------|---------|----------|---------------|
| 1 | {Dx} | X% | X% | X% | X% | X% | {Yes/No} |
| 2 | ... | ... | ... | ... | ... | ... | ... |

## LR Application Log

| Round | Persona | Finding | LR | Diagnosis Affected | Prob Change |
|-------|---------|---------|----|--------------------|-------------|
| R1 | Attending | {finding} | {LR} | {Dx} | X% -> Y% |
| R2 | Pathologist | {lab result} | {LR} | {Dx} | X% -> Y% |
| ... | ... | ... | ... | ... | ... |

## Probability Normalization Notes
- Total probability across all diagnoses should approximate 100%
- After major shifts, redistribute remainder proportionally among other diagnoses
- "Other" category captures unlisted diagnoses (should decrease across rounds)
```

---

## SCENARIO.md Template (Case Input)

```markdown
# Case: {Title or ID}

## Demographics
- Age: {age}
- Sex: {M/F}
- Setting: {ED/Outpatient/ICU/Inpatient}

## Chief Complaint
{CC in patient's own words or brief clinical statement}

## History of Present Illness
{Chronological narrative with pertinent positives and negatives}

## Past Medical History
{PMH list}

## Medications
{Current medications}

## Allergies
{Drug allergies}

## Social History
{Tobacco, alcohol, drugs, occupation, travel, sexual history as relevant}

## Family History
{Relevant family history}

## Vital Signs
- T: {temp} | HR: {hr} | BP: {bp} | RR: {rr} | SpO2: {spo2} on {supplemental O2 or RA}

## Physical Examination
{Organized by system: General, HEENT, Neck, Lungs, CV, Abdomen, Extremities, Neuro, Skin}

## Laboratory Data
{Organized by panel: CBC, CMP, UA, coags, special labs}

## Imaging
{Imaging results with descriptions}

## Additional Studies
{ECG, PFTs, cultures, pathology, etc.}

## Clinical Question
{What is the most likely diagnosis? What is the next best diagnostic step?}
```
