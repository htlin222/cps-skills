"""Tests for case directory initialization."""
import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(__file__), "..", ".claude", "skills", "cps", "scripts", "init_case.py")


class TestInitCase:
    """init_case.py should create a complete case directory structure."""

    def test_creates_all_files(self, tmp_path):
        scenario = tmp_path / "SCENARIO.md"
        scenario.write_text("# Test Case\n## Chief Complaint\nChest pain\n")
        base = tmp_path / "cases"

        result = subprocess.run(
            [sys.executable, SCRIPT, "test-slug", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        assert result.returncode == 0

        case_dir = base / "test-slug"
        assert case_dir.is_dir()
        assert (case_dir / "SCENARIO.md").is_file()
        assert (case_dir / "FINAL_DX.md").is_file()
        assert (case_dir / "probability-table.md").is_file()
        assert (case_dir / "VALIDATION.md").is_file()
        assert (case_dir / "PERFORMANCE.md").is_file()
        for i in range(1, 6):
            assert (case_dir / f"round-{i}.md").is_file()

    def test_round_headers_correct(self, tmp_path):
        scenario = tmp_path / "SCENARIO.md"
        scenario.write_text("# Test\n")
        base = tmp_path / "cases"

        subprocess.run(
            [sys.executable, SCRIPT, "test-headers", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        case_dir = base / "test-headers"

        assert "Attending" in (case_dir / "round-1.md").read_text()
        assert "Radiology" in (case_dir / "round-2.md").read_text()
        assert "Subspecialty" in (case_dir / "round-3.md").read_text()
        assert "EBM" in (case_dir / "round-4.md").read_text()
        assert "Consensus" in (case_dir / "round-5.md").read_text()

    def test_scenario_copied(self, tmp_path):
        scenario = tmp_path / "input.md"
        scenario.write_text("# My Patient\nSpecific content here\n")
        base = tmp_path / "cases"

        subprocess.run(
            [sys.executable, SCRIPT, "copy-test", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        copied = (base / "copy-test" / "SCENARIO.md").read_text()
        assert "Specific content here" in copied

    def test_same_file_no_error(self, tmp_path):
        """SameFileError fix: when scenario is already at target path."""
        base = tmp_path / "cases"
        case_dir = base / "same-file"
        case_dir.mkdir(parents=True)
        scenario = case_dir / "SCENARIO.md"
        scenario.write_text("# Already here\n")

        result = subprocess.run(
            [sys.executable, SCRIPT, "same-file", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "Already here" in scenario.read_text()

    def test_no_overwrite_existing_round(self, tmp_path):
        """Existing round files with content should NOT be overwritten."""
        base = tmp_path / "cases"
        case_dir = base / "no-overwrite"
        case_dir.mkdir(parents=True)
        scenario = tmp_path / "SCENARIO.md"
        scenario.write_text("# Test\n")

        # Pre-create round-1 with custom content
        round1 = case_dir / "round-1.md"
        round1.write_text("# My existing analysis\nImportant content\n")

        subprocess.run(
            [sys.executable, SCRIPT, "no-overwrite", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        assert "Important content" in round1.read_text()

    def test_overwrites_empty_files(self, tmp_path):
        """Empty round files SHOULD be overwritten with template headers."""
        base = tmp_path / "cases"
        case_dir = base / "empty-overwrite"
        case_dir.mkdir(parents=True)
        scenario = tmp_path / "SCENARIO.md"
        scenario.write_text("# Test\n")

        # Pre-create empty round-1
        (case_dir / "round-1.md").write_text("")

        subprocess.run(
            [sys.executable, SCRIPT, "empty-overwrite", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        assert "Attending" in (case_dir / "round-1.md").read_text()

    def test_missing_scenario_fails(self, tmp_path):
        """Should fail with exit code 1 if scenario file doesn't exist."""
        result = subprocess.run(
            [sys.executable, SCRIPT, "fail-test", "/nonexistent/file.md", "--base-dir", str(tmp_path)],
            capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "not found" in result.stderr

    def test_prints_absolute_path(self, tmp_path):
        scenario = tmp_path / "SCENARIO.md"
        scenario.write_text("# Test\n")
        base = tmp_path / "cases"

        result = subprocess.run(
            [sys.executable, SCRIPT, "path-test", str(scenario), "--base-dir", str(base)],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert os.path.isabs(result.stdout.strip())
