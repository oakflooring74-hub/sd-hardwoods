# -*- coding: utf-8 -*-
"""
Refresh build/data/youtube_videos.json from the public San Diego Hardwoods
YouTube channel (https://www.youtube.com/@sandiegohardwoods).

    python build/scripts/update_youtube_videos.py

This is a MANUAL utility -- the normal site build never runs it and never
touches the network. It scrapes public YouTube page data only (no API key,
no credentials, nothing secret):

  1. Reads the channel's /videos and /shorts tabs (ytInitialData), following
     innertube continuations, to enumerate every public upload.
  2. Fetches each video's watch page (ytInitialPlayerResponse) for the exact
     title, publish date, duration, and description.
  3. Merges with the existing snapshot: curated fields maintained by hand in
     the snapshot (site_description, site_display_title, gallery_href,
     gallery_label, featured, featured_rank) are preserved for videos that
     already exist. New videos
     are added with a heuristic category (baked into the file so the rendered
     result stays deterministic); videos no longer public are DROPPED, with a
     loud notice printed so the removal is a conscious decision at review time.
  4. Writes the snapshot sorted: featured (by rank) first, then newest first.

After running it: review `git diff build/data/youtube_videos.json`, re-run
`python build/scripts/build_all.py`, and review the regenerated Videos page.

If YouTube changes its page internals and the scrape breaks, yt-dlp
(`yt-dlp --flat-playlist -J <channel-url>`) or the YouTube Data API (with a
key kept OUTSIDE this repository) are alternative metadata sources -- feed
whatever they return into the same snapshot schema rather than changing the
build.
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent  # -> build/
SNAPSHOT = BUILD / "data" / "youtube_videos.json"
CHANNEL = "https://www.youtube.com/@sandiegohardwoods"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

CATEGORIES = {
    "dust-contained-refinishing": "Dust-Contained Sanding & Refinishing",
    "repairs-restoration": "Repairs & Restoration",
    "deep-cleaning-recoating": "Deep Cleaning & Recoating",
}


def fetch(url, data=None, content_type=None):
    headers = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def walk(obj, key, out):
    if isinstance(obj, dict):
        if key in obj:
            out.append(obj[key])
        for v in obj.values():
            walk(v, key, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, key, out)


def harvest_tab_ids(tab):
    """Return the ordered list of video IDs on a channel tab (videos/shorts),
    following continuations."""
    html = fetch(f"{CHANNEL}/{tab}")
    api_key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    data = json.loads(m.group(1))

    ids, tokens_seen = [], set()

    def collect(obj):
        lockups, shorts, conts = [], [], []
        walk(obj, "lockupViewModel", lockups)
        walk(obj, "shortsLockupViewModel", shorts)
        walk(obj, "continuationItemRenderer", conts)
        for lv in lockups:
            if lv.get("contentId"):
                ids.append(lv["contentId"])
        for s in shorts:
            vid = None
            try:
                vid = s["onTap"]["innertubeCommand"]["reelWatchEndpoint"]["videoId"]
            except (KeyError, TypeError):
                pass
            if vid:
                ids.append(vid)
        return [c.get("continuationEndpoint", {}).get("continuationCommand", {}).get("token")
                for c in conts
                if c.get("continuationEndpoint", {}).get("continuationCommand", {}).get("token")]

    tokens = collect(data)
    while tokens:
        tok = tokens.pop(0)
        if tok in tokens_seen:
            continue
        tokens_seen.add(tok)
        body = json.dumps({
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.20260101.00.00"}},
            "continuation": tok,
        }).encode()
        resp = fetch(f"https://www.youtube.com/youtubei/v1/browse?key={api_key}",
                     data=body, content_type="application/json")
        tokens += collect(json.loads(resp))

    seen, ordered = set(), []
    for vid in ids:
        if vid not in seen:
            seen.add(vid)
            ordered.append(vid)
    return ordered


def fetch_video_meta(vid):
    html = fetch(f"https://www.youtube.com/watch?v={vid}")
    m = re.search(r"var ytInitialPlayerResponse = (\{.*?\});(?:var |</script>)", html, re.S)
    pr = json.loads(m.group(1))
    vd = pr.get("videoDetails", {})
    mf = pr.get("microformat", {}).get("playerMicroformatRenderer", {})
    return {
        "title": vd.get("title", ""),
        "lengthSeconds": int(vd.get("lengthSeconds", 0)),
        "publishDate": (mf.get("publishDate") or "")[:10],
        "description": vd.get("shortDescription", ""),
    }


def categorize(title):
    t = title.lower()
    if "deep clean" in t or "power scrubber" in t:
        return "deep-cleaning-recoating"
    if "restoration" in t or "repair" in t or "transformation" in t:
        return "repairs-restoration"
    return "dust-contained-refinishing"


def iso_duration(sec):
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + f"{s}S"


def duration_text(sec):
    m, s = divmod(int(sec), 60)
    h, m2 = divmod(m, 60)
    return f"{h}:{m2:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    old = {}
    if SNAPSHOT.exists():
        with open(SNAPSHOT, encoding="utf-8") as f:
            old = {r["id"]: r for r in json.load(f)["videos"]}

    print("Enumerating channel uploads...")
    video_ids = harvest_tab_ids("videos")
    short_ids = harvest_tab_ids("shorts")
    all_ids = video_ids + [v for v in short_ids if v not in video_ids]
    print(f"  {len(video_ids)} standard videos, {len(short_ids)} shorts")

    records = []
    for vid in all_ids:
        try:
            meta = fetch_video_meta(vid)
        except Exception as exc:  # noqa: BLE001 -- report and keep the old record
            print(f"  WARN: could not refresh {vid} ({exc}); keeping previous data")
            if vid in old:
                records.append(old[vid])
            continue
        prev = old.get(vid, {})
        rec = {
            "id": vid,
            "title": meta["title"] or prev.get("title", ""),
            "watch_url": f"https://www.youtube.com/watch?v={vid}",
            "embed_url": f"https://www.youtube-nocookie.com/embed/{vid}",
            "thumbnail_url": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            "publish_date": meta["publishDate"] or prev.get("publish_date", ""),
            "duration_seconds": meta["lengthSeconds"],
            "duration_iso8601": iso_duration(meta["lengthSeconds"]),
            "duration_text": duration_text(meta["lengthSeconds"]),
            "is_short": vid in short_ids,
            "category": prev.get("category") or categorize(meta["title"]),
            "featured": prev.get("featured", False),
            "featured_rank": prev.get("featured_rank"),
            "description": meta["description"],
        }
        rec["category_label"] = CATEGORIES[rec["category"]]
        for key in ("site_description", "site_display_title", "gallery_href", "gallery_label"):
            if prev.get(key):
                rec[key] = prev[key]
        records.append(rec)
        time.sleep(0.3)

    dropped = [vid for vid in old if vid not in {r["id"] for r in records}]
    for vid in dropped:
        print(f"  NOTICE: {vid} ({old[vid].get('title', '?')[:60]}) is no longer "
              "public and was dropped from the snapshot")

    featured = sorted([r for r in records if r["featured"]],
                      key=lambda r: r["featured_rank"] or 99)
    rest = sorted([r for r in records if not r["featured"]],
                  key=lambda r: (r["publish_date"], r["id"]), reverse=True)
    records = featured + rest

    snapshot = {
        "_comment": ("Checked-in snapshot of every public upload on the San Diego Hardwoods "
                     "YouTube channel (https://www.youtube.com/@sandiegohardwoods). The Videos "
                     "page build consumes this file only -- no network access during builds. "
                     "Refresh with: python build/scripts/update_youtube_videos.py (see "
                     "build/README.md). Curated fields preserved across refreshes: "
                     "site_description, site_display_title, gallery_href, gallery_label, "
                     "featured, featured_rank. site_display_title is used only where the live "
                     "title is blank or date-only; the live title is always preserved in "
                     "`title`."),
        "channel_url": CHANNEL,
        "snapshot_date": time.strftime("%Y-%m-%d"),
        "video_count": len(records),
        "videos": records,
    }
    with open(SNAPSHOT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(snapshot, f, indent=1, ensure_ascii=False)
    print(f"Wrote {SNAPSHOT} ({len(records)} videos). Review `git diff`, then re-run "
          "python build/scripts/build_all.py.")


if __name__ == "__main__":
    sys.exit(main())
