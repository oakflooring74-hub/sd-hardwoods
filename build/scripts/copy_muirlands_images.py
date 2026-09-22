#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copy Muirlands Oak project images to repo root with SEO-friendly filenames.

Source folder: MUIRLANDS OAK FLOOR REFINISHING LA JOLLA SAN DIEGO WATERMARKED/
Output: repo root (same level as index.html, etc.)

SEO filename mapping based on image content analysis.
"""
import shutil
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent.parent / "MUIRLANDS OAK FLOOR REFINISHING LA JOLLA SAN DIEGO WATERMARKED"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Mapping: original filename -> SEO-friendly filename (matching build_muirlands_oak_refinishing_la_jolla.py)
IMAGE_MAP = {
    "20211216_181235.jpg": "red-oak-floor-refinishing-la-jolla-before-sanding-1.jpg",
    "20211216_181248.jpg": "dustless-hardwood-floor-sanding-la-jolla-wide.jpg",
    "20211231_144758.jpg": "red-oak-refinishing-low-voc-polyurethane-finish-san-diego-1.jpg",
    "20211231_144821.jpg": "bona-traffic-hd-hardwood-floor-finishing-la-jolla-after.jpg",
    "20211231_144829.jpg": "professional-wood-floor-restoration-san-diego-oak.jpg",
    "20211231_144837.jpg": "best-flooring-contractor-san-diego-hardwood-refinishing.jpg",
    "20211231_144843.jpg": "high-ranking-great-reviews-wood-floor-service-la-jolla.jpg",
    "20211231_144902.jpg": "extensive-before-after-gallery-hardwood-san-diego.jpg",
    "20211231_144910.jpg": "videos-of-wood-floor-finishing-oak-la-jolla.jpg",
    "20211231_145012.jpg": "modern-planetary-sander-hardwood-refinishing-wide.jpg",
    "20211231_145023.jpg": "san-diego-hardwoods-best-oak-floor-restoration-2.jpg",
    "20211231_145031.jpg": "low-voc-modern-finish-hardwood-refinishing-la-jolla.jpg",
    "20211231_145046.jpg": "dust-containment-equipment-wood-floor-sanding-san-diego.jpg",
    "20211231_145114.jpg": "fix-my-floor-hardwood-restoration-oak-la-jolla-after.jpg",
    "20211231_145122.jpg": "floor-refinishing-service-san-diego-harbor-view-oak.jpg",
    "20211231_145129.jpg": "professional-hardwood-floor-installation-and-refinishing-sd.jpg",
    "20211231_145136.jpg": "bona-certified-craftsman-oak-restoration-san-diego-1.jpg",
    "20211231_145145.jpg": "high-durability-polyurethane-floor-finishing-la-jolla.jpg",
    "20211231_145150.jpg": "san-diego-county-hardwood-refinishing-oak-gallery-after.jpg",
    "20211231_145152.jpg": "vintage-wood-floor-restoration-san-diego-low-voc-finish.jpg",
    "20211231_145211.jpg": "expert-hardwood-floor-refinishing-la-jolla-oak-professional.jpg",
    "20211231_145225.jpg": "dust-free-sanding-and-finishing-wood-floors-san-diego.jpg",
    "20211231_145233.jpg": "custom-stain-touch-up-oak-refinishing-la-jolla-hd.jpg",
    "20211231_145309.jpg": "mission-vintage-hardwood-floor-refinishing-san-diego.jpg",
    "CUSTOM STAINED WOOD FLOOR LA JOLLA SAN DIEGO.jpg": "custom-stained-red-oak-floor-professional-finishing-sd.jpg",
    "LA JOLLA WOOD FLOOR REFINISHING CONTRACTOR.jpg": "la-jolla-hardwood-floor-refinishing-contractor-best-service.jpg",
    "SAN DIEGO HARDWOOD FLOOR REFINISHING LA JOLLA OAK 1.jpg": "red-oak-finished-stairs-la-jolla-san-diego.jpg",
    "SAN DIEGO HARDWOOD FLOOR RESTORATION AND REPAIRS.jpg": "red-oak-floor-restoration-repair-la-jolla-san-diego-professional.jpg",
}

# Additional images referenced in build script but not in original mapping
ADDITIONAL_IMAGES = {
    "20211231_145129.jpg": "red-oak-floor-refinishing-la-jolla-during-sanding-wide.jpg",  # Duplicate source, different name
    "20211231_144829.jpg": "red-oak-floor-refinishing-la-jolla-after-finish-1.jpg",  # Duplicate source, different name
}


def main():
    copied = 0
    for orig, seo_name in IMAGE_MAP.items():
        src = SOURCE_DIR / orig
        dst = REPO_ROOT / seo_name
        
        if not src.exists():
            print(f"MISSING: {orig}")
            continue
            
        if dst.exists():
            print(f"SKIP (exists): {seo_name}")
            copied += 1
            continue
            
        shutil.copy2(src, dst)
        print(f"COPYED: {orig} -> {seo_name}")
        copied += 1
    
    print(f"\nTotal copied/skipped: {copied}/{len(IMAGE_MAP)}")


if __name__ == "__main__":
    main()
