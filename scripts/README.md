# Cyberpunk Red: Script Documentation

This directory contains utility scripts for importing and processing content from an Obsidian vault into the Jekyll-based static site.

## Pipeline Overview
The core import process is orchestrated by `import_obsidian.sh`, which cleans the target directories, copies files from the vault, and runs the Python processing suite.

### Core Pipeline Scripts

| Script | Language | Purpose | Usage |
|:---|:---|:---|:---|
| `import_obsidian.sh` | Bash | **Main Entry Point.** Coordinates cleanup, file copying, and execution of the Python suite. | `bash scripts/import_obsidian.sh` |
| `resolve_links.py` | Python | Converts Obsidian `[[Wikilinks]]` into Jekyll-compatible Markdown links. | `python3 scripts/resolve_links.py` |
| `format_corporations.py` | Python | Processes corporation-specific sections like "Discovered Details" into formatted YAML/Markdown. | `python3 scripts/format_corporations.py` |
| `format_players.py` | Python | Formats player stats, skills, and gear into themed grids and tables for character dossiers. | `python3 scripts/format_players.py` |
| `hide_secrets.py` | Python | Filters out `<secret>` tags and GM-only notes from files before they reach production. | `python3 scripts/hide_secrets.py` |
| `parse_corporate_levels.py` | Python | Extracts security/level tables from the vault and generates `_data/corporate_levels.yml`. | `python3 scripts/parse_corporate_levels.py` |

---

### Maintenance & Utility Scripts

| Script | Language | Purpose | Status |
|:---|:---|:---|:---|
| `standardize_lore.py` | Python | **Active.** Normalizes headers, adds front matter, and cleans sub-headers in the source Obsidian vault. | **Active** (Source Maintenance) |
| `generate_pdf.py` | Python | **Active.** Compiles plots, players, corporations, and recaps from the vault into `_plots.pdf` using LibreOffice. | **Active** (Document Compilation) |
| `test_regex.py` | Python | Used for testing and debugging complex regex patterns. | **Obsolete** (Utility/Debug) |

---

## Usage Instructions

1. **Full Reimport**: To perform a complete refresh of the site content from the vault, run:
   ```bash
   bash scripts/import_obsidian.sh
   ```
2. **Lore Standardization**: To clean up formatting specifically in the Obsidian vault's Lore folder:
   ```bash
   python3 scripts/standardize_lore.py
   ```
   *Note: This modifies files in `obsidian_vault/Lore/` directly.*
3. **Generate Campaign Compendium PDF**: To compile all campaign data (plots, players, corporations, session recaps) into a single unified `_plots.pdf` document:
   ```bash
   python3 scripts/generate_pdf.py
   ```

## Maintenance Rules
- **Do not delete obsolete scripts**: Keep them for reference or potential future use.
- **Update this README**: Whenever a new script is added or the pipeline logic changes, ensure this document is updated.
