# -*- coding: utf-8 -*-
"""
Milestone 2.13 ledger + similarity audit generator.

Parses the 13 *generated* root pages (post-build) for every <img> usage, cross-
references each by (page, src) against the Milestone 2.12 ledger
(build/data/image_alt_expansion_ledger.csv) to recover the "previous alt", and
writes build/data/image_alt_recomposition_ledger.csv with one row per image
usage. Also runs the programmatic checks listed in the milestone brief and
writes a similarity report (exact-prefix + semantic near-duplicate) as a
section of docs/2026-07-image-alt-recomposition-report.md's companion data
file, build/data/image_alt_recomposition_similarity.md.

Read-only with respect to every page/source file except its own two outputs.
"""
import csv
import difflib
import io
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DATA = REPO / "build" / "data"
OLD_LEDGER = DATA / "image_alt_expansion_ledger.csv"
NEW_LEDGER = DATA / "image_alt_recomposition_ledger.csv"
SIMILARITY_OUT = DATA / "image_alt_recomposition_similarity.md"

PAGES = [
    ("index.html", "https://www.sdhardwoods.com/"),
    ("about_us.html", "https://www.sdhardwoods.com/about_us.html"),
    ("contact_us.html", "https://www.sdhardwoods.com/contact_us.html"),
    ("floor-assessments-inspections.html", "https://www.sdhardwoods.com/floor-assessments-inspections"),
    ("videos_of_refinishing_process.html", "https://www.sdhardwoods.com/videos_of_refinishing_process.html"),
    ("recent_project_photo_gallery_1.html", "https://www.sdhardwoods.com/recent_project_photo_gallery_1.html"),
    ("recent_project_photo_gallery_2.html", "https://www.sdhardwoods.com/recent_project_photo_gallery_2.html"),
    ("recent_project_photo_gallery_3.html", "https://www.sdhardwoods.com/recent_project_photo_gallery_3.html"),
    ("recent_project_photo_gallery_4.html", "https://www.sdhardwoods.com/recent_project_photo_gallery_4.html"),
    ("recent_project_gallery_5.html", "https://www.sdhardwoods.com/recent_project_gallery_5.html"),
    ("solid_wood_floor_photo_gallery.html", "https://www.sdhardwoods.com/solid_wood_floor_photo_gallery.html"),
    ("deep-cleaning-hardwood-floors-san-diego.html", "https://www.sdhardwoods.com/deep-cleaning-hardwood-floors-san-diego.html"),
    ("blog.html", "https://www.sdhardwoods.com/blog.html"),
]

SOURCE_FILE_BY_PAGE = {
    "index.html": "build/data/index/gallery.json",
    "about_us.html": "build/scripts/pages/build_about_us.py (static literal)",
    "contact_us.html": "n/a (no images)",
    "floor-assessments-inspections.html": "build/scripts/pages/build_floor_assessments.py (static literal)",
    "videos_of_refinishing_process.html": "build/scripts/pages/build_videos.py + build/data/youtube_videos.json",
    "recent_project_photo_gallery_1.html": "build/data/recent_project_photo_gallery_1/modules.json",
    "recent_project_photo_gallery_2.html": "build/data/recent_project_photo_gallery_2/modules.json",
    "recent_project_photo_gallery_3.html": "build/data/recent_project_photo_gallery_3/modules.json",
    "recent_project_photo_gallery_4.html": "build/data/recent_project_photo_gallery_4/modules.json",
    "recent_project_gallery_5.html": "build/data/recent_project_gallery_5/projects.json",
    "solid_wood_floor_photo_gallery.html": "build/data/solid_wood_floor_photo_gallery/images.json + projects.json",
    "deep-cleaning-hardwood-floors-san-diego.html": "build/scripts/pages/assemble_deep_cleaning.py (ALT_OVERRIDE) + gallery_records.json",
    "blog.html": "build/scripts/pages/assemble_blog.py (ALT_OVERRIDE + spam-stripping) + case_studies.json",
}

