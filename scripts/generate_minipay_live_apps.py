#!/usr/bin/env python3
"""Regenerate skills/celo-copilot/references/minipay-live-apps.md from a discovery export CSV."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 scripts/generate_minipay_live_apps.py /path/to/discover-mini-apps-export.csv",
            file=sys.stderr,
        )
        sys.exit(1)

    csv_path = Path(sys.argv[1]).resolve()
    repo_root = Path(__file__).resolve().parents[1]
    out = repo_root / "skills/celo-copilot/references/minipay-live-apps.md"

    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)

    def pri(x: dict) -> int:
        try:
            return int(x.get("priority") or 0)
        except ValueError:
            return 0

    pub = [r for r in rows if r.get("isPublished", "").lower() == "true"]
    unpub = [r for r in rows if r.get("isPublished", "").lower() != "true"]
    pub.sort(key=pri, reverse=True)
    unpub.sort(key=pri, reverse=True)

    def esc(s: str | None) -> str:
        return (s or "").replace("|", "\\|").replace("\n", " ")

    def country_note(r: dict) -> str:
        w = (r.get("targeting_whitelistedCountries") or "").strip()
        b = (r.get("targeting_blacklistedCountries") or "").strip()
        plat = r.get("targeting_platform", "")
        if w and b:
            ws = w[:80] + ("…" if len(w) > 80 else "")
            bs = b[:60] + ("…" if len(b) > 60 else "")
            return f"Whitelist: {ws}; Blacklist: {bs}"
        if w:
            return f"Countries: {w}" if len(w) < 120 else f"Countries: {w[:117]}…"
        if b:
            return f"Blacklist: {b}" if len(b) < 120 else f"Blacklist: {b[:117]}…"
        if plat and plat != "all":
            return f"Platform: {plat} only"
        return "No country filter in export (not same as worldwide in UI)"

    lines: list[str] = []
    lines.append("# MiniPay live Mini Apps (discovery catalog snapshot)")
    lines.append("")
    lines.append(
        "> **Snapshot source:** Opera MiniPay discovery export (`discover-mini-apps-export.csv`). "
        "**Point-in-time** list so developers can see categories and live-style products in the MiniPay ecosystem."
    )
    lines.append(">")
    lines.append(
        f"> **Last regenerated from export:** {date.today().isoformat()} "
        "(run `python3 scripts/generate_minipay_live_apps.py <csv>` from repo root)."
    )
    lines.append("")
    lines.append("## Important for developers")
    lines.append("")
    lines.append(
        "- **Not all apps are available in all countries.** Targeting uses `targeting_whitelistedCountries` / "
        "`targeting_blacklistedCountries` (ISO 3166-1 alpha-2, pipe `|` separated). An empty field in the export "
        "usually means no filter **in this dataset** — the in-wallet catalog can still differ by region, platform "
        "(Android vs iOS), and Opera rollout."
    )
    lines.append(
        "- **This is not a live API.** The discovery list changes frequently. Re-import the CSV and re-run this script, "
        "or check MiniPay in target markets for ground truth."
    )
    lines.append("- **`isPublished`** reflects the export flag at snapshot time.")
    lines.append("")
    lines.append("## Published listings (snapshot)")
    lines.append("")
    lines.append("| Name | Category | Publisher | Tagline | Link |")
    lines.append("|------|----------|-----------|---------|------|")
    for r in pub:
        link = (r.get("linkUrl") or "").strip()
        lines.append(
            f"| {esc(r.get('name'))} | {esc(r.get('category'))} | {esc(r.get('publisher'))} | "
            f"{esc(r.get('tagline'))} | {link} |"
        )

    lines.append("")
    lines.append("## Country / platform hints (published apps, same priority order)")
    lines.append("")
    lines.append("| Name | Availability note (from export) |")
    lines.append("|------|-----------------------------------|")
    for r in pub:
        note = esc(country_note(r))
        lines.append(f"| {esc(r.get('name'))} | {note} |")

    lines.append("")
    lines.append("## Unpublished in this export (`isPublished: false`)")
    lines.append("")
    for r in unpub:
        lines.append(
            f"- **{esc(r.get('name'))}** ({esc(r.get('category'))}) — {esc(r.get('publisher'))}"
        )

    lines.append("")
    lines.append("## By category (published)")
    lines.append("")
    by_cat: dict[str, list[str]] = defaultdict(list)
    for r in pub:
        by_cat[r.get("category") or "other"].append(r.get("name") or "")
    for cat in sorted(by_cat.keys(), key=str.lower):
        lines.append(f"### {cat}")
        for n in sorted(by_cat[cat], key=str.lower):
            lines.append(f"- {n}")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({len(pub)} published, {len(unpub)} unpublished)")


if __name__ == "__main__":
    main()
