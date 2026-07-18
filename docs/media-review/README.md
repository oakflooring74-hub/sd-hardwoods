# Owner media-review system

This folder is the owner's review surface for **every photograph and video placement on all 13
pages** of the redesigned site. It exists so that image and video descriptions are eventually
built from **facts the owner has actually confirmed** — never from guesses, filenames, or old
alt text that may be wrong.

Created in Milestone 2.5. Everything here except this README is **generated** from the
structured inventory — do not hand-edit the generated files; regenerate them instead.

## What's here

| File | What it is |
|---|---|
| `README.md` | This workflow guide (hand-maintained). |
| `index.html` | Static, local, read-only visual index of every placement with thumbnails, organized by page. Open it in a browser (internet needed for thumbnails). **Never deploy it.** |
| `<page>.md` | One human-readable review file per page (13 total), one entry per placement. |

The underlying structured data lives in:

- `build/data/media/assets.json` — one record per unique image/video
- `build/data/media/placements/<page>.json` — one record per placement (same image can appear on several pages)
- `build/data/media/owner_facts_confirmed.json` — **the only entry point for confirmed owner facts**

Regenerate everything with:

```
python build/scripts/generate_media_inventory.py
python build/scripts/validate_media_inventory.py
```

## Stable IDs

Every placement has a permanent ID the owner can dictate against without reading long
filenames or URLs:

- `HOME-IMG-005` — 5th image placement on the homepage
- `G1-IMG-012` — 12th image placement on Recent Project Gallery 1
- `VIDEOS-VID-014` — 14th video placement on the Videos page
- Prefixes: `HOME`, `DEEP`, `G1`–`G5`, `SOLID`, `VIDEOS`, `ABOUT`, `BLOG`, `CONTACT`, `ASSESS`

IDs are kept stable across regenerations (existing records are matched and preserved; new
media gets new numbers; removed media is flagged `missing_from_page`, never silently deleted).

## The workflow

1. **Claude inventories** each image and video (done — this folder).
2. **The owner identifies the factual project information** for placements, by ID
   (e.g. "G1-IMG-012 is the Hillcrest red oak job, that's the *before* shot").
3. Facts are recorded in the structured media files
   (`owner_facts_confirmed.json` for asset-level facts; placement files for placement-level
   facts such as before/after).
4. **Claude drafts** concise visitor-facing headings, captions and alt text **from confirmed
   facts only**.
5. **The owner reviews** the meaningful factual wording (`approval_status` → `approved`).
6. Only approved metadata is injected into the generated pages (future milestone — nothing is
   auto-published today).
7. `validate_media_inventory.py` proves no placement is missed and no unapproved wording
   leaks onto pages.

## Rules that bind every session

- **Never invent** species, locations, project stages, finishes, damage causes, dates or any
  other owner fact. Unknown = `needs_owner_review`.
- Existing captions/alt text are treated as *claims to verify*, not as facts — several have
  already proven false (see below).
- Confirmed facts are never overwritten by page text; the generator preserves
  `owner_facts`, `proposed_*` and `approval_status` on every run.
- Media review happens in **organized page batches**, not one-off single-image questions.

## Current confirmed facts & known conflicts (as of 2026-07-18)

**Confirmed (owner, 2026-07-18):** `TRICIA WALNUT102/110/54/23.jpg` are four views of **one**
walnut floor refinishing project at **Bing Crosby Ranch, San Diego**. Their previous homepage
alt texts (bamboo / Rancho Santa Fe parquet / La Jolla maple) were false and have been replaced
with restrained provisional wording. **Still pending:** the exact stage/angle of each photo —
do not label before/after/sanding/finish until confirmed.

**Flagged conflict:** `TRICIA WALNUT27/30/63/76.jpg` appear on the Solid Wood Gallery in a
project described as *Graff Brothers rift & quartered white oak installation* — the filenames
disagree with the description. Owner must say which is right. (Not covered by the four-image
confirmation above.)

**Video metadata flags** (source: the YouTube channel itself — fix on YouTube, then rerun
`update_youtube_videos.py`): one title beginning with `Title:`; a probable "Sold Cherry" →
"Solid Cherry" typo; four pairs of duplicate titles; the official channel handle needs
confirming (`@SANDIEGOHARDWOODS` is used visibly; one schema `sameAs` says `@SD-1974`).
