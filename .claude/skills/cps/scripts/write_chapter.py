#!/usr/bin/env python3
"""Write a chapter reference file from stdin to the chapters directory.
Usage: echo "content" | python write_chapter.py ch03-abdominal-pain.md
"""
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python write_chapter.py <filename>")
    sys.exit(1)

# 输出目录随脚本走（旧版硬编码上游作者的个人绝对路径，换机即失效/误写）。
output_dir = Path(__file__).resolve().parents[1] / "references" / "chapters"
output_path = (output_dir / sys.argv[1]).resolve()
# 文件名防越界：解析后必须仍落在 chapters/ 内，拒绝 ../ 之类。
if output_path.parent != output_dir.resolve():
    print(f"Error: filename must be a plain file name inside {output_dir}", file=sys.stderr)
    sys.exit(1)
output_dir.mkdir(parents=True, exist_ok=True)

content = sys.stdin.read()
output_path.write_text(content, encoding="utf-8")

print(f"Written {len(content)} bytes to {output_path}")
