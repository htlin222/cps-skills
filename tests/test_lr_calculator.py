"""Tests for Bayesian LR calculator — the core diagnostic reasoning engine."""
import json
import subprocess
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".claude", "skills", "cps", "scripts"))
from lr_calculator import prob_to_odds, odds_to_prob, calculate_diagnosis, format_pct, build_table


class TestProbOddsConversion:
    """Probability <-> odds conversion must be mathematically correct."""

    def test_50_percent(self):
        assert prob_to_odds(0.5) == 1.0

    def test_odds_roundtrip(self):
        for p in [0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
            assert abs(odds_to_prob(prob_to_odds(p)) - p) < 1e-10

    def test_zero_probability(self):
        assert prob_to_odds(0.0) == 0.0
        assert odds_to_prob(0.0) == 0.0

    def test_one_probability(self):
        assert prob_to_odds(1.0) == float("inf")
        assert odds_to_prob(float("inf")) == 1.0

    def test_low_probability(self):
        odds = prob_to_odds(0.01)
        assert abs(odds - 0.01010101) < 1e-6

    def test_high_probability(self):
        odds = prob_to_odds(0.99)
        assert abs(odds - 99.0) < 1e-6


class TestCalculateDiagnosis:
    """Core Bayesian calculation logic."""

    def test_single_finding_positive(self):
        """Troponin+ with LR+ 11 on 25% prior → ~78.6%"""
        dx = {
            "name": "ACS",
            "prior": 0.25,
            "findings": [{"name": "Troponin+", "lr": 11.0, "present": True}]
        }
        steps, final = calculate_diagnosis(dx)
        assert len(steps) == 1
        assert abs(final - 0.7857) < 0.01

    def test_single_finding_negative(self):
        """Normal ECG with LR- 0.04 on 25% prior → ~1.3%"""
        dx = {
            "name": "MI",
            "prior": 0.25,
            "findings": [{"name": "Normal ECG", "lr": 0.04, "present": True}]
        }
        steps, final = calculate_diagnosis(dx)
        assert final < 0.02  # should be ~1.3%

    def test_sequential_lr_application(self):
        """Multiple findings applied sequentially — order shouldn't matter for final result."""
        dx_ab = {
            "name": "Test",
            "prior": 0.25,
            "findings": [
                {"name": "A", "lr": 5.0, "present": True},
                {"name": "B", "lr": 2.0, "present": True},
            ]
        }
        dx_ba = {
            "name": "Test",
            "prior": 0.25,
            "findings": [
                {"name": "B", "lr": 2.0, "present": True},
                {"name": "A", "lr": 5.0, "present": True},
            ]
        }
        _, final_ab = calculate_diagnosis(dx_ab)
        _, final_ba = calculate_diagnosis(dx_ba)
        assert abs(final_ab - final_ba) < 1e-10

    def test_no_findings(self):
        """No findings → probability stays at prior."""
        dx = {"name": "Test", "prior": 0.30, "findings": []}
        _, final = calculate_diagnosis(dx)
        assert final == 0.30

    def test_lr_of_one(self):
        """LR = 1.0 should not change probability."""
        dx = {
            "name": "Test",
            "prior": 0.40,
            "findings": [{"name": "Useless test", "lr": 1.0, "present": True}]
        }
        _, final = calculate_diagnosis(dx)
        assert abs(final - 0.40) < 1e-10

    def test_lems_case(self):
        """Reproduce Case 1: LEMS diagnosis with known LRs."""
        dx = {
            "name": "LEMS",
            "prior": 0.35,
            "findings": [
                {"name": "Proximal weakness + areflexia", "lr": 5.0, "present": True},
                {"name": "Low CMAPs", "lr": 8.0, "present": True},
                {"name": "SIADH", "lr": 3.0, "present": True},
                {"name": "Failed MG therapy", "lr": 4.0, "present": True},
            ]
        }
        _, final = calculate_diagnosis(dx)
        assert final > 0.99  # should be ~99.6%

    def test_strong_rule_out(self):
        """Strong LR- should drive probability very low."""
        dx = {
            "name": "PE",
            "prior": 0.30,
            "findings": [{"name": "Negative D-dimer", "lr": 0.05, "present": True}]
        }
        _, final = calculate_diagnosis(dx)
        assert final < 0.025  # ~2.1%

    def test_very_low_prior_with_positive_lr(self):
        """Even strong LR+ on very low prior shouldn't produce high probability."""
        dx = {
            "name": "Rare disease",
            "prior": 0.001,
            "findings": [{"name": "Positive test", "lr": 10.0, "present": True}]
        }
        _, final = calculate_diagnosis(dx)
        assert final < 0.02  # ~1% — base rate matters!


class TestFormatPct:
    def test_basic(self):
        assert format_pct(0.5) == "50.0%"
        assert format_pct(0.0) == "0.0%"
        assert format_pct(1.0) == "100.0%"
        assert format_pct(0.999) == "99.9%"


class TestBuildTable:
    """Integration test for full table generation."""

    def test_single_diagnosis(self):
        data = {
            "diagnoses": [{
                "name": "ACS",
                "prior": 0.25,
                "must_not_miss": True,
                "findings": [{"name": "Troponin+", "lr": 11.0, "present": True}]
            }]
        }
        table = build_table(data)
        assert "Bayesian Probability Table" in table
        assert "ACS" in table
        assert "MUST NOT MISS" in table
        assert "25.0%" in table

    def test_multiple_diagnoses_ranked(self):
        data = {
            "diagnoses": [
                {"name": "Low", "prior": 0.10, "findings": []},
                {"name": "High", "prior": 0.60, "findings": []},
                {"name": "Mid", "prior": 0.30, "findings": []},
            ]
        }
        table = build_table(data)
        lines = table.split("\n")
        summary_lines = [l for l in lines if l.startswith("1.") or l.startswith("2.") or l.startswith("3.")]
        assert "High" in summary_lines[0]
        assert "Mid" in summary_lines[1]
        assert "Low" in summary_lines[2]


class TestCLI:
    """Test the script runs correctly from command line."""

    SCRIPT = os.path.join(os.path.dirname(__file__), "..", ".claude", "skills", "cps", "scripts", "lr_calculator.py")

    def test_stdin_input(self):
        data = json.dumps({
            "diagnoses": [{
                "name": "Test",
                "prior": 0.5,
                "findings": [{"name": "F1", "lr": 2.0, "present": True}]
            }]
        })
        result = subprocess.run(
            [sys.executable, self.SCRIPT],
            input=data, capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "Bayesian Probability Table" in result.stdout

    def test_file_input(self, tmp_path):
        data = {
            "diagnoses": [{
                "name": "Test",
                "prior": 0.5,
                "findings": [{"name": "F1", "lr": 2.0, "present": True}]
            }]
        }
        f = tmp_path / "input.json"
        f.write_text(json.dumps(data))
        result = subprocess.run(
            [sys.executable, self.SCRIPT, "--file", str(f)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "Test" in result.stdout
