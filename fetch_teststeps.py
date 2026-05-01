#!/usr/bin/env python3
"""Fetch test steps from Polarion, generate story narratives, and analyze redundancy."""

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
    output = {}
    for item in results:
        wid = item["workItemId"]
        output[wid] = {"steps": item.get("testSteps", [])}
    return output


def _log(msg, verbose=False):
    if verbose:
        print(msg, file=sys.stderr)


def _write_story(workitem_data, story_path, verbose=False):
    from generate_story import generate_story
    _log("\n" + "=" * 60, verbose)
    _log("STORY GENERATION", verbose)
    _log("=" * 60, verbose)
    md = generate_story(workitem_data, verbose=verbose)
    with open(story_path, "w") as f:
        f.write(md + "\n")
    print(f"Generated story -> {story_path}", file=sys.stderr)


def _write_redundancy_report(workitem_data, report_path, verbose=False):
    from analyze_redundancy import analyze_redundancy
    _log("\n" + "=" * 60, verbose)
    _log("REDUNDANCY ANALYSIS", verbose)
    _log("=" * 60, verbose)
    report = analyze_redundancy(workitem_data, verbose=verbose)
    with open(report_path, "w") as f:
        f.write(report + "\n")
    print(f"Generated redundancy report -> {report_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch test steps from Polarion, generate stories, and analyze redundancy."
    )
    parser.add_argument("test_ids", nargs="+", help="Work item IDs (e.g. OCP-23144 OCP-23143)")
    parser.add_argument("--base-url", required=True, help="Polarion server URL")
    parser.add_argument("--project", required=True, help="Polarion project ID")
    parser.add_argument("--token", help="Personal access token (or set POLARION_TOKEN env var)")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Disable SSL certificate verification")
    parser.add_argument("--output", "-o", help="Write JSON output to file")
    parser.add_argument("--story", metavar="FILE", help="Generate narrative Markdown story to FILE")
    parser.add_argument("--analyze", metavar="FILE", help="Generate redundancy analysis report to FILE")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed step-by-step progress on stderr")
    args = parser.parse_args()
    verbose = args.verbose

    token = args.token or os.environ.get("POLARION_TOKEN")
    if not token:
        parser.error("--token or POLARION_TOKEN env var is required")

    base_url = args.base_url.rstrip("/")
    verify_ssl = not args.no_verify_ssl
    results = []
    errors = []

    total = len(args.test_ids)
    _log("=" * 60, verbose)
    _log("FETCHING TEST STEPS", verbose)
    _log("=" * 60, verbose)

    for idx, wid in enumerate(args.test_ids, 1):
        _log(f"  [{idx}/{total}] Fetching {wid} ...", verbose)
        try:
            raw = fetch_teststeps(base_url, args.project, wid, token, verify_ssl)
            parsed = parse_teststeps(raw, wid)
            results.append(parsed)
            step_count = len(parsed.get("testSteps", []))
            _log(f"           {step_count} steps fetched", verbose)
            if verbose:
                for si, s in enumerate(parsed.get("testSteps", []), 1):
                    step_text = s.get("step", "")[:80]
                    has_exp = bool(s.get("expectedResult", "").strip())
                    _log(f"           step {si}: {step_text}..." + (" [+expected]" if has_exp else ""), verbose)
        except requests.HTTPError as e:
            errors.append({"workItemId": wid, "error": str(e), "status": e.response.status_code})
            _log(f"           ERROR: {e.response.status_code} {e}", verbose)
        except requests.RequestException as e:
            errors.append({"workItemId": wid, "error": str(e)})
            _log(f"           ERROR: {e}", verbose)

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

    if args.story:
        _write_story(output, args.story, verbose)
    if args.analyze:
        _write_redundancy_report(output, args.analyze, verbose)

    if errors:
        print(f"WARNING: {len(errors)} work item(s) failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
