# pubmed_fetcher/cli.py

import argparse
import csv
import sys
from typing import Optional
from .core import get_papers_with_non_academic_authors


def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with non-academic (pharma/biotech) authors."
    )
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")
    parser.add_argument("-n", "--number", type=int, default=20, help="Number of papers to fetch (default: 20)")
    args = parser.parse_args()

    results = get_papers_with_non_academic_authors(
        query=args.query,
        retmax=args.number,
        debug=args.debug
    )

    if not results:
        print("No papers found with non-academic authors.")
        return

    fieldnames = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    if args.file:
        with open(args.file, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Wrote {len(results)} records to {args.file}")
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
