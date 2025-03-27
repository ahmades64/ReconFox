# 🦊 ReconFox

**ReconFox** is a Python-based web crawler focused on discovering potentially vulnerable areas of a target website such as forms, parameterized URLs, JavaScript files, comment fields, and more.

> ⚠️ This tool is only for reconnaissance — it does NOT exploit any vulnerabilities.

## 🔧 Features
- Crawls internal links of a target domain
- Identifies:
  - URLs with query parameters
  - JavaScript files
  - Forms (login, signup, profile edit, etc.)
  - Comment sections
- Outputs all results into a categorized text file

## 🚀 Usage

```bash
python reconfox.py