# Decorative images intentionally left with empty alt (shared chrome, unchanged this milestone).
DECORATIVE_SRC_MARKERS = ("sdh-logo-256.webp", "sdhLightboxImg")

IMG_TAG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')


def parse_imgs(html_text):
    out = []
    for m in IMG_TAG_RE.finditer(html_text):
        tag = m.group(0)
        attrs = dict(ATTR_RE.findall(tag))
        out.append(attrs)
    return out


def load_old_ledger():
    rows = {}
    if not OLD_LEDGER.exists():
        return rows
    with io.open(OLD_LEDGER, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[(r["page_url"], r["image_path"])] = r
    return rows


def classify_role(alt, figcaption_hint=None):
    a = (alt or "").lower()
    if a.startswith("before "):
        return "before"
    if a.startswith("after "):
        return "after"
    if "video thumbnail" in a or "youtube" in a:
        return "video thumbnail"
    if not alt:
        return "decorative/empty"
    return "other"


def project_id(alt):
    m = re.search(r'#(\d+)', alt or "")
    return m.group(1) if m else ""


PAGE_NOTES = {
    "index.html": "Homepage: merged each image's short base sentence with its already-authoritative, reviewer-refined caption (Milestone 2.7), removing the redundant restatement. 4 Bing Crosby Ranch photos (no caption) hand-recomposed to drop internal verification metadata from the alt text.",
    "recent_project_photo_gallery_1.html": "Gallery 1: fixed the confirmed systemic bug -- alt previously led with the shared project title (~250+ identical characters per pair); now leads with Before/After + project number + the genuinely image-specific legacy detail, with project context merged in afterward, deduplicated.",
    "recent_project_photo_gallery_2.html": "Gallery 2: same systemic-bug fix as Gallery 1, applied to the general-case branch only (the idx==8 special Bird Rock/Rancho Santa Fe pair already led correctly and was left unchanged).",
    "recent_project_photo_gallery_3.html": "Gallery 3: audited -- base alt already leads with image-specific content; only the one confirmed byte-identical pair (SUE30/SUE76, Project #50) was recomposed. All other images left unchanged (already compliant).",
    "recent_project_photo_gallery_4.html": "Gallery 4: audited -- base alt already leads with image-specific content; only the two confirmed byte-identical pairs (BEACH1/BEACH4 Project #72; REFINISH LAUZON MAPLE... pair Project #63) were recomposed. All other images left unchanged (already compliant).",
    "recent_project_gallery_5.html": "Gallery 5: audited -- already fully compliant (image-specific content leads, no exact-duplicate prefixes, no self-duplicate sentences). No source change.",
    "solid_wood_floor_photo_gallery.html": "Solid & Engineered: audited -- per-image alt already leads with a real installation-stage progression on all 4 projects. Only Project 1's 4 TRICIA WALNUT27/30/63/76 images (the pre-existing filename-vs-white-oak conflict) had their shared trailing project-heading/note block trimmed, since it was fully redundant with content already stated in the lead. Projects 2-4 left unchanged (already compliant).",
    "deep-cleaning-hardwood-floors-san-diego.html": "Deep Cleaning: recomposed all 20 pairs. Pairs #1-9 are this page's own real projects, recomposed to lead with the visible process stage (not a forced Before/After label -- Pair #1's CSS before/after roles don't reliably match a damaged/completed reading). Pairs #10-20 reuse the exact same source photos as Gallery 1 Projects #10-20 (a pre-existing raw-source duplication across both pages) and reuse that already-recomposed wording verbatim.",
    "blog.html": "Blog: audited -- 39 of 43 images already led with real, image-specific content. 2 images (Case Study #8) had pure ALL-CAPS keyword-spam legacy alt with zero image-specific content; recomposed to lead with the real figcaption fact (before-sanding stage; confirmed red-oak species). A general spam-stripping rule also removes the same boilerplate marker from any other affected image (Case Study #12) as a structural cleanup.",
    "videos_of_refinishing_process.html": "Videos: recomposed all 58 thumbnails -- removed the repeated canned closing template (\"San Diego Hardwoods YouTube video thumbnail showing {category}... uploaded {date}\", identical across up to 38 videos in the same category) in favor of each video's own title + real description alone. 10 thumbnails across all 3 categories additionally hand-composed as a curated, owner-reviewed sample.",
    "about_us.html": "About Us: audited -- single image (LARK56.jpg), no change. Shares its opening sentence with Floor Assessments' use of the same photo -- legitimate reuse of the same real photograph, not a duplicate-content defect.",
    "floor-assessments-inspections.html": "Floor Assessments: audited -- single image (LARK56.jpg), no change. See About Us note re: legitimate cross-page photo reuse.",
    "contact_us.html": "Contact Us: confirmed zero <img> tags on this page.",
}

OWNER_REVIEW_NOTES = {
    ("recent_project_photo_gallery_1.html", "/DOUGLAS FIR REFINISH6.jpg"): "Jacobian/Jacobean spelling conflict (this page vs. homepage data) -- unresolved, flagged.",
    ("recent_project_photo_gallery_1.html", "/DOUGLAS FIR REFINISH14.jpg"): "Jacobian/Jacobean spelling conflict -- unresolved, flagged.",
    ("recent_project_photo_gallery_1.html", "/DOUGLAS FIR REFINISHING1.jpg"): "Jacobian/Jacobean spelling conflict -- unresolved, flagged.",
    ("recent_project_photo_gallery_1.html", "/DOUGLAS FIR REFINISHING16.jpg"): "Jacobian/Jacobean spelling conflict -- unresolved, flagged.",
    ("videos_of_refinishing_process.html", "https://i.ytimg.com/vi/ixqPScnbnLE/hqdefault.jpg"): "Identical title/description/category/publish-date to HF1pRJYTgZk in youtube_videos.json -- genuinely indistinguishable from repo data, likely a duplicate upload. Not invented a difference.",
    ("videos_of_refinishing_process.html", "https://i.ytimg.com/vi/HF1pRJYTgZk/hqdefault.jpg"): "Identical title/description/category/publish-date to ixqPScnbnLE in youtube_videos.json -- genuinely indistinguishable from repo data, likely a duplicate upload. Not invented a difference.",
    ("blog.html", "assets/images/20181228_131405.5202851_std.jpg"): "Case Study #11: empty legacy alt, no distinguishing caption or prose exists in case_studies.json for this image vs. its siblings. Not invented a difference.",
    ("blog.html", "assets/images/20190201_110423.47185639_std.jpg"): "Case Study #11: empty legacy alt, no distinguishing caption or prose exists for this image vs. its siblings. Not invented a difference.",
    ("blog.html", "assets/images/20190201_110134.47185733_std.jpg"): "Case Study #11: empty legacy alt, no distinguishing caption or prose exists for this image vs. its siblings. Not invented a difference.",
    ("blog.html", "assets/images/20190216_105602.56133521_std.jpg"): "Case Study #12: after spam-stripping, this image's remaining legacy alt text is identical to 20190218's; only this one has a distinguishing figcaption (used to lead). Prose-to-image mapping for this case study also doesn't map cleanly 1:1 -- flagged, not guessed.",
    ("blog.html", "assets/images/20190218_104244.56133615_std.jpg"): "Case Study #12: after spam-stripping, this image's remaining legacy alt text is identical to 20190216's, and no distinguishing figcaption exists for this one. Not invented a difference.",
    ("blog.html", "assets/images/20190408_142730.117193948_std.jpg"): "Case Study #12: after spam-stripping, this image's remaining legacy alt text is identical to 20190426's; no distinguishing caption exists for either. Not invented a difference.",
    ("blog.html", "assets/images/20190426_161833.117194035_std.jpg"): "Case Study #12: after spam-stripping, this image's remaining legacy alt text is identical to 20190408's; no distinguishing caption exists for either. Not invented a difference.",
    ("solid_wood_floor_photo_gallery.html", "/TRICIA WALNUT27.jpg"): "Filenames say 'walnut,' all published text (heading/note/alt) says white oak -- pre-existing conflict flagged since Milestone 2.5, deliberately unresolved. Also 'Graff Brothers' here vs. 'Graf Brothers' in homepage's Bird Rock data -- brand-spelling conflict, unresolved.",
    ("solid_wood_floor_photo_gallery.html", "/TRICIA WALNUT30.jpg"): "Same TRICIA WALNUT/white-oak and Graff/Graf conflicts as WALNUT27 -- unresolved, flagged.",
    ("solid_wood_floor_photo_gallery.html", "/TRICIA WALNUT63.jpg"): "Same TRICIA WALNUT/white-oak and Graff/Graf conflicts as WALNUT27 -- unresolved, flagged.",
    ("solid_wood_floor_photo_gallery.html", "/TRICIA WALNUT76.jpg"): "Same TRICIA WALNUT/white-oak and Graff/Graf conflicts as WALNUT27 -- unresolved, flagged.",
    ("index.html", "/KIM BIRD ROCK WHITE OAK88.jpg"): "'Graf Brothers' here vs. 'Graff Brothers' in Solid & Engineered's Project 1 data -- brand-spelling conflict, unresolved.",
    ("recent_project_photo_gallery_4.html", "/ASH24.jpg"): "Project #61: neither this photo nor its pair's own data describes a damaged/pre-refinish state -- both are completed-result descriptions distinguished only by geographic vantage. No before/after claim invented; flagged for owner confirmation of whether a true 'before' photo exists elsewhere for this project.",
    ("recent_project_photo_gallery_4.html", "/ASH37.jpg"): "Project #61: same finding as ASH24 -- no damaged/pre-refinish state exists in the data for either photo of this project.",
    ("recent_project_photo_gallery_1.html", "/FRENCH OAK INSTALL21.jpg"): "Project #12 title says 'Baker's Hill' -- not a known real San Diego neighborhood -- while Projects #8/#9 in the same modules.json correctly say 'Bankers Hill.' Kept as the current wording (not silently corrected); unresolved, flagged.",
    ("recent_project_photo_gallery_1.html", "/FRENCH OAK INSTALL60.jpg"): "Same Baker's Hill/Bankers Hill conflict as FRENCH OAK INSTALL21.jpg -- unresolved, flagged.",
    ("recent_project_photo_gallery_1.html", "/RECOAT OAK6.jpg"): "Project #18's title claims restoration 'without a full sanding' while both this image's alt and its pair's alt describe dust-free/dustless sanding as part of the process -- a real factual contradiction in the source data, preserved as-is rather than silently resolved.",
    ("recent_project_photo_gallery_1.html", "/RECOAT OAK8.jpg"): "Same Project #18 sanding-vs-recoating contradiction as RECOAT OAK6.jpg -- unresolved, flagged.",
}


def main():
    old_ledger = load_old_ledger()
    rows = []
    meaningful_alts = []  # (page, src, alt) for similarity pass

    for fname, page_url in PAGES:
        path = REPO / fname
        if not path.exists():
            continue
        html_text = path.read_text(encoding="utf-8")
        imgs = parse_imgs(html_text)
        for attrs in imgs:
            src = attrs.get("src", "")
            alt = attrs.get("alt", "")
            haystack = attrs.get("src", "") + attrs.get("id", "") + attrs.get("data-brand-src", "")
            is_decorative = alt == "" and (any(m in haystack for m in DECORATIVE_SRC_MARKERS) or attrs.get("id") == "sdhLightboxImg")
            old = old_ledger.get((page_url, src))
            prev_alt = old["final_alt"] if old else ""
            role = classify_role(alt)
            pid = project_id(alt)
            changed = (alt != prev_alt)
            flag = "no"
            notes = PAGE_NOTES.get(fname, "")
            key = (fname, src)
            if key in OWNER_REVIEW_NOTES:
                flag = "yes"
                notes = notes + " " + OWNER_REVIEW_NOTES[key]
            if not alt and not is_decorative:
                # meaningful image with empty alt that isn't one of the known decorative cases
                flag = "yes"
                notes = notes + " Empty alt on an otherwise-meaningful image -- verify intentional."

            rows.append({
                "page": page_url,
                "source_file": SOURCE_FILE_BY_PAGE.get(fname, ""),
                "image_path": src,
                "project_or_video_id": pid,
                "classification": "decorative" if is_decorative else role,
                "previous_alt": prev_alt,
                "revised_alt": alt,
                "previous_char_count": len(prev_alt),
                "revised_char_count": len(alt),
                "first_200_revised": alt[:200],
                "grounding_sources_used": SOURCE_FILE_BY_PAGE.get(fname, ""),
                "duplicate_wording_removed": "yes" if changed else "no",
                "owner_review_flag": flag,
                "notes": notes.strip(),
            })
            if not is_decorative and alt:
                meaningful_alts.append((page_url, src, alt))

    with io.open(NEW_LEDGER, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=[
            "page", "source_file", "image_path", "project_or_video_id", "classification",
            "previous_alt", "revised_alt", "previous_char_count", "revised_char_count",
            "first_200_revised", "grounding_sources_used", "duplicate_wording_removed",
            "owner_review_flag", "notes",
        ])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    total_img_usages = len(rows)
    meaningful_count = len(meaningful_alts)
    empty_intentional = sum(1 for r in rows if r["classification"] == "decorative")
    empty_unintentional = sum(1 for r in rows if not r["revised_alt"] and r["classification"] != "decorative")

    # ---- similarity pass over first-200-char strings of meaningful alts ----
    pairs = []
    n = len(meaningful_alts)
    prefixes = [a[2][:200].lower() for a in meaningful_alts]
    for i in range(n):
        for j in range(i + 1, n):
            if meaningful_alts[i][0] != meaningful_alts[j][0]:
                continue  # only compare within the same page (cross-page reuse is handled separately)
            ratio = difflib.SequenceMatcher(None, prefixes[i], prefixes[j]).ratio()
            if ratio > 0.5:
                pairs.append((ratio, meaningful_alts[i], meaningful_alts[j]))
    pairs.sort(key=lambda x: -x[0])
    top20 = pairs[:20]

    exact_dup_groups = {}
    for page, src, alt in meaningful_alts:
        key = (page, alt[:120].lower())
        exact_dup_groups.setdefault(key, []).append(src)
    exact_dups = {k: v for k, v in exact_dup_groups.items() if len(v) > 1}

    with io.open(SIMILARITY_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Milestone 2.13 -- Similarity Audit (auto-generated)\n\n")
        f.write(f"Total `<img>` usages audited: **{total_img_usages}**\n\n")
        f.write(f"Meaningful (non-decorative, non-empty) alts: **{meaningful_count}**\n\n")
        f.write(f"Intentional empty/decorative alts: **{empty_intentional}**\n\n")
        f.write(f"Unintentional empty alts on meaningful images: **{empty_unintentional}**\n\n")
        f.write("## Exact first-120-character duplicate groups (same page)\n\n")
        if not exact_dups:
            f.write("None found.\n\n")
        else:
            for (page, prefix), srcs in exact_dups.items():
                f.write(f"- `{page}` -- {len(srcs)} images share this opening: {', '.join(srcs)}\n")
                f.write(f"  - prefix: \"{prefix[:110]}\"\n")
            f.write("\n")
        f.write("## Top 20 most similar first-200-character pairs (same page, ratio > 0.5)\n\n")
        for ratio, a, b in top20:
            f.write(f"- **{ratio:.2f}** -- `{a[0]}`: `{a[1]}` vs `{b[1]}`\n")
            f.write(f"  - A: \"{a[2][:150]}\"\n")
            f.write(f"  - B: \"{b[2][:150]}\"\n")
        if not top20:
            f.write("None above threshold.\n")

    print(f"Wrote {NEW_LEDGER} ({total_img_usages} rows)")
    print(f"Wrote {SIMILARITY_OUT}")
    print(f"total_img_usages={total_img_usages} meaningful={meaningful_count} decorative={empty_intentional} unintentional_empty={empty_unintentional} exact_dup_groups={len(exact_dups)} top_similarity_pairs={len(top20)}")


if __name__ == "__main__":
    main()
