#!/usr/bin/env python3
"""Read and format raw trend reports for a given date. Outputs to stdout."""

import sys
import glob
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 read_reports.py YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    date = sys.argv[1]
    report_dir = "/data/.openclaw/workspace/trend-reports"
    pattern = os.path.join(report_dir, f"{date}_*.txt")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No reports found for {date} in {report_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"# Trend Reports for {date}")
    print(f"# {len(files)} report(s) found\n")

    for f in files:
        basename = os.path.basename(f)
        # Extract query from filename: date_query_words.txt -> query words
        query = basename.replace(f"{date}_", "").replace(".txt", "").replace("_", " ")
        print(f"{'='*60}")
        print(f"## Report: {query}")
        print(f"## File: {basename}")
        print(f"{'='*60}\n")
        with open(f, "r") as fh:
            # Strip ANSI codes
            import re
            content = fh.read()
            content = re.sub(r'\x1b\[[0-9;]*m', '', content)
            print(content)
        print()

if __name__ == "__main__":
    main()
