#!/usr/bin/env python3
"""Extract chapter text from an epub file and convert HTML to readable markdown-ish text."""

import argparse
import zipfile
import sys
from html.parser import HTMLParser

CHAPTER_FILES = {
    1: ["text/part0007.html"],
    2: ["text/part0008.html"],
    3: ["text/part0009.html"],
    4: ["text/part0010.html"],
    5: ["text/part0011_split_000.html", "text/part0011_split_001.html", "text/part0011_split_002.html"],
    6: ["text/part0012.html"],
    7: ["text/part0013.html"],
    8: ["text/part0014.html"],
    9: ["text/part0015.html"],
    10: ["text/part0016.html"],
    11: ["text/part0017.html"],
    12: ["text/part0018.html"],
    13: ["text/part0019.html"],
    14: ["text/part0020.html"],
    15: ["text/part0021.html"],
    16: ["text/part0022.html"],
    17: ["text/part0023.html"],
    18: ["text/part0024.html"],
    19: ["text/part0025.html"],
    20: ["text/part0026.html"],
    21: ["text/part0027.html"],
    22: ["text/part0028.html"],
    23: ["text/part0029.html"],
    24: ["text/part0030.html"],
    25: ["text/part0031.html"],
    26: ["text/part0032.html"],
    27: ["text/part0033.html"],
    28: ["text/part0034.html"],
    29: ["text/part0035.html"],
    30: ["text/part0036.html"],
    31: ["text/part0037.html"],
    32: ["text/part0038.html"],
    33: ["text/part0039.html"],
}

CHAPTER_TITLES = {
    1: "Diagnostic Process",
    2: "Screening and Health Maintenance",
    3: "Abdominal Pain",
    4: "Acid-Base Abnormalities",
    5: "AIDS/HIV",
    6: "Anemia",
    7: "Back Pain",
    8: "Bleeding Disorders",
    9: "Chest Pain",
    10: "Cough, Fever, and Respiratory Infections",
    11: "Delirium and Dementia",
    12: "Diabetes",
    13: "Diarrhea, Acute",
    14: "Dizziness",
    15: "Dyspnea",
    16: "Dysuria",
    17: "Edema",
    18: "Fatigue",
    19: "GI Bleeding",
    20: "Headache",
    21: "Hematuria",
    22: "Hypercalcemia",
    23: "Hypertension",
    24: "Hyponatremia and Hypernatremia",
    25: "Hypotension",
    26: "Jaundice and Abnormal Liver Enzymes",
    27: "Joint Pain",
    28: "Kidney Injury, Acute",
    29: "Rash",
    30: "Sore Throat",
    31: "Syncope",
    32: "Unintentional Weight Loss",
    33: "Wheezing and Stridor",
}


