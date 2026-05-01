#!/usr/bin/env python3
"""Analyze work item test steps for redundancy and similarity."""

import argparse
import json
import re
import sys
from difflib import SequenceMatcher

sys.path.insert(0, ".")
from generate_story import _build_paragraph, _clean


_STOP_WORDS = frozenset(
    "the a an to and or of in on for is it by with that this from as at be are "
    "was has have can will should not all then next after following subsequently "
    "continuing moving proceeding point now done complete step going further "
    "building carrying advancing here turning attention action progressing "
    "taking stepping forward onward process begin outcome expected run".split()
)


def _log(msg, verbose):
    if verbose:
        print(msg, file=sys.stderr)


def _normalize(text):
    text = text.lower()
    text = re.sub(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", "", text)
    text = re.sub(r"[a-f0-9]{10,}", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"/[\w/.\-]+", "", text)
    text = re.sub(r"\$\{[^}]+\}", "", text)
    text = re.sub(r'"[^"]{40,}"', "", text)
    text = re.sub(r"apiversion:.*?kind:", "kind:", text)
    text = re.sub(r"[^a-z0-9\s:.\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_keywords(text):
    words = re.findall(r"[a-z][a-z\-]{2,}", text.lower())
    return set(w for w in words if w not in _STOP_WORDS)


def _jaccard(s1, s2):
    if not s1 and not s2:
        return 0
    return len(s1 & s2) / len(s1 | s2)


def _step_similarity(steps_a, steps_b, verbose=False, label=""):
    if not steps_a or not steps_b:
        return 0, 0, []
    norms_a = [_normalize(_clean(s.get("step", ""))) for s in steps_a]
    norms_b = [_normalize(_clean(s.get("step", ""))) for s in steps_b]
    matched_pairs = []
    for idx_a, na in enumerate(norms_a):
        if not na:
            continue
        best_ratio, best_idx = 0, -1
        for idx_b, nb in enumerate(norms_b):
            if not nb:
                continue
            r = SequenceMatcher(None, na, nb).ratio()
            if r > best_ratio:
                best_ratio, best_idx = r, idx_b
        if best_ratio > 0.55:
            matched_pairs.append((idx_a, best_idx, best_ratio))
            _log(f"           step {idx_a+1} -> step {best_idx+1}  sim={best_ratio:.0%}", verbose)
    valid_a = [x for x in norms_a if x]
    coverage = len(matched_pairs) / len(valid_a) if valid_a else 0
    return len(matched_pairs), coverage, matched_pairs


def _describe_group(group_wids, data):
    lines = []
    for wid in group_wids:
        steps = data[wid].get("steps", [])
        first_step = _clean(steps[0].get("step", "")) if steps else ""
        if len(first_step) > 100:
            first_step = first_step[:100] + "..."
        lines.append(f"  - **{wid}** ({len(steps)} steps): {first_step}")
    return "\n".join(lines)


def analyze_redundancy(data, similarity_threshold=0.25, verbose=False):
    paragraphs = {}
    keywords = {}

    _log("  Phase 1: Building normalized paragraphs and keywords ...", verbose)
    for wid, info in data.items():
        steps = info.get("steps", [])
        if not steps:
            _log(f"    {wid}: 0 steps — skipped", verbose)
            continue
        para = _build_paragraph(wid, steps)
        norm = _normalize(para)
        kw = _extract_keywords(norm)
        paragraphs[wid] = norm
        keywords[wid] = kw
        _log(f"    {wid}: {len(steps)} steps, {len(kw)} keywords", verbose)

    wids = list(paragraphs.keys())
    total_pairs = len(wids) * (len(wids) - 1) // 2
    _log(f"\n  Phase 2: Comparing {total_pairs} pairs across {len(wids)} work items ...", verbose)

    pairs = []
    compared = 0
    for i in range(len(wids)):
        for j in range(i + 1, len(wids)):
            w1, w2 = wids[i], wids[j]
            compared += 1
            text_sim = SequenceMatcher(None, paragraphs[w1], paragraphs[w2]).ratio()
            kw_sim = _jaccard(keywords[w1], keywords[w2])

            # Skip pairs that can't reach threshold even with perfect step match
            if 0.30 * text_sim + 0.35 * kw_sim + 0.35 * 1.0 < similarity_threshold:
                continue

            steps_a = data[w1].get("steps", [])
            steps_b = data[w2].get("steps", [])

            show_detail = verbose and (kw_sim > 0.15 or text_sim > 0.03)
            if show_detail:
                _log(f"\n    [{compared}/{total_pairs}] {w1} vs {w2}  text={text_sim:.1%} kw={kw_sim:.1%}", verbose)

            m_ab, c_ab, pairs_ab = _step_similarity(steps_a, steps_b, verbose=show_detail)
            m_ba, c_ba, pairs_ba = _step_similarity(steps_b, steps_a)
            step_sim = max(c_ab, c_ba)
            combined = 0.30 * text_sim + 0.35 * kw_sim + 0.35 * step_sim

            if show_detail:
                _log(f"         step_sim={step_sim:.1%}  combined={combined:.1%}"
                     + (" ** FLAGGED **" if combined >= similarity_threshold else " (below threshold)"), verbose)

            if combined >= similarity_threshold:
                if c_ab >= c_ba:
                    matched_steps = pairs_ab
                    direction = f"{w1} -> {w2}"
                else:
                    matched_steps = pairs_ba
                    direction = f"{w2} -> {w1}"
                pairs.append({
                    "w1": w1, "w2": w2,
                    "combined": combined,
                    "text_sim": text_sim,
                    "kw_sim": kw_sim,
                    "step_sim": step_sim,
                    "step_matches_count": max(m_ab, m_ba),
                    "steps_a": len(steps_a),
                    "steps_b": len(steps_b),
                    "matched_steps": matched_steps,
                    "direction": direction,
                })
    pairs.sort(key=lambda x: -x["combined"])

    _log(f"\n  Phase 3: Clustering {len(pairs)} flagged pairs ...", verbose)

    # Build groups via union-find
    parent = {w: w for w in wids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for p in pairs:
        union(p["w1"], p["w2"])

    groups = {}
    for w in wids:
        r = find(w)
        groups.setdefault(r, []).append(w)
    cluster_groups = {r: members for r, members in groups.items() if len(members) > 1}

    for ci, (root, members) in enumerate(cluster_groups.items(), 1):
        _log(f"    Cluster {ci}: {', '.join(members)}", verbose)

    unique_count = sum(1 for m in groups.values() if len(m) == 1)
    _log(f"    Unique work items (no overlap): {unique_count}", verbose)

    _log(f"\n  Phase 4: Generating report ...", verbose)

    lines = []
    lines.append("# Test Steps Redundancy Analysis Report")
    lines.append("")
    lines.append(f"- **Work items analyzed:** {len(wids)}")
    lines.append(f"- **Similar pairs found:** {len(pairs)}")
    lines.append(f"- **Redundancy clusters:** {len(cluster_groups)}")
    lines.append(f"- **Unique (no overlap):** {unique_count}")
    lines.append("")

    # Clusters
    lines.append("---")
    lines.append("")
    lines.append("## Redundancy Clusters")
    lines.append("")
    lines.append("Work items grouped together share significant step overlap and could")
    lines.append("potentially be consolidated or have one removed.")
    lines.append("")

    for ci, (root, members) in enumerate(cluster_groups.items(), 1):
        lines.append(f"### Cluster {ci}: {', '.join(members)}")
        lines.append("")
        lines.append(_describe_group(members, data))
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Detailed Pair Analysis")
    lines.append("")
    lines.append("Pairs ranked by combined similarity score (text + keyword + step-level).")
    lines.append("")

    HIGH, MED = 0.40, 0.30

    for rank, p in enumerate(pairs, 1):
        score = p["combined"]
        if score >= HIGH:
            verdict = "HIGH — strong candidate to merge or remove one"
        elif score >= MED:
            verdict = "MEDIUM — review for partial overlap"
        else:
            verdict = "LOW — minor overlap, likely distinct"

        lines.append(f"### {rank}. {p['w1']} vs {p['w2']}")
        lines.append("")
        lines.append(f"| Metric | Score |")
        lines.append(f"|--------|-------|")
        lines.append(f"| **Combined** | **{score:.1%}** |")
        lines.append(f"| Text similarity | {p['text_sim']:.1%} |")
        lines.append(f"| Keyword overlap | {p['kw_sim']:.1%} |")
        lines.append(f"| Step-level match | {p['step_sim']:.1%} ({p['step_matches_count']}/{min(p['steps_a'], p['steps_b'])} steps) |")
        lines.append(f"")
        lines.append(f"**Verdict:** {verdict}")
        lines.append("")

        if p["matched_steps"]:
            src_wid = p["direction"].split(" -> ")[0]
            dst_wid = p["direction"].split(" -> ")[1]
            src_steps = data[src_wid].get("steps", [])
            dst_steps = data[dst_wid].get("steps", [])
            lines.append(f"**Matched steps ({src_wid} -> {dst_wid}):**")
            lines.append("")
            for idx_a, idx_b, ratio in p["matched_steps"]:
                sa = _clean(src_steps[idx_a].get("step", ""))[:80]
                sb = _clean(dst_steps[idx_b].get("step", ""))[:80]
                lines.append(f"- Step {idx_a+1} ({ratio:.0%}): `{sa}...`")
                lines.append(f"  matches Step {idx_b+1}: `{sb}...`")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")

    high_pairs = [p for p in pairs if p["combined"] >= HIGH]
    med_pairs = [p for p in pairs if MED <= p["combined"] < HIGH]

    if high_pairs:
        lines.append("### Merge or Remove (HIGH similarity)")
        lines.append("")
        for p in high_pairs:
            smaller = p["w1"] if p["steps_a"] <= p["steps_b"] else p["w2"]
            larger = p["w2"] if smaller == p["w1"] else p["w1"]
            lines.append(
                f"- **{p['w1']}** and **{p['w2']}** ({p['combined']:.0%} similar): "
                f"`{smaller}` is a subset of `{larger}` — consider removing `{smaller}` "
                f"or merging its unique steps into `{larger}`."
            )
        lines.append("")

    if med_pairs:
        lines.append("### Review for Partial Consolidation (MEDIUM similarity)")
        lines.append("")
        for p in med_pairs:
            lines.append(
                f"- **{p['w1']}** and **{p['w2']}** ({p['combined']:.0%} similar): "
                f"share overlapping setup/verification steps — extract shared steps "
                f"into a common precondition or reference one from the other."
            )
        lines.append("")

    lines.append(f"### No Action Needed")
    lines.append("")
    lines.append(
        f"{unique_count} work items show no significant overlap with any other "
        f"and should be kept as-is."
    )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze test step redundancy across work items.")
    parser.add_argument("input", help="Path to workitem-keyed JSON file")
    parser.add_argument("--output", "-o", help="Write report to file instead of stdout")
    parser.add_argument("--threshold", type=float, default=0.25, help="Minimum combined similarity (default 0.25)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed comparison progress")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    report = analyze_redundancy(data, args.threshold, verbose=args.verbose)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report + "\n")
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
