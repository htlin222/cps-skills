#!/usr/bin/env python3
"""Write a chapter reference file from stdin to the chapters directory.
Usage: echo "content" | python write_chapter.py ch03-abdominal-pain.md
"""
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python write_chapter.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
output_dir = "/Users/htlin/cps-skills/.claude/skills/cps/references/chapters"
output_path = os.path.join(output_dir, filename)
os.makedirs(output_dir, exist_ok=True)

content = sys.stdin.read()
with open(output_path, 'w') as f:
    f.write(content)

print(f"Written {len(content)} bytes to {output_path}")
