# Polarion Test Steps Fetcher

Fetch test steps from the Polarion REST API for given test case work item IDs and output them as clean JSON.

## Prerequisites

- Python 3.8+
- `requests` library

```bash
pip install requests
```

## Authentication

Generate a Personal Access Token in Polarion under **My Account > Personal Access Tokens**.

Set it as an environment variable:

```bash
export POLARION_TOKEN="your_token_here"
```

Or pass it directly via `--token`.

## Usage

### Fetch from Polarion API

```bash
python3 fetch_teststeps.py OCP-23144 OCP-23143 OCP-88225 \
    --base-url https://polarion.engineering.redhat.com \
    --project MyProject \
    --no-verify-ssl \
    -o teststeps_by_workitem.json
```

### Transform an existing results file

If you already have a raw results file (flat array format), convert it to workitem-keyed JSON:

```bash
python3 fetch_teststeps.py --from-file teststeps_casenumbers.txt -o teststeps_by_workitem.json
```

### Output to stdout

Omit `-o` to print JSON to the terminal:

```bash
python3 fetch_teststeps.py OCP-23144 \
    --base-url https://polarion.engineering.redhat.com \
    --project MyProject
```

## Options

| Flag | Description |
|---|---|
| `--base-url` | Polarion server URL (required for API fetch) |
| `--project` | Polarion project ID (required for API fetch) |
| `--token` | Personal access token (or use `POLARION_TOKEN` env var) |
| `--from-file` | Transform an existing results JSON file instead of fetching |
| `--flat` | Output as flat array of results instead of workitem-keyed |
| `--raw` | Output raw API responses without parsing |
| `--no-verify-ssl` | Skip SSL certificate verification |
| `-o, --output` | Write output to a file |

## Output Format

Default output is workitem-keyed:

```json
{
  "OCP-23144": {
    "steps": [
      {
        "index": "1",
        "step": "Create remote cluster by running...",
        "expectedResult": ""
      },
      {
        "index": "2",
        "step": "Verify the cluster is ready...",
        "expectedResult": "Cluster status: Ready"
      }
    ]
  },
  "OCP-23143": {
    "steps": [...]
  }
}
```

Use `--flat` to get the original array format:

```json
{
  "results": [
    {
      "workItemId": "OCP-23144",
      "testSteps": [...]
    }
  ]
}
```

## Files

| File | Description |
|---|---|
| `fetch_teststeps.py` | Main script |
| `teststeps_by_workitem.json` | Pre-fetched test steps (43 work items, HTML stripped) |
