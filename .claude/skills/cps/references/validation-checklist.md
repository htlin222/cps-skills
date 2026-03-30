# CPS Step Validation Checklist

After each phase, copy the corresponding section into `VALIDATION.md` and mark items `[x]`. If any critical item fails, document remediation before proceeding.

---

## Phase 1: Case Intake — Validation

### 1A. Red Flag History Check (**HARD GATE** — must pass before proceeding)
- [ ] Identify PMH items with unusual age-of-onset (MI <40, stroke <50, aneurysm <60, VTE <40 unprovoked)
- [ ] For each flagged item: "What was the established etiology?"
- [ ] For each flagged item: "What were the prior diagnostic findings (cath, imaging)?"
- [ ] For each flagged item: "Is there an underlying condition?"
- [ ] If etiology unknown → flag for Syndromic Screen in Phase 2

### 1B. Problem Representation
- [ ] Age, sex, key PMH (with etiology if relevant)
- [ ] Duration + acuity of chief complaint (acute/subacute/chronic)
- [ ] Pertinent positives and negatives
- [ ] Relevant context (setting, risk factors)
- [ ] Framing statement follows format: "This is a [age][sex] with [PMH] presenting with [duration] of [CC], associated with [features], in the setting of [context]"

### 1C. Data Extraction
- [ ] Demographics, medications (with doses), allergies
- [ ] Social history (smoking, alcohol, drugs, occupation, travel)
- [ ] Family history with ≥2 generations + inheritance pattern noted
- [ ] All vitals, PE findings (including pertinent negatives), labs with ranges

**Pass/Fail**: All 1A items must pass (HARD GATE). ≥4/5 in 1B. All 1C items.

---

## Phase 2: DDx Generation — Validation

### 2A. DDx Completeness
- [ ] ≥10 diagnoses generated
- [ ] Both anatomic AND pathophysiologic (VINDICATE) approaches used
- [ ] "Other/unlisted" category with ≥5% probability mass
- [ ] Probabilities sum to ~100%

### 2B. Must-Not-Miss Coverage
- [ ] All MNM diagnoses for chief complaint(s) listed (cross-ref ddx-framework.md)
- [ ] Each MNM has explicit exclusion plan
- [ ] No MNM removed until post-test prob <2% with documented evidence

### 2C. Syndromic Screen Trigger
Evaluate: Patient <50 AND (vascular/cardiac etiology unclear OR unexplained multi-system findings)?
- [ ] If YES → trigger syndromic screen:
  - [ ] Complete skin exam (CAL spots, neurofibromas, xanthomas, skin laxity, angiokeratomas)
  - [ ] Eye exam (Lisch nodules, lens subluxation, angioid streaks)
  - [ ] Vascular exam all territories (pulse asymmetry, bruits)
  - [ ] Connective tissue screen (hypermobility, arm span, pectus)
  - [ ] 3-generation family pedigree with inheritance pattern
- [ ] If NO → document why screen not needed

**Pass/Fail**: All 2A items. All 2B items. 2C evaluated (trigger or justify skip).

---

## Phase 3: Round 1 Initial DDx — Validation

### 3A. LR Application
- [ ] Every key PE finding evaluated for LR applicability
- [ ] Every abnormal lab result evaluated for LR applicability
- [ ] Every imaging finding evaluated for LR applicability
- [ ] LR source cited for each (chapter ref [@key], literature, or "estimated")
- [ ] Coverage: ___/___ findings with LRs (target >80%)

### 3B. Rare Cause Search Trigger
Evaluate: Do findings show a pattern NOT matching common DDx for this demographic?
- [ ] If YES → WebSearch: "[finding] causes differential review" + "[finding] [demographic] etiology"
- [ ] New diagnoses from search added to DDx with probabilities
- [ ] If NO → document why standard DDx is sufficient

### 3C. Pre-test Probability Anchoring
- [ ] Clinical setting documented (ED/outpatient/ICU)
- [ ] Prevalence data cited for anchoring top diagnoses
- [ ] Demographics applied (age, sex, ethnicity, risk factors)

**Pass/Fail**: 3A coverage >80%. 3B evaluated. All 3C items.

---

## Phase 4: Rounds 2-3 — Validation

### 4A. Hypothesis Space Audit (**MANDATORY after EACH round**)
- [ ] Explicitly asked: "Is there a diagnosis NOT in Top 10 explaining ALL findings?"
- [ ] If yes → added to DDx with probability + WebSearch for evidence
- [ ] If no → documented reasoning for current DDx adequacy
- [ ] Unexplained findings listed (if any remain after leading Dx)

### 4B. Evidence Quality
- [ ] Each LR has a source ([@key], study, or "estimated — needs verification")
- [ ] Correlated tests identified (e.g., ESR+CRP) — only best LR applied
- [ ] "Estimated" LRs flagged for verification in Round 4

### 4C. Genetic Pattern Recognition
Evaluate: Family history shows AD pattern of premature vascular/cardiac disease?
- [ ] If YES → screen for: NF1, Marfan, vEDS, Loeys-Dietz, FMD, ACTA2
- [ ] If NO → document why genetic screen not triggered

**Pass/Fail**: 4A performed after EACH round (mandatory). ≥3/4 in 4B. 4C evaluated.

---

## Phase 5: Final Diagnosis — Validation

### 5A. Bayesian Convergence
- [ ] Leading Dx post-test probability documented: ___%
- [ ] If >90%: convergence achieved → proceed to final Dx
- [ ] If <90%: additional testing/evidence recommended before closure
- [ ] Probability distribution normalized (sums to ~100%)

### 5B. Must-Not-Miss Exclusion
- [ ] Every MNM has explicit exclusion: test result, clinical finding, or prob <2%
- [ ] Confidence level for each: High / Moderate / Low
- [ ] No MNM excluded with "Low" confidence without follow-up plan

### 5C. Diagnostic Unification Test
- [ ] Final Dx explains ALL key findings
- [ ] Unexplained findings documented ("incidental", "comorbid", "needs further workup")
- [ ] Occam's razor: is single Dx sufficient or are multiple Dx needed?
- [ ] Alternative Dx that explain most findings → documented with rejection reasoning

**Pass/Fail**: 5A documented. All 5B items. All 5C items.
