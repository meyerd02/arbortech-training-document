#!/usr/bin/env python3
"""One-off prep for the module-guide screenshots (2026-08-06 capture session).

Copies the raw Chrome captures into build/screenshots/modules/<section-type>.jpg,
cropping the Shopify preview bar off the bottom of each storefront shot, and
derives the breadcrumbs strip from the collection-hero shot. Safe to re-run if
the raw capture dir still exists; otherwise the named files in
build/screenshots/modules/ are the source of truth (replace one and re-run
build_pages.py to refresh the guide).
"""
import os
from PIL import Image

RAW = "/var/folders/3p/l68l_8bx23b9vfcr8w_cpqt40000gp/T/claude-chrome-screenshots-meUtpk"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots", "modules")
os.makedirs(OUT, exist_ok=True)

BAR = 52  # px of Shopify preview bar to crop off the bottom
MAXW = 1200  # downscale so the self-contained guide stays emailable


def save(img, path):
    if img.width > MAXW:
        img = img.resize((MAXW, round(img.height * MAXW / img.width)), Image.LANCZOS)
    img.save(path, quality=74)

# raw-file suffix -> section type
SHOTS = {
    "1785972732512-26": "arb-hero-carousel",
    "1785972732514-27": "arb-triage-trio",
    "1785972732515-28": "arb-clever-engineering",
    "1785972732516-29": "arb-featured-product",
    "1785972732517-30": "arb-shop-by-showcase",
    "1785972732518-31": "arb-featured-guide",
    "1785972772658-32": "arb-parallax-quote",
    "1785972772659-33": "arb-card-grid",
    "1785972772659-34": "arb-our-story",
    "1785972772660-35": "arb-events-calendar",
    "1785972772660-36": "arb-footer",
    "1785972797781-37": "arb-bento-grid",
    "1785972843545-43": "arb-main-product",
    "1785972824339-39": "arb-product-overview-video",
    "1785972824339-40": "arb-clever-bits",
    "1785972824340-41": "arb-product-story-panels",
    "1785972824341-42": "arb-product-tabs",
    "1785973074111-48": "arb-related-projects",
    "1785972952865-45": "arb-product-artists",
    "1785973130631-49": "arb-faq",
    "1785973130632-50": "arb-inspiration-hub-nav",
    "1785973167476-51": "arb-section-header",
    "1785973167477-52": "arb-spotlight-case-study",
    "1785973167478-53": "arb-projects-grid",
    "1785973167478-54": "arb-blog-posts-preview",
    "1785973244035-60": "arb-artist-hero",
    "1785973207242-55": "arb-about-quote",
    "1785973207244-57": "arb-artist-tools-choice",
    "1785973207247-58": "arb-artists-techniques",
    "1785973244036-61": "arbt-page-story-blocks",
    "1785973278617-62": "arb-video-player",
    "1785973278618-63": "arb-image-carousel",
    "1785973278619-64": "arb-page-next-nav",
    "1785973324941-65": "arb-vertical-hero",
    "1785973344794-69": "arb-simple-hero-banner",
    "1785973411848-74": "arbt-tool-resources-grid",
    "1785973449636-75": "arb-our-story-text",
    "1785973449637-76": "arbt-tool-resource-detail",
    "1785973488408-77": "arbt-retailer-locator",
    "1785973488409-78": "arbt-technical-resources",
    "1785973526970-79": "arbt-widerruf-form",
    "1785973526974-80": "arbt-test-accessories",
}

for suffix, name in SHOTS.items():
    src = f"{RAW}/screenshot-{suffix}.jpg"
    img = Image.open(src)
    w, h = img.size
    save(img.crop((0, 0, w, h - BAR)), f"{OUT}/{name}.jpg")

# Breadcrumbs: the orange bar (plus a little hero context) from the collection hero shot
hero = Image.open(f"{RAW}/screenshot-1785973344794-69.jpg")
w, h = hero.size
save(hero.crop((0, 430, w, 615)), f"{OUT}/arb-breadcrumbs.jpg")

print(f"wrote {len(SHOTS) + 1} module screenshots to {OUT}")
