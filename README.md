# PubMed Fetcher

A command-line Python tool to fetch research papers from PubMed that include **non-academic authors** (e.g., from pharmaceutical or biotech companies). The tool filters authors based on affiliation keywords and exports results in CSV format.

---

## 📦 Installation

```bash
git clone https://github.com/yourname/pubmed-fetcher.git
cd pubmed-fetcher
poetry install
```

---

## 🚀 Usage

Basic example (search and output to file):

```bash
poetry run get-papers-list "cancer immunotherapy" -n 50 -f output.csv
```

Debug mode (prints extra info to console):

```bash
poetry run get-papers-list "genome sequencing" --debug
```

---

## ✨ Features

- ✅ Fetches PubMed articles using PubMed E-utilities API.
- ✅ Filters authors with **non-academic affiliations** (e.g., biotech, pharma).
- ✅ Extracts paper metadata including:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Authors
  - Company Affiliations
  - Corresponding Author Email
- ✅ Exports results to a clean CSV file or prints to console.
- ✅ Supports custom query terms and result limits.
- ✅ Command-line interface with help, debug, and file options.
- ✅ Typed Python, modular structure, and Poetry-managed dependencies.

---

## 💠 How to Run

```bash
poetry run get-papers-list "your query here" [-n NUM] [-f filename.csv] [--debug]
```

### CLI Options

| Option           | Description                                  |
| ---------------- | -------------------------------------------- |
| `query`          | PubMed search term (in quotes if multi-word) |
| `-n`, `--number` | Number of papers to fetch (default: 20)      |
| `-f`, `--file`   | Output CSV file name (optional)              |
| `-d`, `--debug`  | Enable debug output (optional)               |
| `-h`, `--help`   | Show help message                            |

---

## 📝 Notes

- The script uses simple heuristics to identify non-academic affiliations by filtering out terms like `university`, `hospital`, etc., and including terms like `pharma`, `biotech`, `inc`, etc.
- You must have an active internet connection to access the PubMed API.
- For larger queries, consider increasing `-n` to fetch more articles.
- All dependencies are managed via [Poetry](https://python-poetry.org/).
- This code is structured for evaluation and automation — outputs are consistent and scriptable.

---

## 🔪 Testing (Optional)

To run tests (if added later):

```bash
pytest
```

---

## 📄 License

MIT © [Unknown]

Unknown

