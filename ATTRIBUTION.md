# Attribution

## Clinical Data Sources

The 33 chapter reference files in `.claude/skills/cps/references/chapters/` contain diagnostic frameworks, likelihood ratio tables, and clinical algorithms compiled from peer-reviewed medical literature.

All citations use pandoc-style `[@key]` format. The complete bibliography is maintained in [`references.bib`](references.bib).

## Key Source Categories

### Evidence-Based Physical Diagnosis
- Clinical likelihood ratio compilations [@mcgee2018]
- JAMA Rational Clinical Examination series [@simel2009]

### Clinical Decision Rules
- Wells criteria for PE [@wells2001] and DVT [@wells2003]
- Modified Centor score [@centor1981; @mcisaac1998]
- Ottawa SAH rules [@perry2013]
- HINTS exam [@kattah2009]
- Glasgow-Blatchford score [@blatchford2000]
- Alvarado score [@alvarado1986]
- Light's criteria [@light1972]
- CAM for delirium [@inouye1990]

### Methodology
- Bayesian diagnostic reasoning and Fagan nomogram [@fagan1975]
- Evidence-based medicine principles [@sackett2000]

### Guidelines
- USPSTF screening recommendations [@uspstf2023]
- AHA/ACC cardiovascular guidelines

## Scope of Content

The chapter references are condensed clinical data summaries (60-120 lines each) containing:
- Likelihood ratio values (LR+/LR-) from original validation studies
- Sensitivity and specificity data
- Diagnostic algorithms and clinical decision rules
- Must-not-miss diagnoses and red flags

These are structured data references for clinical reasoning, not reproductions of any single source.

## Contributing

To add or correct a citation, update `references.bib` with the appropriate BibTeX entry and add `[@key]` references in the relevant chapter files.
