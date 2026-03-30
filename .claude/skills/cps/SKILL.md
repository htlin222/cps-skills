---
name: cps
description: End-to-end clinical diagnostic reasoning skill. Takes a patient case (SCENARIO.md), runs multi-persona Bayesian reasoning rounds with textbook evidence and literature search, outputs structured DDx with likelihood ratios. Use when solving clinical cases, generating differential diagnoses, discussing clinical scenarios, or running diagnostic rounds.
---

# CPS: Clinical Problem Solving

Models the NEJM Clinical Problem-Solving format. Multi-persona diagnostic rounds apply Bayesian reasoning with likelihood ratios to systematically narrow a differential diagnosis, supported by textbook extraction and literature evidence.

## Quick Start

```
/cps path/to/SCENARIO.md
/cps discover chest pain
/cps round ./case/45f-chest-pain 6
/cps review ./case/45f-chest-pain
```

## Subcommands

| Command | Purpose |
|---------|---------|
| `/cps SCENARIO.md` | Full 7-phase diagnostic workflow |
| `/cps discover [topic]` | Search for challenging cases from medical literature |
| `/cps round [case-dir] N` | Run additional round N on an existing case |
| `/cps review [case-dir]` | Review and update DDx for an existing case |
| `/cps retro [case-dir] [correct-dx]` | Retrospective evaluation after answer revealed |

---

## Full Workflow (`/cps SCENARIO.md`)

Copy this checklist and track progress:

```
- [ ] Phase 1: Case Intake & Setup → Validate (Red Flag History HARD GATE)
- [ ] Phase 2: Symptom Mapping & DDx → Validate (MNM coverage, Syndromic Screen)
- [ ] Phase 3: Initial DDx (Attending) → Validate (LR completeness, Rare Cause Search)
- [ ] Phase 4: Multi-Persona Rounds → Validate (Hypothesis Space Audit after EACH round)
- [ ] Phase 5: Evidence Search (Round 4)
- [ ] Phase 6: Bayesian Probability Update
- [ ] Phase 7: Final Diagnosis → Validate (convergence, MNM exclusion, unification test)
```

**Validation**: After each phase, complete the corresponding checklist from [validation-checklist.md](references/safety/validation-checklist.md) and append to `VALIDATION.md`. Phase 1 Red Flag History is a **HARD GATE** — must pass before proceeding.

### Phase 1: Case Intake & Setup

1. Read the SCENARIO.md file
2. Extract a URL-safe slug from the case (e.g., `45f-chest-pain-dyspnea`)
3. Initialize case directory:
   ```bash
   python .claude/skills/cps/scripts/init_case.py "{slug}" "path/to/SCENARIO.md" --base-dir ./case
   ```
4. Parse structured data from the scenario: demographics, chief complaint(s), HPI, PMH, medications, vitals, PE, labs, imaging

### Phase 2: Symptom Mapping & Textbook Extraction

1. Identify chief complaint(s) and map to textbook chapters using [references/core/chapter-map.md](references/core/chapter-map.md)
2. Read the relevant pre-distilled chapter references (typically 1-3). For example, chest pain + dyspnea:
   - Read [references/chapters/ch09-chest-pain.md](references/chapters/ch09-chest-pain.md)
   - Read [references/chapters/ch15-dyspnea.md](references/chapters/ch15-dyspnea.md)
3. Focus on each chapter's:
   - Differential diagnosis framework and pivotal findings
   - Likelihood ratios (LR+/LR-) for key findings
   - Diagnostic algorithms and decision points
   - Must-not-miss diagnoses and red flags
4. **Always read [references/chapters/ch01-diagnostic-process.md](references/chapters/ch01-diagnostic-process.md)** — it contains the core clinical reasoning methodology

### Phase 3: Initial DDx — Round 1 (Attending Physician)

Adopt the **Attending Physician (Internal Medicine)** persona. See [references/core/personas.md](references/core/personas.md).

