#!/usr/bin/env python3
"""Initialize case directory structure for Clinical Problem Solving."""

import argparse
import os
import shutil
import sys


ROUND_HEADERS = {
    1: "Attending Physician (Internal Medicine)",
    2: "Diagnostic Testing (Radiology & Pathology)",
    3: "Subspecialty Consultation",
    4: "Evidence Synthesis (EBM)",
    5: "Diagnostic Conference (Consensus)",
}

PROBABILITY_TABLE_TEMPLATE = """# Probability Table

| Diagnosis | Prior | Finding (LR) | Posterior | Finding (LR) | Posterior | Final |
|-----------|-------|---------------|----------|---------------|----------|-------|
|           |       |               |          |               |          |       |
"""

FINAL_DX_TEMPLATE = """# Final Diagnosis

<!-- Replace with final diagnosis and supporting evidence -->
"""


def main():
    parser = argparse.ArgumentParser(
        description="Initialize case directory structure for CPS."
    )
    parser.add_argument(
        "slug",
        help='Case slug, e.g. "45f-chest-pain"'
    )
    parser.add_argument(
        "scenario_path",
        help="Path to the scenario markdown file"
    )
    parser.add_argument(
        "--base-dir", default="./case",
        help="Base directory for cases (default: ./case)"
    )
    args = parser.parse_args()

    case_dir = os.path.join(args.base_dir, args.slug)

    # Validate scenario file exists
    if not os.path.isfile(args.scenario_path):
        print(f"Error: Scenario file not found: {args.scenario_path}", file=sys.stderr)
        sys.exit(1)

    # Create case directory
    os.makedirs(case_dir, exist_ok=True)

    # Copy scenario file (skip if src and dst are the same path)
    dst_scenario = os.path.join(case_dir, "SCENARIO.md")
    if os.path.abspath(args.scenario_path) != os.path.abspath(dst_scenario):
        shutil.copy2(args.scenario_path, dst_scenario)

    # Create round files (only if they don't exist or are empty)
    for round_num, subtitle in ROUND_HEADERS.items():
        filepath = os.path.join(case_dir, f"round-{round_num}.md")
        if not os.path.isfile(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, "w") as f:
                f.write(f"# Round {round_num}: {subtitle}\n")

    # Create probability table (only if doesn't exist or empty)
    prob_path = os.path.join(case_dir, "probability-table.md")
    if not os.path.isfile(prob_path) or os.path.getsize(prob_path) == 0:
        with open(prob_path, "w") as f:
            f.write(PROBABILITY_TABLE_TEMPLATE)

    # Create validation log (only if doesn't exist or empty)
    val_path = os.path.join(case_dir, "VALIDATION.md")
    if not os.path.isfile(val_path) or os.path.getsize(val_path) == 0:
        with open(val_path, "w") as f:
            f.write("# Validation Log\n")

    # Create performance scorecard (only if doesn't exist or empty)
    perf_path = os.path.join(case_dir, "PERFORMANCE.md")
    if not os.path.isfile(perf_path) or os.path.getsize(perf_path) == 0:
        with open(perf_path, "w") as f:
            f.write("# Performance Scorecard\n")

    # Create final diagnosis file (only if doesn't exist or empty)
    final_path = os.path.join(case_dir, "FINAL_DX.md")
    if not os.path.isfile(final_path) or os.path.getsize(final_path) == 0:
        with open(final_path, "w") as f:
            f.write(FINAL_DX_TEMPLATE)

    print(os.path.abspath(case_dir))


if __name__ == "__main__":
    main()
