#!/usr/bin/env python3
"""CI checks for the skills repo: frontmatter, self-containment, template invariants.

Run locally: python3 scripts/check_skills.py
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / "skills"

# Invariants the SKILL.md contracts call out explicitly.
INVARIANTS = {
    "html-report/template.html": [
        # SKILL.md: the scroll-margin rule ships in the template — keep it.
        "scroll-margin-top: 50vh",
    ],
}

EXTERNAL_RESOURCE = re.compile(
    r"""<script\b[^>]*\bsrc=["']https?   # remote script
      | <link\b[^>]*\bhref=["']https?    # remote stylesheet/font/icon
      | @import\s+(?:url\()?["']?https?  # remote @import
      | url\(\s*["']?https?              # remote css url()
      | <iframe\b                        # embedded frame
    """,
    re.VERBOSE | re.IGNORECASE,
)


def fail(errors, path, msg):
    errors.append(f"{path}: {msg}")


def check_skill(skill_dir, errors):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(errors, skill_dir, "missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        fail(errors, skill_md, "frontmatter must start and end with '---' lines")
        return
    front = m.group(1)
    name_m = re.search(r"^name:\s*(\S.*)$", front, re.MULTILINE)
    if not name_m:
        fail(errors, skill_md, "frontmatter needs an inline 'name:' value")
    elif name_m.group(1).strip() != skill_dir.name:
        fail(
            errors,
            skill_md,
            f"'name: {name_m.group(1).strip()}' does not match directory '{skill_dir.name}'",
        )
    if not re.search(r"^description:\s*\S", front, re.MULTILINE):
        fail(errors, skill_md, "frontmatter needs a 'description:'")


def check_html(path, errors):
    html = path.read_text(encoding="utf-8")
    if EXTERNAL_RESOURCE.search(html):
        fail(
            errors,
            path,
            "external script/stylesheet/font/iframe found — page must stay self-contained",
        )
    for expected in INVARIANTS.get(f"{path.parent.name}/{path.name}", []):
        if expected not in html:
            fail(errors, path, f"invariant missing: {expected!r}")


def main():
    errors = []
    if not SKILLS_DIR.is_dir():
        fail(errors, SKILLS_DIR, "no skills/ directory")
    else:
        for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
            check_skill(skill_dir, errors)
            for html in sorted(skill_dir.glob("*.html")):
                check_html(html, errors)
    if errors:
        print("CI check failed:")
        print("\n".join(f"  - {e}" for e in errors))
        return 1
    skills = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir())
    print(f"OK: {len(skills)} skill(s) valid: {', '.join(skills)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
