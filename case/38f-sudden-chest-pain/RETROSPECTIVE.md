# Retrospective: Could AI + Family Doctor Have Reached NF1?

## The Honest Pivot-by-Pivot Analysis

### Pivot 1: Ambulance — "38F with prior MI + chest pain"

**What the AI did**: Jumped to SCAD (97.5%) based on "young woman + prior MI = SCAD" heuristic.

**Would a family doctor + AI have done differently?**
A family doctor would know this patient's FULL history — prior hospitalizations, medications, family history, skin findings. The specialist-oriented CPS workflow treated this as a de novo case with limited information.

**FAILURE POINT**: The CPS skill didn't prompt for a critical question: **"Why did this 38-year-old have her prior MI?"** If the skill had forced the attending persona to seek the etiology of the first MI before generating a DDx for the current event, the coronary aneurysms would have been known from the start.

**Fix needed**: Add a **"Red Flag History" checkpoint** — when a patient has an unusual past medical history (MI at <40), the skill should demand: "What was the established etiology? What were the cath findings? What is the underlying condition?"

| Grade | Verdict |
|-------|---------|
| **D** | Anchored on SCAD without investigating the prior MI etiology |

---

### Pivot 2: ECG + Labs — "Multi-territory MI + microcytic anemia"

**What the AI did**: Recognized multi-territory disease (old inferior + new anterior) shifted away from SCAD toward APS. Correctly identified microcytic anemia as a complicating factor.

**Would the AI have suggested the right workup?** Partially — we recommended APS panel, ANA, iron studies. These were appropriate. But we didn't flag **"complete skin exam"** at this stage.

**FAILURE POINT**: The CPS skill has no **"systems review trigger"** that fires when the etiology of coronary disease is unknown. A family doctor, seeing this patient longitudinally, would already know about her skin lesions. The AI, processing a case sequentially, needs a prompt to ask about ALL organ systems when the cardiac etiology is unclear.

**Fix needed**: Add a **"Syndromic Screen" module** — when coronary disease etiology is unclear in a young patient, automatically trigger: complete skin exam, eye exam, connective tissue screening, vascular exam of all territories, detailed family pedigree.

| Grade | Verdict |
|-------|---------|
| **C+** | Right direction (APS, autoimmune workup) but missed the skin exam prompt |

---

### Pivot 3: Catheterization — "Diffuse 3-vessel coronary aneurysms"

**What the AI did**: Correctly identified coronary aneurysms as the pivotal finding. Generated a DDx of KD, PAN, CTD, vasculitis. Ranked KD #1 at 90%.

**Would the AI have reached NF1?** NO — NF1 was not in the differential at all. The AI's DDx for "coronary aneurysms in young patient" was limited to: KD, PAN, Behçet, CTD, FMD. NF1 vasculopathy is rare and was not in the hypothesis space.

**FAILURE POINT**: The CPS skill's `ddx-framework.md` and chapter references don't include NF1 vasculopathy as a cause of coronary aneurysms. This is a **knowledge gap** — the reference chapters don't cover NF1 vasculopathy because it's a rare genetic condition beyond the scope of general internal medicine references.

**What would have helped?** If the AI had been prompted to do a WebSearch for "causes of coronary artery aneurysms young woman" at this stage, NF1 vasculopathy would likely have appeared in review articles and case reports. The EBM round (Round 4) should have been triggered HERE, not just for SCAD evidence.

**Fix needed**: Add a **"Rare Cause Search" trigger** — when the cath reveals an unexpected pattern (coronary aneurysms, not atherosclerotic), automatically run a WebSearch for comprehensive etiologic lists rather than relying solely on pre-loaded chapter references.

| Grade | Verdict |
|-------|---------|
| **B-** | Correctly identified aneurysms as pivotal; reasonable DDx; but missed NF1 entirely |

---

### Pivot 4: Rheumatology — "Skin papules + hyperpigmented patch"

**What the AI did**: Correctly flagged the skin findings as a diagnostic clue. Generated a DDx including NF1 (10%), sarcoidosis (25%), PXE (5%). Recommended skin biopsy.

**Would the AI have reached NF1?** YES, partially — NF1 was in the DDx at 10%. The AI recognized that papules could be neurofibromas and the hyperpigmented patch could be a café-au-lait spot. However, it ranked sarcoidosis higher (25%) and kept KD at 50%.

**What would have been better?** If the AI had been more aggressive about the **family history pattern** at this stage. Father (SCA at 45) + grandfather (HD at 37) = autosomal dominant inheritance. Combined with skin papules + possible café-au-lait spot + coronary aneurysms, NF1 should have been ranked higher. The AI noted the AD pattern but didn't weight it strongly enough.

**Fix needed**: Add a **"Genetic Pattern Recognition" module** — when family history shows an autosomal dominant pattern of premature vascular disease + skin findings, aggressively consider genetic vasculopathies (NF1, Marfan, Ehlers-Danlos, Loeys-Dietz).

