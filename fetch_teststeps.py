#!/usr/bin/env python3
"""Fetch test steps from Polarion REST API for given test case work item IDs.

Usage:
    # Fetch live from Polarion (workitem-keyed output by default):
    python3 fetch_teststeps.py OCP-23144 OCP-23143 \
        --base-url https://polarion.engineering.redhat.com \
        --project MyProject \
        --token "$POLARION_TOKEN" \
        --no-verify-ssl \
        -o teststeps_by_workitem.json

    # Flat list output (array of results):
    python3 fetch_teststeps.py OCP-23144 --flat ...

    # Transform an existing results file to workitem-keyed format:
    python3 fetch_teststeps.py --from-file teststeps_casenumbers.txt -o teststeps_by_workitem.json

    # Read token from env var instead of CLI arg:
    export POLARION_TOKEN="your_token"
    python3 fetch_teststeps.py OCP-23144 --base-url ... --project ...
"""

import argparse
import json
import os
import sys
import urllib3
from urllib.parse import quote

import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_teststeps(base_url, project_id, work_item_id, token, verify_ssl):
    url = (
        f"{base_url}/polarion/rest/v1/projects/{quote(project_id)}"
        f"/workitems/{quote(work_item_id)}/teststeps"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    params = {"fields[teststeps]": "@basic"}

    resp = requests.get(url, headers=headers, params=params, verify=verify_ssl)
    resp.raise_for_status()
    return resp.json()


def parse_teststeps(raw_response, work_item_id):
    steps = []
    for item in raw_response.get("data", []):
        attrs = item.get("attributes", {})
        keys = attrs.get("keys", [])
        values = attrs.get("values", [])
        step_dict = {"index": attrs.get("index")}
        for key, val in zip(keys, values):
            step_dict[key] = val.get("value", "") if isinstance(val, dict) else val
        steps.append(step_dict)
    return {"workItemId": work_item_id, "testSteps": steps}


def to_workitem_keyed(results):
    """Convert flat results list to {workItemId: {steps: [...]}} dict."""
    output = {}
    for item in results:
        wid = item["workItemId"]
        output[wid] = {"steps": item.get("testSteps", [])}
    return output


def load_from_file(filepath):
    """Load previously fetched results from a JSON file."""
    with open(filepath) as f:
        data = json.load(f)
    return data.get("results", [])


def main():
    parser = argparse.ArgumentParser(
        description="Fetch test steps from Polarion for given test case IDs."
    )
    parser.add_argument("test_ids", nargs="*", help="Work item IDs (e.g. OCP-23144 OCP-23143)")
    parser.add_argument("--base-url", help="Polarion server URL (e.g. https://polarion.engineering.redhat.com)")
    parser.add_argument("--project", help="Polarion project ID")
    parser.add_argument("--token", help="Personal access token (or set POLARION_TOKEN env var)")
    parser.add_argument("--raw", action="store_true", help="Output raw API responses instead of parsed")
    parser.add_argument("--flat", action="store_true", help="Output flat list instead of workitem-keyed format")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Disable SSL certificate verification")
    parser.add_argument("--output", "-o", help="Write JSON output to file instead of stdout")
    parser.add_argument("--from-file", help="Transform an existing results JSON file instead of fetching from API")
    args = parser.parse_args()

    # -- Mode 1: Transform existing file --
    if args.from_file:
        results = load_from_file(args.from_file)
        if args.flat:
            output = {"results": results}
        else:
            output = to_workitem_keyed(results)
        json_out = json.dumps(output, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w") as f:
                f.write(json_out + "\n")
            print(f"Converted {len(results)} work items -> {args.output}", file=sys.stderr)
        else:
            print(json_out)
        return

    # -- Mode 2: Fetch from Polarion API --
    if not args.test_ids:
        parser.error("test_ids are required when not using --from-file")

    token = args.token or os.environ.get("POLARION_TOKEN")
    if not token:
        parser.error("--token or POLARION_TOKEN env var is required")
    if not args.base_url:
        parser.error("--base-url is required when fetching from API")
    if not args.project:
        parser.error("--project is required when fetching from API")

    base_url = args.base_url.rstrip("/")
    verify_ssl = not args.no_verify_ssl
    results = []
    errors = []

    for wid in args.test_ids:
        try:
            raw = fetch_teststeps(base_url, args.project, wid, token, verify_ssl)
            if args.raw:
                results.append({"workItemId": wid, "response": raw})
            else:
                results.append(parse_teststeps(raw, wid))
        except requests.HTTPError as e:
            errors.append({"workItemId": wid, "error": str(e), "status": e.response.status_code})
        except requests.RequestException as e:
            errors.append({"workItemId": wid, "error": str(e)})

    if args.flat or args.raw:
        output = {"results": results}
        if errors:
            output["errors"] = errors
    else:
        output = to_workitem_keyed(results)
        if errors:
            output["_errors"] = errors

    json_out = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_out + "\n")
        print(f"Fetched {len(results)} work items -> {args.output}", file=sys.stderr)
    else:
        print(json_out)

    if errors:
        print(f"WARNING: {len(errors)} work item(s) failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
