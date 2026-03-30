# Bayesian Diagnostic Reasoning Reference

## Core Formulas

### Pre-test to Post-test Probability

```
Pre-test odds = P / (1 - P)
Post-test odds = Pre-test odds x LR
Post-test probability = Post-test odds / (1 + Post-test odds)
```

Where P = pre-test probability and LR = likelihood ratio for the test/finding.

### Likelihood Ratio Calculation

```
LR+ = Sensitivity / (1 - Specificity)
LR- = (1 - Sensitivity) / Specificity
```

Use these formulas to estimate LR when published values are unavailable but sensitivity/specificity data exists.

### Sequential Testing

When applying multiple independent tests:

```
Final odds = Pre-test odds x LR1 x LR2 x LR3 x ...
```

Tests must be conditionally independent for sequential multiplication to be valid. Correlated tests (e.g., two inflammatory markers) should not both be applied at full LR.

---

## LR Interpretation Scale

| LR+ Range | LR- Range | Strength | Effect on Probability |
|-----------|-----------|----------|----------------------|
| > 10 | < 0.1 | Strong | Large, often conclusive shift |
| 5 - 10 | 0.1 - 0.2 | Moderate | Meaningful shift |
| 2 - 5 | 0.2 - 0.5 | Small | Small but sometimes important shift |
| 1 - 2 | 0.5 - 1.0 | Negligible | Rarely changes management |
| 1.0 | 1.0 | Useless | No diagnostic value |

---

## High-Yield Clinical Likelihood Ratios

### Heart Failure (CHF)

| Finding | LR+ | LR- |
|---------|-----|-----|
| S3 gallop | 11.0 | 0.88 |
| JVD | 5.1 | 0.66 |
| Hepatojugular reflux | 6.4 | 0.79 |
| Peripheral edema | 2.3 | 0.64 |
| BNP > 500 pg/mL | 6.0 | 0.08 |
| BNP < 100 pg/mL | 0.11 | -- |
| Pulmonary rales | 2.8 | 0.51 |

### Abdominal Conditions

| Finding | Condition | LR+ | LR- |
|---------|-----------|-----|-----|
| Murphy sign | Cholecystitis | 2.8 | 0.5 |
| McBurney tenderness | Appendicitis | 3.4 | 0.4 |
| Psoas sign | Appendicitis | 2.4 | 0.90 |
| Rovsing sign | Appendicitis | 2.5 | -- |
| Shifting dullness | Ascites | 2.7 | 0.3 |
| Fluid wave | Ascites | 6.0 | 0.4 |
| Involuntary guarding | Peritonitis | 3.7 | -- |

### Pulmonary Embolism

| Finding | LR+ | LR- |
|---------|-----|-----|
| Wells score >= 7 (high) | 10.0 | -- |
| Wells score 2-6 (moderate) | 1.8 | -- |
| Wells score < 2 (low) | 0.25 | -- |
| Positive D-dimer | 1.6 | 0.10 |
| CT angiography positive | 24.0 | 0.05 |

### Neurological

| Finding | Condition | LR+ | LR- |
|---------|-----------|-----|-----|
| Kernig sign | Meningitis | 5.0 | 0.72 |
| Brudzinski sign | Meningitis | 5.0 | 0.72 |
| Jolt accentuation | Meningitis | 2.4 | 0.05 |
| Babinski sign | UMN lesion | 10.0 | -- |
| Pronator drift | Stroke | 6.0 | 0.45 |

### Cardiac / Chest Pain

| Finding | Condition | LR+ | LR- |
|---------|-----------|-----|-----|
| Troponin elevated (>99th %ile) | ACS | 7.0 | 0.19 |
| ST elevation (new) | STEMI | 13.0 | -- |
| HEART score >= 7 | ACS (30-day MACE) | 13.0 | -- |
| HEART score 0-3 | ACS (30-day MACE) | 0.08 | -- |
| Chest wall tenderness | Non-cardiac | 0.3 (for ACS) | -- |
| Pleuritic quality | Non-cardiac | 0.2 (for ACS) | -- |

### Infectious Disease

| Finding | Condition | LR+ | LR- |
|---------|-----------|-----|-----|
| Centor score 4 | Strep pharyngitis | 6.3 | -- |
| Centor score 0-1 | Strep pharyngitis | 0.16 | -- |
| Procalcitonin > 0.5 | Bacterial infection | 3.3 | 0.29 |
| Blood cultures positive | Bacteremia | -- | -- |
| Nuchal rigidity | Meningitis | 1.0 | -- |

---

## Worked Example

**Case**: 50-year-old male presents with acute substernal chest pain radiating to left arm, diaphoresis. No prior CAD. Smoker, hypertensive.

**Step 1: Anchor pre-test probability**
- Middle-aged male + risk factors + classic presentation
- Pre-test probability for ACS: 40%
- Pre-test odds: 0.40 / 0.60 = 0.667

**Step 2: Apply ECG finding (2mm ST depression in V3-V5)**
- ST changes for ACS: LR+ ~5.0
- Post-test odds: 0.667 x 5.0 = 3.33
- Post-test probability: 3.33 / 4.33 = 77%

**Step 3: Apply troponin result (elevated at 0.8 ng/mL)**
- Elevated troponin for ACS: LR+ ~7.0
- Pre-test odds (from Step 2): 3.33
- Post-test odds: 3.33 x 7.0 = 23.3
- Post-test probability: 23.3 / 24.3 = **96%**

**Conclusion**: After two pivotal findings, probability of ACS shifted from 40% to 96%. Warrants emergent cardiac catheterization.

---

## Fagan Nomogram

The Fagan nomogram provides a graphical shortcut for Bayesian updating:

1. Mark the **pre-test probability** on the left axis
2. Mark the **likelihood ratio** on the middle axis
3. Draw a straight line through both points
4. Read the **post-test probability** where the line crosses the right axis

This avoids manual odds conversion. Useful for quick bedside estimates and teaching.

---

## Practical Rules

1. **Pre-test probability matters most**: A very high LR+ applied to a very low pre-test probability may still yield a modest post-test probability. Never skip anchoring.

2. **Correlated tests**: Do not sequentially multiply LRs from non-independent tests (e.g., ESR and CRP both reflect inflammation). Use the single best test or discount the second LR.

3. **Spectrum bias**: Published LRs may come from populations with more severe disease. Adjust when applying to milder presentations.

4. **LR of 1 is not reassuring**: It means the test result is equally likely in those with and without disease. It provides zero information.

5. **Threshold approach**: Treatment threshold (~60-80% for many conditions) and testing threshold (~5-15%) define when to act vs. test vs. observe.
