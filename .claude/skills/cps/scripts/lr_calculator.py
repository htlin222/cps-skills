#!/usr/bin/env python3
"""Bayesian probability calculator using likelihood ratios."""

import argparse
import json
import sys


def prob_to_odds(p):
    """Convert probability to odds."""
    if p >= 1.0:
        return float("inf")
    if p <= 0.0:
        return 0.0
    return p / (1.0 - p)


def odds_to_prob(odds):
    """Convert odds to probability."""
    if odds == float("inf"):
        return 1.0
    if odds <= 0.0:
        return 0.0
    return odds / (1.0 + odds)


def format_pct(p):
    """Format probability as percentage string."""
    return f"{p * 100:.1f}%"


def calculate_diagnosis(dx):
    """Calculate posterior probabilities for a single diagnosis.

    Returns list of (finding_label, lr_applied, posterior) tuples
    and the final probability.
    """
    prior = dx["prior"]
    odds = prob_to_odds(prior)
    steps = []

    for finding in dx.get("findings", []):
        lr = finding["lr"]
        present = finding["present"]
        name = finding["name"]

        odds *= lr
        posterior = odds_to_prob(odds)

        if present:
            label = f"{name}+ (\u00d7{lr})"
        else:
            label = f"{name}\u2212 (\u00d7{lr})"

        steps.append((label, posterior))

    final = odds_to_prob(odds) if dx.get("findings") else prior
    return steps, final


def build_table(data):
    """Build markdown table from input data."""
    diagnoses = data["diagnoses"]

    # Calculate all results first
    results = []
    max_findings = 0
    for dx in diagnoses:
        steps, final = calculate_diagnosis(dx)
        must_not_miss = dx.get("must_not_miss", False)
        results.append({
            "name": dx["name"],
            "prior": dx["prior"],
            "steps": steps,
            "final": final,
            "must_not_miss": must_not_miss,
        })
        max_findings = max(max_findings, len(steps))

    # Build header
    header_parts = ["Diagnosis", "Prior"]
    for i in range(max_findings):
        header_parts.append(f"Finding {i + 1} (LR)")
        header_parts.append(f"Post-{i + 1}")
    header_parts.append("Final")

    lines = []
    lines.append("## Bayesian Probability Table")
    lines.append("")

    header_line = "| " + " | ".join(header_parts) + " |"
    sep_line = "| " + " | ".join("---" for _ in header_parts) + " |"
    lines.append(header_line)
    lines.append(sep_line)

    # Build rows
    for r in results:
        row = [r["name"], format_pct(r["prior"])]
        for step_label, posterior in r["steps"]:
            row.append(step_label)
            row.append(format_pct(posterior))
        # Pad if fewer findings than max
        while len(row) < 2 + max_findings * 2:
            row.append("")
        row.append(format_pct(r["final"]))
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    # Summary section
    lines.append("## Summary")
    lines.append("")

    ranked = sorted(results, key=lambda x: x["final"], reverse=True)
    for i, r in enumerate(ranked, 1):
        flag = " (MUST NOT MISS)" if r["must_not_miss"] else ""
        lines.append(f"{i}. **{r['name']}**: {format_pct(r['final'])}{flag}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Bayesian probability calculator using likelihood ratios."
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to input JSON file (default: read from stdin)"
    )
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    print(build_table(data))


if __name__ == "__main__":
    main()
