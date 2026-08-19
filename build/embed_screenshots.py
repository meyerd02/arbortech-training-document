#!/usr/bin/env python3
"""Insert (or refresh) admin/storefront screenshots into shopify-training/index.html.

Each figure is embedded as a base64 data URI so the manual stays a single
self-contained file. Source JPGs live in build/screenshots/. Idempotent:
re-running replaces existing figures (matched by data-shot id) in place.

Usage: python3 shopify-training/build/embed_screenshots.py
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SHOTS = ROOT / "build" / "screenshots"

CSS_MARK = "/* ── Screenshots ── */"
CSS_BLOCK = """    /* ── Screenshots ── */
    figure.screenshot { margin: 1.4rem 0 1.9rem; }
    figure.screenshot img { width: 100%; height: auto; display: block; border: 1px solid var(--line); border-radius: var(--radius); box-shadow: 0 1px 5px rgba(26,34,48,.09); }
    figure.screenshot figcaption { font-size: .85rem; color: var(--muted); margin-top: .55rem; line-height: 1.5; }
    figure.screenshot figcaption strong { color: var(--ink); }
"""

# (shot-id, filename, anchor-string the figure is inserted AFTER, caption html)
FIGURES = [
    ("storefront-home", "storefront-home.jpg",
     "<p>The public storefront is <code>https://arbortechtools.com</code> (and its country variants – see below). Right now the storefront is still password-protected while we finish the build; you'll log in with the store password until launch. That changes nothing about how you use the admin.</p>",
     "The public storefront – what all the content in this manual feeds. The top navigation, hero slides and audience cards are all editable through the admin areas covered below."),

    ("admin-home", "admin-home.jpg",
     "<h3>Quick tour of the sidebar</h3>",
     "The admin <strong>Home</strong> screen. The left sidebar is how you reach everything in this manual – Products, Content, Online Store, Discounts and (bottom-left) Settings."),

    ("products-list", "products-list.jpg",
     "<p><strong>Products → All products</strong> lists everything. Click a product to open it, or <strong>Add product</strong> for a new one.</p>",
     "<strong>Products → All products.</strong> Note the Status column (Active / Draft), stock per product, and the search-and-filter bar at the top. Click any row to open the product."),

    ("product-detail", "product-detail.jpg",
     "<li><strong>Duplicate</strong> – use <strong>Duplicate</strong> (top right) to copy an existing product as a starting point. <em>Tip:</em> rename it and set status to Draft before editing, so nothing half-finished goes live.</li>\n      </ul>",
     "A product edit screen (Mini Grinder MG1000): Title, Description and Media on the left; Status, Publishing and <strong>Product organisation</strong> (type, vendor, collections, tags – Section 2.5) on the right. <strong>Duplicate</strong> sits top-right."),

    ("product-variants", "product-variants.jpg",
     "<li>Customers see variant buttons (e.g. 18V / 20V) on the product page.</li>\n      </ul>",
     "The <strong>Variants</strong> section on the same product: two options (Setup and Battery Platform) generate the variant grid below, each row with its own price and stock. The <strong>Product metafields</strong> panel visible at the bottom is covered in Blind Spots."),

    ("collections-list", "collections-list.jpg",
     "<li><strong>Automated collection</strong> – rules (e.g. tag contains <code>power-tools</code>) pull products in automatically. Most of your shop collections are automated, driven by <strong>tags</strong> – so tagging a product correctly is how it lands in the right place.</li>\n      </ul>",
     "<strong>Products → Collections.</strong> The Conditions column shows which collections are automated (e.g. “Tag includes masonry”) – the two Spare Parts collections at the top with no conditions are manual."),

    ("collection-detail", "collection-detail.jpg",
     None,  # placed immediately after collections-list figure
     "Inside the Woodworking collection: the rule (<em>Tag includes woodworking</em>, top right) pulls the products in automatically. The description and search-engine listing are edited here too."),

    ("pages-list", "pages-list.jpg",
     "<p><strong>Online Store → Pages</strong> (also under Content → Pages). This is where About, Contact, Support, Sustainability, and the vertical pages (Woodworking, Masonry, Landscaping), Artists &amp; Makers, Project Stories, How-to Guides and Competitions live. The <a href=\"sitemap.html\"><strong>Sitemap</strong></a> tab lists every page on the site, grouped by how editable it is – check there before diving into an unfamiliar page.</p>",
     "<strong>Online Store → Pages.</strong> Every content page with its visibility status. The yellow banner just reminds you the storefront is still password-protected pre-launch."),

    ("page-editor", "page-editor.jpg",
     "<li><svg viewBox=\"0 0 24 24\" width=\"20\" height=\"20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M10.3 3.9 2.6 17.2a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z\"/><path d=\"M12 9v4\"/><path d=\"M12 16.5h.01\"/></svg> Several of your pages are <em>landing pages with bespoke layouts</em> (e.g. the vertical pages, artist pages). For those, the main content area may be secondary to structured blocks – if you need to change the layout, that's a call-us item.</li>\n      </ul>",
     "Editing the “Who We Are” page: rich-text Content box, Visibility and Template on the right, and the <strong>Search engine listing</strong> card at the bottom (that card is the SEO panel covered in Section 7.1). This is one of the bespoke-layout pages – note its custom template, <code>who-we-are</code>."),

    ("blog-posts", "blog-posts.jpg",
     "<li><strong>Publishing</strong> – set <strong>Active</strong> now, or schedule a date/time. Scheduled posts show as \"Scheduled\" until they go live – a \"not-yet-live\" state to be aware of (see Blind Spots → Draft vs live).</li>\n      </ul>",
     "<strong>Blog posts</strong> – every article in the News blog with its visibility and publish date. The posts with designed story layouts look identical here to normal posts – see the warning below before editing one."),

    ("menus-list", "menus-list.jpg",
     "<tr><td><strong>Customer account main menu</strong></td><td>Account pages navigation.</td></tr>\n        </tbody>\n      </table>",
     "<strong>Content → Menus.</strong> Your menus and their top-level items – Main menu drives the header navigation, Footer menu the footer columns, and the two Legal menus the legal strip (Section 10.2)."),

    ("main-menu-editor", "main-menu-editor.jpg",
     "<li><strong>Save menu</strong> when done.</li>\n      </ul>",
     "Editing the <strong>Main menu</strong>: each row is a top-level header item (Shop All, Woodworking, Masonry, Landscaping, Inspiration, Support). The ▸ arrow expands nested sub-items; drag the handles to reorder, and <strong>Save</strong> when done."),

    ("theme-editor", "theme-editor.jpg",
     "<p>Your homepage is built from content sections you can edit safely. Click any section in the editor to open its settings:</p>",
     "The <strong>Theme Editor</strong>: the left panel lists every section on the page (Hero Carousel, Triage Trio, …), the middle shows a live preview, and clicking a section – here the Newsletter popup – opens its settings on the right. <strong>Save</strong> is top-right."),

    ("themes-page", "themes-page.jpg",
     "<h3>5.4 Saving vs publishing theme changes</h3>\n      <p>This store works on a <strong>shared dev theme + preview duplicate</strong> model:</p>",
     "<strong>Online Store → Themes.</strong> The theme at the top is the <em>published</em> storefront (the current preview duplicate); underneath are the draft themes, including the shared dev theme marked “Do Not Publish”. You edit content with <strong>Edit theme</strong> – the Publish buttons are Juicebox's job."),

    ("files-library", "files-library.jpg",
     "<p><strong>Settings → Files</strong> (or the image picker inside any product/page/section) is where images are stored and reused.</p>",
     "<strong>Content → Files</strong> – the store's image library. Note the Alt text column (fill it in!) and the References column showing where each file is used."),

    ("discounts", "discounts.jpg",
     "<p><strong>Discounts</strong> (in the sidebar) is fully yours to manage – it's content, not plumbing.</p>",
     "<strong>Discounts</strong> – codes and automatic discounts with their status (Scheduled / Active / Expired), method and type. The Eligibility column shows when a discount is limited to specific markets."),

    ("languages-settings", "languages-settings.jpg",
     "<p>Germany is the one market in a different <em>language</em>. German text lives in several places depending on what kind of text it is:</p>",
     "<strong>Settings → Languages.</strong> English is the default; German is published and served on the German market. The <strong>Translate</strong> button next to German is one way into the translation editor."),

    ("storefront-filters", "storefront-filters.jpg",
     "<p>All three metafields are lists of text labels – reuse existing spellings exactly (copy from a similar product) or the filter grows near-duplicate options. If a new product isn't filterable, these fields plus the tags are the first things to check.</p>",
     "The shop filter sidebar as customers see it (Woodworking collection): the <strong>Vertical</strong> and <strong>By Product</strong> groups come from tags; the contextual filters appear per bucket. Every value here traces back to the product fields in the table above."),

    ("product-metafields-seo", "product-metafields-seo.jpg",
     "<p>If a product page shows content that isn't in the description box, it's coming from one of these. If you can't see a field, click <strong>View all</strong> / the <strong>⋮</strong> menu on the product page → <em>Edit metafields</em>, or check <strong>Settings → Custom data</strong> for the metaobject forms (Story panels / Clever Bits are edited as forms with rich text + image pickers).</p>",
     "The bottom of a product page: the long list of <strong>metafields</strong> (story content, related products, compatibility, legacy URLs…) that powers the rich product-page content – followed by the <strong>Search engine listing</strong> card. If text on the storefront isn't in the Description box, it's almost certainly in one of these fields."),
]


def data_uri(path: Path) -> str:
    b = path.read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("ascii")


def figure_html(shot_id: str, filename: str, caption: str) -> str:
    uri = data_uri(SHOTS / filename)
    return (
        f'<figure class="screenshot" data-shot="{shot_id}">'
        f'<img src="{uri}" alt="Screenshot: {shot_id.replace("-", " ")}" loading="lazy">'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    if CSS_MARK not in html:
        anchor = "    /* ── Header ─────────────────────────────────────────────── */"
        assert html.count(anchor) == 1, "CSS anchor not found"
        html = html.replace(anchor, CSS_BLOCK + "\n" + anchor)

    # Drop any previously inserted figures, then (re)insert fresh ones.
    html = re.sub(r'\n?\s*<figure class="screenshot" data-shot="[^"]*">.*?</figure>', "", html, flags=re.S)

    prev_id = None
    for shot_id, filename, anchor, caption in FIGURES:
        fig = figure_html(shot_id, filename, caption)
        if anchor is None:
            # chain: insert straight after the previous figure
            marker = f'data-shot="{prev_id}"'
            idx = html.index(marker)
            end = html.index("</figure>", idx) + len("</figure>")
            html = html[:end] + "\n\n      " + fig + html[end:]
        else:
            count = html.count(anchor)
            if count != 1:
                sys.exit(f"Anchor for {shot_id} matched {count} times – aborting, nothing written.")
            html = html.replace(anchor, anchor + "\n\n      " + fig)
        prev_id = shot_id

    INDEX.write_text(html, encoding="utf-8")
    size_mb = INDEX.stat().st_size / 1e6
    print(f"Inserted {len(FIGURES)} screenshots into {INDEX.name} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
