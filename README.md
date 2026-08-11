# Shopify Training — Facilitation (internal)

Internal material for running the Arbortech CMS training session. **Never send this
folder to the client** — it contains our candid framing, known-issue talking points and
negotiation lines. The client-facing material lives in `../arbortechtools.com/shopify-training/`.

## Contents

- `session-script.md` — the facilitator run sheet: timeboxed agenda, SHOW/DEMO/ASK cues,
  per-section **TEST** checkboxes (the client-driving verification actions), the seeded
  "remedy list" (§8), and close-out CAPTURE checks.
- `agenda.html` — the weekly client catch-up agenda (`/agenda`). **Deliberately hidden:
  it appears in no tab bar** — reachable only by typing the URL, which is fine if the
  client stumbles onto it (David, 2026-08-11: "wouldn't bother me if they did"). Do NOT
  add it to `tab_nav()` in `build/build_pages.py` or to any page's tab bar. Its own tab
  bar shows the three visible tabs with none marked current. Refresh its contents each
  week before the catch-up; the actions/dates tables at the bottom are filled in live
  during the meeting.
- `catalogue-audit.html` — the catalogue audit & collections review checklist (SKUs,
  voltages, imagery, regional publishing, collections/grouping), pre-filled with
  evidence verified against the live store 2026-08-11. Tabbed into this set alongside
  the manual copies. Unlike the rest of this folder it is written client-safe — it can
  be presented to or shared with Arbortech as-is, but re-verify its live-store numbers
  (product/collection counts, open items) before reusing it at a later date.

## Relationship to `../arbortechtools.com/shopify-training/` (the client handover set)

The script and the handover set are two halves of one deliverable and must stay in step:

| This folder (internal) | `arbortechtools.com/shopify-training/` (client-facing) |
|---|---|
| `session-script.md` run sheet | `index.html` (manual), `modules.html` (module guide), `sitemap.html` (generated, currently unlinked from the tab bar — reachable via manual §3.1) |
| Candid: known limitations, rejected prototypes, negotiation lines | Diplomatic: how-to only |
| Section references like "Manual §3.2", "Module Guide tab", "Sitemap tab" point INTO the handover set | Carries no reference back to this folder |

Rules for agents working on either side:

1. **Section numbers are load-bearing.** The script cites the manual by section number
   (§2.6, §3.2 step 5, §10…). If you renumber, add or remove manual sections, sweep
   `session-script.md` for stale references in the same change.
2. **Content moved out of the manual may live on here.** Example: the manual's Wrap-Up
   section (safe-vs-call-us summary, support-contact placeholders) was removed from
   `index.html` on 2026-08-06 at David's direction — its content is now delivered
   verbally via script §0/§9. Don't "restore" it to the manual, and don't strip it from
   the script.
3. **The script states things the manual deliberately softens** (e.g. the rejected
   metaobject article-editor prototype behind §8.1, the metaobject-form UX critique in
   §5). Keep that candour here and out of the client files.
4. **Regeneration:** `sitemap.html`/`modules.html` are rebuilt by
   `../arbortechtools.com/shopify-training/build/build_pages.py` from data snapshots + `module_purposes.json`.
   If a rebuild changes what the tabs contain (page groups, module list), check the
   script's §3/§5 talking points still match.
5. **After the session actually runs**, the blanks in the script (inbox owners, support
   contact, change-request channel) get filled and the remedy-list outcomes recorded —
   at that point update the manual's `[confirm]`-type facts too if any were reinstated.

## History

- Script created 2026-08-06 (originally `docs/training-session-script-internal.md`,
  untracked); moved out of the arbortechtools.com repo entirely on 2026-08-06 so it versions as its own
  repository, cleanly separated from the client-facing handover set it documents.