| Grade | Verdict |
|-------|---------|
| **B+** | NF1 was in the DDx; correctly recommended derm consult and biopsy; but underweighted it |

---

### Pivot 5: Dermatology — "≥6 CAL spots + axillary freckling + neurofibromas"

**What the AI did**: Immediately recognized the diagnostic triad. Correctly diagnosed NF1 with 3/7 NIH criteria met. Connected NF1 vasculopathy to the coronary aneurysms and reinterpreted the family history.

**Grade: A** — Once the dermatology data was presented, the AI got it right instantly.

| Grade | Verdict |
|-------|---------|
| **A** | Instant recognition with the right data |

---

## Summary Scorecard

| Pivot | Data Available | AI Dx | Correct Dx | Grade | Key Failure |
|-------|---------------|-------|------------|-------|-------------|
| 1 | Young F + prior MI | SCAD (97.5%) | NF1 | D | Didn't investigate prior MI etiology |
| 2 | Multi-territory + anemia | APS (94.7%) | NF1 | C+ | No skin exam / syndromic screen |
| 3 | 3-vessel aneurysms | KD (90%) | NF1 | B- | NF1 not in knowledge base for aneurysm DDx |
| 4 | Skin papules + patch | KD/sarcoid/NF1 | NF1 | B+ | NF1 underweighted at 10% |
| 5 | CAL spots + freckling + fibromas | NF1 (>95%) | NF1 | A | — |

**Overall**: The AI would NOT have reached NF1 independently at Pivots 1-3. It needed the dermatology/rheumatology data (Pivots 4-5) to get there. A family doctor who already knew about the patient's skin findings could have reached it earlier — but only if the AI prompted them to report those findings.

---

## CPS Skill Improvements Needed

### 1. "Red Flag History" Checkpoint (Pivot 1 Fix)
**When**: Patient has unusual PMH (MI at <40, stroke at <50, etc.)
**Action**: Before generating DDx for the current event, DEMAND:
- "What was the established etiology of the prior event?"
- "What were the prior diagnostic findings (cath, imaging, labs)?"
- "Is there an underlying condition explaining premature disease?"

### 2. "Syndromic Screen" Module (Pivot 2 Fix)
**When**: Coronary/vascular disease etiology is unclear in a patient <50
**Action**: Automatically trigger a comprehensive review:
- Complete skin exam (café-au-lait spots, neurofibromas, xanthomas, skin laxity, striae)
- Eye exam (Lisch nodules, lens subluxation, angioid streaks)
- Vascular exam (pulse asymmetry, bruits in all territories)
- Connective tissue screen (joint hypermobility, arm span, pectus)
- Detailed 3-generation family pedigree with inheritance pattern analysis
- Genetic testing discussion

### 3. "Rare Cause Search" Trigger (Pivot 3 Fix)
**When**: Cath/imaging reveals an unexpected pattern not matching common DDx
**Action**: Run WebSearch for comprehensive etiologic review articles:
- `"[unexpected finding] causes differential diagnosis review"`
- `"[unexpected finding] young patient etiology"`
- Parse results for causes NOT already in the DDx

### 4. "Genetic Pattern Recognition" Module (Pivot 4 Fix)
**When**: Family history suggests autosomal dominant inheritance + vascular disease
**Action**: Aggressively rank genetic vasculopathies:
- NF1 (skin lesions + vascular aneurysms/stenosis)
- Marfan (tall, arm span, aortic root dilation)
- Vascular Ehlers-Danlos (translucent skin, easy bruising, arterial rupture)
- Loeys-Dietz (bifid uvula, hypertelorism, arterial tortuosity)
- FMD (string-of-beads on angiography)
- ACTA2 (smooth muscle dysfunction, moyamoya)

### 5. "Family Doctor Mode" for the CPS Skill
**Concept**: A variant workflow for primary care physicians who have longitudinal patient data.

Instead of starting with a single chief complaint (specialist mode), Family Doctor Mode starts with:
1. **Patient Profile**: Full PMH, medications, family pedigree, social history, prior workups
2. **Longitudinal Pattern Recognition**: What has changed over time? What patterns emerge across visits?
3. **Comprehensive Physical**: Including skin, eyes, joints, vascular — not just the organ system of complaint
4. **Genetic/Syndromic Screen**: When disease doesn't fit common patterns for the demographic

This mode leverages the family doctor's greatest advantage: **knowing the whole patient**, not just the acute presentation.

### 6. "Hypothesis Space Audit" (Meta-Fix)
**When**: After each round, before finalizing probabilities
**Action**: Ask explicitly: "Is there a diagnosis NOT in our Top 10 that could explain ALL the findings?"
- Force consideration of rare diagnoses
- Run a WebSearch if the clinical pattern is atypical
- Check if any single unifying diagnosis explains seemingly unrelated findings (aneurysms + skin lesions + family history + anemia)

This addresses the fundamental Bayesian limitation exposed by this case: **post-test probability can never exceed the probability mass assigned to hypotheses in your differential.** If NF1 isn't in the DDx, it can't emerge from Bayesian updating alone.
