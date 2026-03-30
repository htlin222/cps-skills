#!/usr/bin/env python3
"""
Distill raw chapter extracts into focused clinical reference files.
Extracts: LR values, differential diagnoses, diagnostic algorithms, clinical pearls.
Strips: case narratives, treatment details, lengthy disease descriptions.

Usage: python distill_chapters.py /tmp/cps_raw_ch{N}.md [output_dir]
       python distill_chapters.py --all [output_dir]
"""
import argparse
import re
import os
import sys

CHAPTER_META = {
    1: ("Diagnostic Process", "diagnostic-process"),
    2: ("Screening and Health Maintenance", "screening"),
    3: ("Abdominal Pain", "abdominal-pain"),
    4: ("Acid-Base Abnormalities", "acid-base"),
    5: ("AIDS/HIV Infection", "hiv-aids"),
    6: ("Anemia", "anemia"),
    7: ("Back Pain", "back-pain"),
    8: ("Bleeding Disorders", "bleeding-disorders"),
    9: ("Chest Pain", "chest-pain"),
    10: ("Cough, Fever, and Respiratory Infections", "cough-fever-respiratory"),
    11: ("Delirium and Dementia", "delirium-dementia"),
    12: ("Diabetes", "diabetes"),
    13: ("Diarrhea, Acute", "diarrhea-acute"),
    14: ("Dizziness", "dizziness"),
    15: ("Dyspnea", "dyspnea"),
    16: ("Dysuria", "dysuria"),
    17: ("Edema", "edema"),
    18: ("Fatigue", "fatigue"),
    19: ("GI Bleeding", "gi-bleeding"),
    20: ("Headache", "headache"),
    21: ("Hematuria", "hematuria"),
    22: ("Hypercalcemia", "hypercalcemia"),
    23: ("Hypertension", "hypertension"),
    24: ("Hyponatremia and Hypernatremia", "hyponatremia-hypernatremia"),
    25: ("Hypotension", "hypotension"),
    26: ("Jaundice and Abnormal Liver Enzymes", "jaundice"),
    27: ("Joint Pain", "joint-pain"),
    28: ("Kidney Injury, Acute", "aki"),
    29: ("Rash", "rash"),
    30: ("Sore Throat", "sore-throat"),
    31: ("Syncope", "syncope"),
    32: ("Unintentional Weight Loss", "weight-loss"),
    33: ("Wheezing and Stridor", "wheezing-stridor"),
}