class HTMLToMarkdown(HTMLParser):
    """Convert HTML to markdown-ish text."""

    def __init__(self):
        super().__init__()
        self.output = []
        self.tag_stack = []
        self._in_table = False
        self._row_cells = []
        self._table_rows = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        self.tag_stack.append(tag)

        if tag in ("h1", "h2", "h3"):
            level = int(tag[1])
            self.output.append("\n" + "#" * level + " ")
        elif tag in ("b", "strong"):
            self.output.append("**")
        elif tag in ("i", "em"):
            self.output.append("*")
        elif tag == "li":
            self.output.append("\n- ")
        elif tag == "p":
            self.output.append("\n\n")
        elif tag == "br":
            self.output.append("\n")
        elif tag == "table":
            self._in_table = True
            self._table_rows = []
        elif tag == "tr":
            self._row_cells = []
        elif tag in ("td", "th"):
            pass  # text collected in handle_data
        elif tag in ("ul", "ol"):
            self.output.append("\n")
        elif tag in ("script", "style"):
            self._skip = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        if tag in ("h1", "h2", "h3"):
            self.output.append("\n")
        elif tag in ("b", "strong"):
            self.output.append("**")
        elif tag in ("i", "em"):
            self.output.append("*")
        elif tag in ("td", "th"):
            # Collect text since last cell boundary
            cell_text = self._collect_cell_text()
            self._row_cells.append(cell_text.strip())
        elif tag == "tr":
            if self._row_cells:
                self._table_rows.append(self._row_cells)
            self._row_cells = []
        elif tag == "table":
            self._in_table = False
            self._flush_table()
        elif tag in ("ul", "ol"):
            self.output.append("\n")
        elif tag in ("script", "style"):
            self._skip = False

    def _collect_cell_text(self):
        """Walk back through output to find text for the current cell."""
        # Collect all text fragments added during this cell
        parts = []
        while self.output and not isinstance(self.output[-1], tuple):
            parts.append(self.output.pop())
        parts.reverse()
        return "".join(parts)

    def _flush_table(self):
        """Render collected table rows as a pipe table."""
        if not self._table_rows:
            return
        # Determine column count
        max_cols = max(len(row) for row in self._table_rows)
        self.output.append("\n\n")
        for i, row in enumerate(self._table_rows):
            # Pad row to max_cols
            while len(row) < max_cols:
                row.append("")
            line = "| " + " | ".join(row) + " |"
            self.output.append(line + "\n")
            if i == 0:
                sep = "| " + " | ".join("---" for _ in row) + " |"
                self.output.append(sep + "\n")
        self.output.append("\n")
        self._table_rows = []

    def handle_data(self, data):
        if self._skip:
            return
        self.output.append(data)

    def handle_entityref(self, name):
        entities = {
            "amp": "&", "lt": "<", "gt": ">", "quot": '"',
            "apos": "'", "nbsp": " ", "ndash": "-", "mdash": "--",
            "lsquo": "\u2018", "rsquo": "\u2019",
            "ldquo": "\u201c", "rdquo": "\u201d",
        }
        self.output.append(entities.get(name, f"&{name};"))

    def handle_charref(self, name):
        try:
            if name.startswith("x"):
                char = chr(int(name[1:], 16))
            else:
                char = chr(int(name))
            self.output.append(char)
        except (ValueError, OverflowError):
            self.output.append(f"&#{name};")

    def get_text(self):
        text = "".join(self.output)
        # Clean up excessive blank lines
        lines = text.split("\n")
        cleaned = []
        prev_blank = False
        for line in lines:
            is_blank = line.strip() == ""
            if is_blank and prev_blank:
                continue
            cleaned.append(line)
            prev_blank = is_blank
        return "\n".join(cleaned).strip()


def extract_chapter(epub_path, chapter_num):
    """Extract and convert a single chapter from the epub."""
    if chapter_num not in CHAPTER_FILES:
        print(f"Error: Chapter {chapter_num} not found. Valid: 1-33", file=sys.stderr)
        sys.exit(1)

    files = CHAPTER_FILES[chapter_num]
    title = CHAPTER_TITLES[chapter_num]

    html_parts = []
    with zipfile.ZipFile(epub_path, "r") as zf:
        for fname in files:
            # Try with and without leading paths
            candidates = [fname, "OEBPS/" + fname, "OPS/" + fname]
            found = False
            for candidate in candidates:
                if candidate in zf.namelist():
                    html_parts.append(zf.read(candidate).decode("utf-8", errors="replace"))
                    found = True
                    break
            if not found:
                # Try matching just the filename
                basename = fname.split("/")[-1]
                for name in zf.namelist():
                    if name.endswith(basename):
                        html_parts.append(zf.read(name).decode("utf-8", errors="replace"))
                        found = True
                        break
            if not found:
                print(f"Warning: File '{fname}' not found in epub", file=sys.stderr)

    if not html_parts:
        print(f"Error: No content found for chapter {chapter_num}", file=sys.stderr)
        sys.exit(1)

    combined_html = "\n".join(html_parts)
    converter = HTMLToMarkdown()
    converter.feed(combined_html)
    text = converter.get_text()

    return f"# Chapter {chapter_num}: {title}\n\n{text}"


def main():
    parser = argparse.ArgumentParser(
        description="Extract chapter text from an epub file and convert to markdown."
    )
    parser.add_argument(
        "chapters", type=int, nargs="+",
        help="Chapter numbers to extract (1-33)"
    )
    parser.add_argument(
        "--epub", default="docs/source.epub",
        help="Path to epub file (default: docs/source.epub)"
    )
    args = parser.parse_args()

    for i, ch in enumerate(args.chapters):
        if i > 0:
            print("\n\n---\n")
        print(extract_chapter(args.epub, ch))


if __name__ == "__main__":
    main()
