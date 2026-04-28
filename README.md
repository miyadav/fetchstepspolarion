# Polarion Test Steps Toolkit

Fetch test steps from Polarion, generate readable narratives, and detect redundant work items — in one command.

## Prerequisites

- Python 3.8+
- `pip install requests`
- Polarion personal access token (`--token` or `POLARION_TOKEN` env var)

## Usage

```bash
python3 fetch_teststeps.py <WORK_ITEM_IDS...> \
  --base-url <POLARION_BASE_URL> \
  --project <PROJECT_ID> \
  --token <TOKEN> \
  [--no-verify-ssl] \
  -o <OUTPUT_JSON_FILE> \
  --story <STORY_MARKDOWN_FILE> \
  --analyze <REDUNDANCY_REPORT_FILE> \
  [--verbose]
```

## Example

```bash
python3 fetch_teststeps.py \
  OCP-23144 OCP-23143 OCP-88225 \
  --base-url https://polarion.engineering.redhat.com \
  --project OSE \
  --token $TOKEN \
  --no-verify-ssl \
  -o teststeps_by_workitem.json \
  --story teststeps_story.md \
  --analyze redundancy_report.md \
  --verbose
```

This fetches steps for all listed work items, saves structured JSON, generates a story narrative per work item, and produces a redundancy report showing which test cases overlap and could be consolidated.

## What Each Flag Does

| Flag | Output | Description |
|------|--------|-------------|
| `-o` | `.json` | Structured test steps keyed by work item ID |
| `--story` | `.md` | Each work item's steps as a readable narrative paragraph |
| `--analyze` | `.md` | Redundancy clusters, similarity scores, and merge recommendations |
| `--verbose` | stderr | Step-by-step progress for fetch, story, and analysis phases |

## Sample Redundancy Report

The `--analyze` flag produces a report like this:

```
# Test Steps Redundancy Analysis Report

- Work items analyzed: 42
- Similar pairs found: 9
- Redundancy clusters: 3
- Unique (no overlap): 33

## Redundancy Clusters

### Cluster 1: OCP-23144, OCP-23143, OCP-23017
  - OCP-23144 (6 steps): Create remote cluster by running...
  - OCP-23143 (8 steps): Create cluster deployment...
  - OCP-23017 (2 steps): Create cluster deployment with overriden CLUSTER_IMAGE_SET...

### Cluster 2: OCP-88225, OCP-88193, OCP-84265
  - OCP-88225 (9 steps): Create a vSphere CD with the following...
  - OCP-88193 (8 steps): CD with multi-zones + zoneType=HostGroup...
  - OCP-84265 (48 steps): Test with the old format in CD.spec.platform.vsphere...

## Detailed Pair Analysis

### 1. OCP-88225 vs OCP-88193

| Metric        | Score              |
|---------------|--------------------|
| Combined      | 48.8%              |
| Text          | 8.7%               |
| Keywords      | 43.1%              |
| Step-level    | 88.9% (8/8 steps)  |

Verdict: HIGH — strong candidate to merge or remove one

Matched steps (OCP-88225 -> OCP-88193):
- Step 1 (67%): Create a vSphere CD with the following:Install-config(No TP)...
  matches Step 2: Create a vSphere CD with the following: Install-config(w/ TP)...
- Step 3 (99%): Test default worker MP with the following steps: replicas 3 -> 4...
  matches Step 3: Test default worker MP with the following steps:replicas 3 -> 4...
- Step 4 (89%): Create infra1 MP and test scale up, autoscaling configuration...
  matches Step 4: Create infra1 MP and test scale up, autoscaling configuration...

## Recommendations

### Merge or Remove (HIGH similarity)
- OCP-88225 and OCP-88193 (49% similar): OCP-88193 is a subset of OCP-88225
- OCP-23144 and OCP-23143 (46% similar): OCP-23144 is a subset of OCP-23143
- OCP-52465 and OCP-51797 (44% similar): OCP-51797 is a subset of OCP-52465

### Review for Partial Consolidation (MEDIUM similarity)
- OCP-88193 and OCP-84265 (37% similar): overlapping setup/verification steps
- OCP-51797 and OCP-23101 (33% similar): overlapping setup/verification steps

### No Action Needed
33 work items show no significant overlap and should be kept as-is.
```

## Files

```
fetch_teststeps.py       # Main entry point — fetch, story, and analysis pipeline
generate_story.py        # Converts steps into narrative paragraphs
analyze_redundancy.py    # Detects duplicate/similar work items
```

## Ideas for Enhancement

- Smarter similarity using TF-IDF or sentence embeddings
- HTML/PDF export for the redundancy report
- Interactive mode to confirm and apply merge/remove recommendations
- CI integration to flag new test cases that duplicate existing ones
- Auto-extract shared setup steps into reusable preconditions
- Polarion write-back to archive redundant work items
- Side-by-side diff view of matched steps

Contributions and feedback welcome — open an issue or a PR.