def extract_lr_values(text):
    """Extract all likelihood ratio mentions from text."""
    lr_entries = []
    # Patterns: LR+ 5.1, LR− 0.3, LR+ of 11, likelihood ratio 5.1
    # Also: sensitivity 90%, specificity 95%
    patterns = [
        r'LR\+?\s*(?:of\s+)?(\d+\.?\d*)',
        r'LR[−–-]\s*(?:of\s+)?(\d+\.?\d*)',
        r'likelihood ratio[^.]*?(\d+\.?\d*)',
        r'sensitivity[^.]*?(\d+\.?\d*)%',
        r'specificity[^.]*?(\d+\.?\d*)%',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            start = max(0, m.start() - 120)
            end = min(len(text), m.end() + 80)
            context = text[start:end].replace('\n', ' ').strip()
            lr_entries.append(context)
    return lr_entries


def extract_sections(text):
    """Extract key sections based on headers and content patterns."""
    sections = {
        'framework': [],
        'diagnoses': [],
        'lr_data': [],
        'algorithm': [],
        'pearls': [],
        'red_flags': [],
    }

    lines = text.split('\n')
    current_section = None
    buffer = []

    for line in lines:
        lower = line.lower().strip()

        # Detect section boundaries
        if any(kw in lower for kw in ['differential diagnosis', 'framework', 'diagnostic approach']):
            if buffer and current_section:
                sections[current_section].extend(buffer)
            current_section = 'framework'
            buffer = [line]
        elif any(kw in lower for kw in ['leading hypothesis', 'disease highlights', 'textbook presentation']):
            if buffer and current_section:
                sections[current_section].extend(buffer)
            current_section = 'diagnoses'
            buffer = [line]
        elif any(kw in lower for kw in ['lr+', 'lr-', 'lr−', 'likelihood ratio', 'sensitivity', 'specificity']):
            sections['lr_data'].append(line)
            if current_section:
                buffer.append(line)
        elif any(kw in lower for kw in ['algorithm', 'diagnostic approach', 'step 1', 'first step']):
            if buffer and current_section:
                sections[current_section].extend(buffer)
            current_section = 'algorithm'
            buffer = [line]
        elif any(kw in lower for kw in ['must not miss', 'red flag', 'alarm', 'dangerous', 'emergenc']):
            sections['red_flags'].append(line)
        elif any(kw in lower for kw in ['pearl', 'key point', 'important', 'remember', 'pitfall', 'fingerprint']):
            sections['pearls'].append(line)
        else:
            if current_section:
                buffer.append(line)

    if buffer and current_section:
        sections[current_section].extend(buffer)

    return sections


def extract_table_rows(text):
    """Extract markdown table rows from text."""
    tables = []
    lines = text.split('\n')
    in_table = False
    current_table = []

    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            in_table = True
            current_table.append(line)
        elif in_table:
            if current_table:
                tables.append('\n'.join(current_table))
            current_table = []
            in_table = False

    if current_table:
        tables.append('\n'.join(current_table))

    return tables


def distill_chapter(chapter_num, raw_text, output_dir):
    """Distill a raw chapter into a focused clinical reference."""
    title, slug = CHAPTER_META[chapter_num]
    filename = f"ch{chapter_num:02d}-{slug}.md"
    output_path = os.path.join(output_dir, filename)

    # Extract LR contexts
    lr_contexts = extract_lr_values(raw_text)

    # Extract key paragraphs containing diagnostic content
    paragraphs = raw_text.split('\n\n')
    diagnostic_paras = []
    lr_paras = []
    algorithm_paras = []
    must_not_miss_paras = []

    for para in paragraphs:
        lower = para.lower()
        if any(kw in lower for kw in ['lr+', 'lr-', 'lr−', 'lr–', 'likelihood ratio',
                                       'sensitivity', 'specificity', 'predictive value']):
            lr_paras.append(para.strip())
        if any(kw in lower for kw in ['differential', 'consider', 'causes include',
                                       'most common cause', 'etiology', 'framework']):
            diagnostic_paras.append(para.strip())
        if any(kw in lower for kw in ['algorithm', 'approach', 'first step', 'next step',
                                       'pivotal', 'distinguish', 'classify']):
            algorithm_paras.append(para.strip())
        if any(kw in lower for kw in ['must not miss', 'red flag', 'alarm', 'life-threatening',
                                       'emergent', 'urgent', 'dangerous']):
            must_not_miss_paras.append(para.strip())

    # Build output
    output_lines = [f"# Ch{chapter_num}: {title}", ""]

    # Framework section
    output_lines.append("## Differential Diagnosis Framework")
    framework_text = '\n\n'.join(diagnostic_paras[:3]) if diagnostic_paras else "See textbook for detailed framework."
    # Truncate to reasonable length
    if len(framework_text) > 1500:
        framework_text = framework_text[:1500] + "..."
    output_lines.append(framework_text)
    output_lines.append("")

    # LR section - the most valuable data
    output_lines.append("## Pivotal Findings & Likelihood Ratios")
    output_lines.append("")
    if lr_paras:
        # Deduplicate and limit
        seen = set()
        for para in lr_paras:
            short = para[:80]
            if short not in seen:
                seen.add(short)
                output_lines.append(para)
                output_lines.append("")
            if len(seen) > 25:
                break
    elif lr_contexts:
        output_lines.append("Extracted LR contexts from text:")
        output_lines.append("")
        seen = set()
        for ctx in lr_contexts:
            short = ctx[:60]
            if short not in seen:
                seen.add(short)
                output_lines.append(f"- {ctx}")
            if len(seen) > 20:
                break
        output_lines.append("")
    else:
        output_lines.append("No explicit LR values found in this chapter. See bayesian-reasoning.md for common LRs.")
        output_lines.append("")

    # Algorithm section
    output_lines.append("## Diagnostic Algorithm")
    algo_text = '\n\n'.join(algorithm_paras[:3]) if algorithm_paras else "See textbook for diagnostic algorithm."
    if len(algo_text) > 1500:
        algo_text = algo_text[:1500] + "..."
    output_lines.append(algo_text)
    output_lines.append("")

    # Red flags
    output_lines.append("## Red Flags (Must-Not-Miss)")
    if must_not_miss_paras:
        for para in must_not_miss_paras[:5]:
            if len(para) > 500:
                para = para[:500] + "..."
            output_lines.append(f"- {para}")
    else:
        output_lines.append("- See ddx-framework.md for must-not-miss diagnoses by symptom category")
    output_lines.append("")

    # Write file
    content = '\n'.join(output_lines)
    with open(output_path, 'w') as f:
        f.write(content)

    line_count = len(output_lines)
    print(f"  ch{chapter_num:02d}-{slug}.md: {line_count} lines")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Distill raw chapter extracts into clinical references")
    parser.add_argument('--all', action='store_true', help='Process all 33 chapters from /tmp/cps_raw_ch*.md')
    parser.add_argument('input', nargs='?', help='Path to raw chapter file')
    parser.add_argument('--output-dir', default='/Users/htlin/cps-skills/.claude/skills/cps/references/chapters',
                        help='Output directory')
    parser.add_argument('--chapter', type=int, help='Chapter number (auto-detected from filename if omitted)')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    if args.all:
        print(f"Distilling all 33 chapters to {args.output_dir}/")
        for ch_num in range(1, 34):
            raw_path = f"/tmp/cps_raw_ch{ch_num}.md"
            if not os.path.exists(raw_path):
                print(f"  SKIP ch{ch_num:02d}: {raw_path} not found")
                continue
            with open(raw_path) as f:
                raw_text = f.read()
            distill_chapter(ch_num, raw_text, args.output_dir)
        print("Done.")
    elif args.input:
        with open(args.input) as f:
            raw_text = f.read()
        ch_num = args.chapter
        if ch_num is None:
            m = re.search(r'ch(\d+)', args.input)
            if m:
                ch_num = int(m.group(1))
            else:
                print("Error: cannot detect chapter number. Use --chapter N")
                sys.exit(1)
        distill_chapter(ch_num, raw_text, args.output_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