1. Write a **problem representation**: "This is a [age][sex] with [key PMH] presenting with [duration] of [chief complaint], associated with [key features], in the setting of [relevant context]"
2. Generate **Top 10 DDx** with pre-test probabilities:
   - Use epidemiologic prevalence for the symptom in the relevant clinical setting
   - Adjust for demographics (age, sex, risk factors)
   - Flag all **must-not-miss** diagnoses regardless of probability — see [references/safety/ddx-framework.md](references/safety/ddx-framework.md)
   - Use both anatomic and pathophysiologic (VINDICATE) approaches
3. For each diagnosis, list key supporting and opposing evidence from the scenario
4. Write output to `round-1.md` using the template from [references/templates/output-templates.md](references/templates/output-templates.md)

### Phase 4: Diagnostic Testing — Rounds 2-3

#### Round 2: Radiology & Pathology

Activate personas based on available data (see [references/core/personas.md](references/core/personas.md)):

- **Radiologist**: If imaging data present (CXR, CT, MRI, US, etc.)
- **Pathologist**: If lab/biopsy data present (CBC, CMP, UA, cultures, histology)

For each finding:
1. Provide structured interpretation
2. Look up the **likelihood ratio** — use [references/core/bayesian-reasoning.md](references/core/bayesian-reasoning.md) for common LRs
3. Apply LR to update the probability for each relevant diagnosis
4. Write output to `round-2.md`

#### Round 3: Subspecialty Consultation

Select 1-2 subspecialists based on the case presentation:

| Symptom Category | Subspecialist |
|-----------------|---------------|
| Chest pain, dyspnea, syncope, edema | Cardiologist |
| Cough, dyspnea, wheezing, hemoptysis | Pulmonologist |
| Fever, immunocompromised, travel | Infectious Disease |
| Headache, dizziness, delirium, focal deficits | Neurologist |

Each subspecialist:
1. Provides domain-specific deep analysis
2. Applies specialty-specific clinical decision rules and risk scores
3. Recommends additional testing with expected LRs
4. Writes output to `round-3.md`

### Phase 5: Evidence Synthesis — Round 4 (EBM Specialist)

Adopt the **EBM Specialist** persona. Two evidence sources:

#### WebSearch (always available)
Search for current evidence on the leading diagnoses:
- `"[diagnosis] [key finding] likelihood ratio"` — find LR values
- `"[diagnosis] diagnostic criteria guidelines 2024 2025"` — current guidelines
- `"[symptom] differential diagnosis evidence-based"` — DDx evidence

#### robust-lit-review CLI (optional, requires .env)
If `.env` is configured with API keys:
```bash
lit-review review "[clinical question]" --target 50 --min-citescore 3.0
```
If `.env` is not configured or `lit-review` is not installed, note the limitation and proceed with WebSearch only.

For each piece of evidence found:
1. Assess level of evidence (systematic review > RCT > cohort > case series > expert opinion)
2. Extract relevant LR values, sensitivity/specificity data
3. Note any guideline recommendations that affect the DDx

Write output to `round-4.md` with an evidence summary table.

### Phase 6: Bayesian Probability Update

After all rounds are complete, compile all likelihood ratios applied and run the calculator:

1. Prepare JSON input with all diagnoses, priors, and findings with LRs
2. Run the calculator:
   ```bash
   echo '{"diagnoses": [...]}' | python .claude/skills/cps/scripts/lr_calculator.py
   ```
3. Review the output probability table
4. Write to `probability-table.md`

See [references/core/bayesian-reasoning.md](references/core/bayesian-reasoning.md) for formulas and common LR values.

### Phase 7: Final Diagnosis — Round 5 (Diagnostic Conference)

Synthesize all rounds into the final diagnosis:

1. Write `round-5.md` as a **Diagnostic Conference** combining all persona perspectives
2. Determine the **leading diagnosis** with its post-test probability
3. Explain the **reasoning chain**: how each key finding shifted the probability
4. Document **why not** for each alternative in the Top 10
5. List **must-not-miss diagnoses** that were ruled out, and how
6. Provide **teaching points** from the case
7. Write `FINAL_DX.md` using the template from [references/templates/output-templates.md](references/templates/output-templates.md)

