# Polarion Test Steps Toolkit

# 🚨 READ THIS FIRST (MANDATORY FOR ALL AGENTS)
## Chat interaction logging

At the end of every Claude Code interaction in this repo, write a summary file to the `chat-details/` folder.

**Filename format:** `<JiraID>-YYYY-MM-DD-HH-MM-<concise_summary>.md`
- If a Jira ID is relevant to the session, prefix it (e.g. `OCP-12345-2026-05-01-14-30-redundancy_threshold_tuning.md`).
- If no Jira ID applies, omit it (e.g. `2026-05-01-14-30-initial_repo_setup.md`).
- Use underscores in the summary slug. Keep it to 3-5 words.

**File contents:** A concise Markdown summary including:
- What was discussed or requested
- What changes were made (files touched, features added/fixed)
- Any decisions or open items

## Overview

This is a Python CLI toolkit that fetches test steps from Polarion, generates readable narrative summaries, and detects redundant/overlapping test cases. It is designed for QE engineers working with OpenShift (OCP) test cases in Polarion.

## Architecture

Single entry point (`fetch_teststeps.py`) orchestrates a three-stage pipeline:

1. **Fetch** — Pulls test steps from the Polarion REST API for a list of work item IDs.
2. **Story generation** — Converts structured steps into narrative Markdown paragraphs (`generate_story.py`).
3. **Redundancy analysis** — Compares all work item pairs using text similarity, keyword overlap (Jaccard), and step-level matching (SequenceMatcher), then clusters redundant items via union-find (`analyze_redundancy.py`).

## Files

| File | Role |
|------|------|
| `fetch_teststeps.py` | CLI entry point. Fetches from Polarion API, writes JSON, and delegates to story/analysis modules. |
| `generate_story.py` | Converts step dicts into narrative paragraphs with connectors. Usable standalone or as a library. |
| `analyze_redundancy.py` | Computes pairwise similarity, clusters overlapping work items, and generates a Markdown report with recommendations. |

## Key conventions

- All modules are both importable and runnable standalone via `if __name__ == "__main__"`.
- Verbose/debug output goes to stderr; structured output goes to stdout or files.
- The shared data format is a dict keyed by work item ID (e.g. `{"OCP-12345": {"steps": [...]}}`).
- `_errors` is a reserved key in the output JSON for failed fetches.
- Auth uses a Bearer token via `--token` flag or `POLARION_TOKEN` env var.

## Dependencies

- Python 3.8+
- `requests` (only external dependency)
- Standard library: `json`, `re`, `argparse`, `difflib.SequenceMatcher`

## Running

```bash
python3 fetch_teststeps.py <WORK_ITEM_IDS...> \
  --base-url <POLARION_URL> \
  --project <PROJECT_ID> \
  --token <TOKEN> \
  [--no-verify-ssl] \
  -o output.json \
  --story story.md \
  --analyze report.md \
  --verbose
```

## Testing

No test suite exists yet. To verify changes manually:

1. Run with `--verbose` against a known set of work items and compare output.
2. `generate_story.py` and `analyze_redundancy.py` can be tested standalone with a previously-saved JSON file.

## Common tasks

- **Adding a new similarity metric**: Modify `analyze_redundancy.py`. Add the metric computation in the pair loop (line ~130), incorporate it into the `combined` score formula (line ~154), and surface it in the report table.
- **Changing the report format**: Edit the Markdown generation section at the bottom of `analyze_redundancy.py` (line ~215+).
- **Adding a new pipeline stage**: Follow the pattern in `fetch_teststeps.py` — add a `_write_*` helper and a new CLI flag, then call it from `main()` after the fetch phase.

