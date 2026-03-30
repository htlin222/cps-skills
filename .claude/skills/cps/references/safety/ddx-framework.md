# Differential Diagnosis Framework

## Approach 1: Anatomic (Organ System)

Systematically consider each organ system in the affected region:

| System | Consider |
|--------|----------|
| Cardiovascular | Ischemia, arrhythmia, valvular, pericardial, aortic, venous |
| Pulmonary | Airway, parenchymal, pleural, vascular (PE), mediastinal |
| GI | Esophageal, gastric, hepatobiliary, pancreatic, intestinal, peritoneal |
| Renal/Urologic | Parenchymal, obstructive, vascular, bladder |
| Neurologic | Central, peripheral, neuromuscular junction, muscular |
| Musculoskeletal | Bone, joint, muscle, tendon, soft tissue |
| Hematologic | RBC, WBC, platelet, coagulation |
| Endocrine | Thyroid, adrenal, pituitary, pancreatic, parathyroid |
| Dermatologic | Infectious, inflammatory, autoimmune, neoplastic |

Use this approach when the symptom localizes to a specific anatomic region (e.g., chest pain, abdominal pain, joint pain).

---

## Approach 2: Pathophysiologic (VINDICATE+)

| Category | Examples |
|----------|----------|
| **V**ascular | Thrombosis, embolism, hemorrhage, vasculitis, ischemia, aneurysm |
| **I**nfectious | Bacterial, viral, fungal, parasitic, mycobacterial, prion |
| **N**eoplastic | Primary, metastatic, paraneoplastic, lymphoproliferative |
| **D**egenerative | Osteoarthritis, dementia, disc disease |
| **I**atrogenic / Intoxication | Drug side effects, overdose, poisoning, post-procedural, withdrawal |
| **C**ongenital | Genetic, developmental, inherited metabolic |
| **A**utoimmune / Allergic | SLE, vasculitis, sarcoidosis, anaphylaxis, drug hypersensitivity |
| **T**raumatic | Fracture, contusion, laceration, compartment syndrome |
| **E**ndocrine / Metabolic | Electrolyte abnormalities, acid-base, hormonal, nutritional deficiency |

Use VINDICATE when the anatomic approach yields too narrow a list or when the symptom is systemic (e.g., fatigue, weight loss, fever).

---

## Must-Not-Miss Diagnoses by Symptom

These diagnoses are life-threatening and must be explicitly considered and excluded in every case.

### Chest Pain
- Acute coronary syndrome (ACS)
- Pulmonary embolism (PE)
- Aortic dissection
- Tension pneumothorax
- Esophageal rupture (Boerhaave syndrome)
- Cardiac tamponade

### Headache
- Subarachnoid hemorrhage (SAH)
- Bacterial meningitis
- Temporal (giant cell) arteritis
- Brain mass / elevated ICP
- Cerebral venous sinus thrombosis

### Abdominal Pain
- Ruptured abdominal aortic aneurysm (AAA)
- Mesenteric ischemia
- Ectopic pregnancy (reproductive-age female)
- Appendicitis / perforation
- Bowel obstruction with strangulation
- Splenic rupture

### Dyspnea
- Pulmonary embolism
- Tension pneumothorax
- Cardiac tamponade
- Anaphylaxis
- Acute decompensated heart failure
- Acute airway obstruction

### Syncope
- Cardiac arrhythmia (VT, VF, complete heart block)
- Pulmonary embolism
- Aortic stenosis (critical)
- Ruptured AAA
- Subarachnoid hemorrhage

### Fever
- Sepsis / bacteremia
- Meningitis / encephalitis
- Necrotizing fasciitis
- Endocarditis
- Epidural abscess

### Altered Mental Status
- Hypoglycemia
- Meningitis / encephalitis
- Intracranial hemorrhage
- Status epilepticus (nonconvulsive)
- Toxic ingestion / overdose
- Wernicke encephalopathy

### Back Pain
- Epidural abscess
- Cauda equina syndrome
- Aortic dissection / ruptured AAA
- Vertebral compression fracture with cord compression
- Spinal metastasis with cord compression

---

## Pre-test Probability Anchoring by Clinical Setting

| Setting | Prevalence Pattern | Anchoring Guidance |
|---------|-------------------|-------------------|
| Emergency Department | Higher prevalence of acute, emergent, life-threatening conditions | Anchor must-not-miss diagnoses at higher pre-test probability. ACS in CP presentation: 15-30%. PE in dyspnea: 10-20%. |
| Outpatient Clinic | Higher prevalence of chronic, common, benign conditions | Anchor common diagnoses higher. Chest pain more likely GERD/MSK (60-70%). Headache more likely tension/migraine (80-90%). |
| ICU | Higher prevalence of multisystem, critical, iatrogenic conditions | Consider nosocomial infections, drug effects, organ failure cascades. Sepsis and multi-organ dysfunction dominate. |
| Inpatient Ward | Mix of acute-on-chronic, hospital-acquired, post-procedural | Consider hospital-acquired infections, medication effects, deconditioning, VTE. |

---

## DDx Re-ranking Rules

### After Each Round

1. **Bayesian update**: Apply LRs from new findings to adjust probabilities for each diagnosis on the list.

2. **Normalization**: After updating individual diagnoses, normalize so the full list (including "other") sums to approximately 100%.

3. **Re-rank by probability**: Reorder the list from highest to lowest post-test probability.

4. **Must-not-miss check**: Ensure all must-not-miss diagnoses remain on the list until explicitly excluded with high confidence (post-test probability < 2% or definitive negative test).

5. **Add new diagnoses**: If a round reveals findings suggesting a diagnosis not on the original list, add it with an estimated probability and redistribute.

6. **Remove diagnoses**: Only remove a diagnosis from the top 10 if its probability falls below 1% AND it is not a must-not-miss diagnosis.

7. **Convergence check**: If a single diagnosis exceeds 90% and all must-not-miss diagnoses are excluded, the case may be ready for final diagnosis.

### Probability Redistribution

When one diagnosis gains probability, others must lose proportionally:

```
Adjusted P(Dx_i) = P(Dx_i) x (1 - P_gained) / (sum of all other P)
```

This preserves the relative ranking among unaffected diagnoses while maintaining a valid probability distribution.