---

## Discover Subcommand (`/cps discover [topic]`)

Search for challenging clinical cases to test the CPS skill.

1. Use WebSearch with queries from [references/discovery/case-discovery.md](references/discovery/case-discovery.md):
   - `"clinical problem-solving" site:nejm.org [topic]`
   - `"case records" site:nejm.org [topic]`
   - `"case report" site:casereports.bmj.com [topic]`
2. Present a table of found cases with: title, source, year, difficulty estimate
3. When the user selects a case, extract key information and format as SCENARIO.md
4. Offer to run the full CPS workflow on the formatted scenario

Difficulty levels: See [references/discovery/case-discovery.md](references/discovery/case-discovery.md)

---

## Round Subcommand (`/cps round [case-dir] N`)

Add an additional diagnostic round to an existing case:

1. Read the existing scenario and all prior rounds from the case directory
2. Ask which persona should lead Round N (or auto-select based on case needs)
3. The new persona reviews all prior work and contributes fresh analysis
4. Update the probability table with any new LR applications
5. Write `round-N.md` to the case directory

---

## Review Subcommand (`/cps review [case-dir]`)

Review and update an existing case:

1. Read SCENARIO.md and all round files
2. Identify gaps: missing LRs, unaddressed findings, overlooked diagnoses
3. Suggest additional rounds or evidence searches
4. Optionally regenerate FINAL_DX.md with updated reasoning

---

## Retro Subcommand (`/cps retro [case-dir] [correct-dx]`)

Retrospective evaluation when the correct diagnosis is known (e.g., NEJM answer reveal):

1. Read SCENARIO.md, all round files, and VALIDATION.md from the case directory
2. Copy template from [references/templates/retrospective-template.md](references/templates/retrospective-template.md)
3. Complete **Diagnostic Trajectory Analysis** (Q1-Q4: was correct Dx in Top 10? Which pivot? Earliest data?)
4. **Grade each phase A-F** with specific failure modes (anchoring, knowledge gap, trigger not fired, etc.)
5. Complete **Safety Check Retrospective** table (should-have-fired vs did-fire)
6. Document **Lessons Learned** (new safety checks, reference gaps, workflow changes)
7. Write `RETROSPECTIVE.md` to the case directory
8. Write `PERFORMANCE.md` using template from [references/templates/performance-metrics.md](references/templates/performance-metrics.md)
9. Update `case/PERFORMANCE_TRACKER.md` with this case's metrics row

---

## SCENARIO.md Input Format

Cases can be free-form text, but this structure is recommended:

```markdown
# [Brief Case Title]

## Chief Complaint
[Main reason for presentation]

## History of Present Illness
[Narrative of the current episode]

## Past Medical History
[Comorbidities, surgeries]

## Medications
[Current medications]

## Social History
[Smoking, alcohol, occupation, travel]

## Family History
[Relevant family conditions]

## Vital Signs
T: __ HR: __ BP: __/__ RR: __ SpO2: __%

## Physical Examination
[System-by-system findings]

## Laboratory Data
[Labs with values and reference ranges]

## Imaging
[Imaging study descriptions and findings]

## Additional Studies
[ECG, PFTs, cultures, biopsies, etc.]
```

---

## Reference Files (Sub-Module Structure)

Only `core/` loads every run. Others load on demand to minimize context usage.

**`core/`** — Always loaded (~386 lines)

| File | Lines | Content |
|------|-------|---------|
| [chapter-map.md](references/core/chapter-map.md) | 73 | Symptom → chapter mapping |
| [personas.md](references/core/personas.md) | 149 | 8 persona definitions + activation rules |
| [bayesian-reasoning.md](references/core/bayesian-reasoning.md) | 164 | LR formulas + common clinical LR table |

