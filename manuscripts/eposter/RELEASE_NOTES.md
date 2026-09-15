# WCIM 2026 E-Poster

One-page A4 e-poster for the 38th World Congress of Internal Medicine
(Taipei, 2026).

**An Artificial Intelligence Clinico-Pathological Conference: Multi-Persona
Bayesian Clinical Reasoning With Closed-Loop Self-Generated Bedside Safety
Checks For Internal Medicine Training**

Hsieh-Ting Lin, MD — Division of Hematology & Medical Oncology,
Koo Foundation Sun Yat-Sen Cancer Center, Taipei, Taiwan

## Asset

`eposter.pdf` — A4 portrait, 1 page, ~170 KB, Arial-metric fonts embedded.

## Contents

- Closed-loop architecture: scenario → rounds → final diagnosis →
  retrospective grading → self-generated safety check, written back into the
  reasoning engine
- Case 1 (Lambert-Eaton myasthenic syndrome): likelihood-ratio cascade,
  35.0% → 99.6%
- Case 2 (NF1 vasculopathy): five diagnostic pivots, each internally coherent
  and confidently wrong
- Six safety checks the system derived from its own failures
- Key result: Bayesian reasoning is bounded by the hypothesis space

## Rebuilding

```bash
cd manuscripts/eposter
./build.sh                       # bundled vector letterhead
./build.sh path/to/template.png  # official WCIM template artwork
```

## Note on the letterhead

`assets/wcim-bg.svg` is a vector reconstruction of the WCIM 2026 template, not
the official artwork. Pass the official file to `build.sh` to swap it in; the
content box is unchanged.
