#!/usr/bin/env python3
"""Generate narrative paragraphs from workitem-keyed test steps JSON.

Can be used standalone:
    python3 generate_story.py /path/to/teststeps_by_workitem.json -o story.md

Or imported and called from other modules:
    from generate_story import generate_story
    markdown = generate_story(data_dict, verbose=True)
"""

import argparse
import json
import re
import sys


CONNECTORS = [
    "To begin", "Then", "Next", "After that", "Following this",
    "Subsequently", "Continuing on", "Moving forward", "Proceeding further",
    "At this point", "Now", "With that done", "Once complete",
    "In the next step", "Going further", "Building on this",
    "Carrying on", "Advancing to the next phase", "From here",
    "Turning attention to the next action", "Progressing onward",
    "Taking it further", "Stepping forward", "Continuing the process",
]


def _log(msg, verbose):
    if verbose:
        print(msg, file=sys.stderr)


def _clean(text):
    return re.sub(r"\s+", " ", text.strip())


def _build_paragraph(work_item_id, steps):
    sentences = []
    for i, step in enumerate(steps):
        step_text = _clean(step.get("step", ""))
        if not step_text:
            continue
        expected = _clean(step.get("expectedResult", ""))
        connector = CONNECTORS[0] if i == 0 else CONNECTORS[i % len(CONNECTORS)].lower()
        sentence = f"{connector}, {step_text}"
        if expected:
            sentence += f" — the expected outcome is: {expected}"
        sentence += "."
        sentences.append(sentence)
    return " ".join(sentences)


def generate_story(data, verbose=False):
    """Return a Markdown string with one labelled paragraph per work item.

    Parameters
    ----------
    data : dict
        Workitem-keyed dict, e.g. {"OCP-12345": {"steps": [...]}, ...}.
    verbose : bool
        Log per-workitem and per-step detail to stderr.
    """
    sections = []
    total = len(data)
    generated = 0

    for idx, (wid, info) in enumerate(data.items(), 1):
        steps = info.get("steps", [])
        if not steps:
            _log(f"  [{idx}/{total}] {wid}: 0 steps — skipped", verbose)
            continue

        _log(f"  [{idx}/{total}] {wid}: {len(steps)} steps", verbose)
        for si, step in enumerate(steps, 1):
            step_text = _clean(step.get("step", ""))
            preview = step_text[:80] + "..." if len(step_text) > 80 else step_text
            has_expected = bool(_clean(step.get("expectedResult", "")))
            _log(f"           step {si}: {preview}" + (" [+expected]" if has_expected else ""), verbose)

        paragraph = _build_paragraph(wid, steps)
        sections.append(f"**{wid}**\n\n{paragraph}\n")
        generated += 1

    _log(f"  Story generated for {generated}/{total} work items", verbose)
    return "\n---\n\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Generate story paragraphs from test-steps JSON.")
    parser.add_argument("input", help="Path to workitem-keyed JSON file")
    parser.add_argument("--output", "-o", help="Write Markdown to file instead of stdout")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show step-by-step progress")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    md = generate_story(data, verbose=args.verbose)

    if args.output:
        with open(args.output, "w") as f:
            f.write(md + "\n")
        print(f"Generated story for {len(data)} work items -> {args.output}", file=sys.stderr)
    else:
        print(md)


if __name__ == "__main__":
    main()