**`chapters/`** — Load 1-3 per case (~80-120 lines each)

| [chapters/ch01-ch33](references/chapters/) | 33 files | Evidence-based DDx, LRs, algorithms per symptom |

**`templates/`** — Load when writing output

| [output-templates.md](references/templates/output-templates.md) | 158 | FINAL_DX, round-N, probability-table templates |
| [retrospective-template.md](references/templates/retrospective-template.md) | 106 | Post-case grading (for `/cps retro`) |
| [performance-metrics.md](references/templates/performance-metrics.md) | 56 | Cross-case metrics definitions |

**`safety/`** — Load during validation

| [validation-checklist.md](references/safety/validation-checklist.md) | 125 | Step validation per phase |
| [ddx-framework.md](references/safety/ddx-framework.md) | 144 | VINDICATE + must-not-miss lists |
| [rare-causes.md](references/safety/rare-causes.md) | 63 | NF1, KD, SCAD, PXE, Fabry... |

**`discovery/`** — Load only for `/cps discover`

| [case-discovery.md](references/discovery/case-discovery.md) | 80 | Finding challenging cases from literature |

## Scripts

| Script | Usage |
|--------|-------|
| `init_case.py` | `python scripts/init_case.py "slug" SCENARIO.md` — initialize case directory |
| `lr_calculator.py` | `echo '{"diagnoses":[...]}' \| python scripts/lr_calculator.py` — Bayesian calculator |
| `extract_chapter.py` | `python scripts/extract_chapter.py 9 15` — re-extract from epub (optional, if epub present) |

## Safety Checks (Built from Case Retrospectives)

### 1. Red Flag History Checkpoint
**When**: Patient has unusual PMH (MI at <40, stroke at <50, aneurysm at <60)
**Action**: Before generating DDx, DEMAND the etiology of the prior event. Do NOT assume the current event shares the same mechanism without evidence.

### 2. Syndromic Screen
**When**: Vascular disease etiology is unclear in a patient <50
**Action**: Trigger a comprehensive review beyond the chief complaint:
- Complete skin exam (café-au-lait spots, neurofibromas, xanthomas, skin laxity)
- Eye exam (Lisch nodules, lens subluxation, angioid streaks)
- Vascular exam of all territories (pulse asymmetry, bruits)
- Connective tissue screen (joint hypermobility, arm span, pectus)
- 3-generation family pedigree with inheritance pattern analysis

### 3. Rare Cause Search
**When**: Diagnostic findings (cath, imaging, biopsy) reveal a pattern not matching common DDx
**Action**: WebSearch for comprehensive etiologic reviews before defaulting to the "most common" cause. The textbook chapters cover common diagnoses; rare causes need active search.

### 4. Hypothesis Space Audit
**When**: After EVERY round, before finalizing probabilities
**Action**: Ask explicitly: *"Is there a diagnosis NOT in our Top 10 that could explain ALL the findings?"*
- Bayesian updating can only redistribute probability among existing hypotheses
- If the true diagnosis isn't in the DDx, no amount of LR application will find it
- Force consideration of unifying diagnoses that explain seemingly unrelated findings

### 5. Genetic Pattern Recognition
**When**: Family history shows autosomal dominant premature vascular/cardiac disease
**Action**: Consider genetic vasculopathies: NF1, Marfan, vascular Ehlers-Danlos, Loeys-Dietz, FMD, ACTA2

## Key Principles

1. **Evidence over intuition**: Every probability shift must cite a likelihood ratio with source
2. **Must-not-miss first**: Always identify and explicitly rule out dangerous diagnoses
3. **Bayesian discipline**: Pre-test → apply LR → post-test. No skipping steps
4. **Multi-perspective**: No single persona owns the diagnosis — the conference decides
5. **Transparent reasoning**: Every round documents what changed and why
6. **Hypothesis humility**: The DDx is never closed. Unexpected findings demand expanding the hypothesis space, not forcing them into existing categories
