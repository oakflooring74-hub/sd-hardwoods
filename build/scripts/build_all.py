"""
Regenerate all 12 site pages from raw-source/ + data/ + chrome/.

Usage:
    python build_all.py

Requires Python 3.10+ (stdlib only, no third-party packages).

This runs each page's build script as a subprocess, in the order below. A few pages
are two-step (an "extract/build" pass that (re)writes data/<page>/*.json or *.html from
raw-source/, followed by an "assemble" pass that reads that data + chrome/ and writes the
final page to the repo root). Most are single-step: they read already-extracted data/ files
directly and assemble in one pass.

Output: writes directly over the repo-root .html files (index.html, about_us.html, etc.) --
the same files that are the live, deployed site. Review with `git diff` before committing.

See build/README.md for full background, the per-page table, and known quirks.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # build/scripts
PAGES = HERE / "pages"
COMMON = HERE / "common"

# (label, [scripts to run in order])
STEPS = [
    ("index (homepage)",              [PAGES / "build_homepage.py"]),
    ("about_us",                      [PAGES / "build_about_us.py"]),
    ("contact_us",                    [PAGES / "build_contact_us.py"]),
    ("videos_of_refinishing_process", [PAGES / "build_videos.py"]),
    ("recent_project_photo_gallery_1", [PAGES / "build_gallery1.py"]),
    ("recent_project_photo_gallery_2", [PAGES / "build_gallery2.py"]),
    ("recent_project_photo_gallery_3 + _4", [COMMON / "build_page.py"]),
    ("recent_project_gallery_5",      [PAGES / "build_gallery5.py"]),
    ("solid_wood_floor_photo_gallery", [PAGES / "build_solidwood.py"]),
    ("deep-cleaning-hardwood-floors-san-diego", [
        PAGES / "build_deep_cleaning.py",
        PAGES / "assemble_deep_cleaning.py",
    ]),
    ("blog", [
        PAGES / "build_blog.py",
        PAGES / "assemble_blog.py",
    ]),
]


def main():
    failures = []
    for label, scripts in STEPS:
        print(f"\n=== {label} ===")
        for script in scripts:
            result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
            print(result.stdout.strip())
            if result.returncode != 0:
                print(result.stderr, file=sys.stderr)
                failures.append((label, script.name))
                break  # don't run the next step in this page's chain if this one failed

    print("\n" + "=" * 60)
    if failures:
        print(f"FAILED: {len(failures)} step(s) did not complete:")
        for label, script in failures:
            print(f"  - {label} ({script})")
        sys.exit(1)
    else:
        print("All 12 pages regenerated successfully.")
        print("Run `git diff` at the repo root to review what changed before committing.")


if __name__ == "__main__":
    main()
