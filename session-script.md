# Arbortech CMS Training — Facilitator Script (INTERNAL — not for client handover)

> Companion to the client-facing set in `shopify-training/` (Manual / Sitemap / Module
> Guide tabs). This is your run sheet: talking points, demo beats, questions to force,
> and the remediation list we want surfaced. Keep it on your second screen.

---

## 0 · Framing (say this first, ~3 min)

Open with the *why* before any clicking:

> "Two goals today. One: you leave able to do the routine content work yourselves —
> products, pages, posts, menus, images. Two — and this is the more important one this
> week — **we want to surface everything about how this CMS works for you while we're
> all in the room**. If something feels clunky, hard to find, or you think 'I'd never
> remember that', say it out loud. This week is the window where fixing things is
> cheap. After launch it's a change request; today it's a conversation."

Mechanics to state:

- Session is recorded; they keep the recording + the manual (show the three tabs).
- Ground rule: interrupt freely. Every "wait, go back" tells us something worth writing down.
- You (David) keep a visible running list — **"the remedy list"** — anything raised
  gets written down in front of them. Don't promise anything in the room; we triage after.
- Confirm the two `[confirm]` placeholders live, and fill them in the manual afterwards:
  - Juicebox support contact for content questions: ____________
  - Change-request channel (email? ticket?): ____________

---

## 1 · Orientation (~5 min) — Manual §1

- SHOW: admin.shopify.com/store/arbortechtools.
  - Bookmark it now, together — the admin is where everything happens, never the public site.
  - Personal staff logins only; never share an account; 2FA is on and stays on.
  - The storefront password stays until launch; it changes nothing about admin work.
- SHOW: the sidebar map (manual's table).
  - Products = catalogue; Content = pages/blog/files; Online Store = themes, navigation,
    redirects; Settings = plumbing (mostly ours).
  - "If you're ever lost: which of these four does my task belong to?"
- KEY FRAME to plant early: **one store, five markets**.
  - Same product, page and post everywhere — you never duplicate per country.
  - The address prefix (`/`, `/en-us`, `/en-ca`, `/en-uk`, `/de-de`) decides currency,
    tax display and language.
  - Corollary: an edit is live in five countries at once. Draft-first habit matters.
- ASK: "Who will actually be doing content day-to-day?"
  - Determines depth for the rest of the session.
  - Our open question from the build: **who authors articles post-launch?** Get this
    answered today — it decides whether article tooling is ever worth revisiting (§8.1).

**TEST — before moving on:**
- [ ] Every attendee is logged into the admin on their own staff account (2FA passed).
- [ ] Every attendee can open Products, Pages and the Theme Editor (permissions right).
- [ ] One attendee switches the storefront between `/` and `/en-us` and sees the
      currency change (proves the market model landed).

## 2 · Products (~15 min) — Manual §2

Demo on the practice draft product, then one real product (e.g. TURBOPlane).

- Edit title/description → Save → view on storefront.
  - Point out the description box is the *short* editorial blurb.
  - The long designed content (story panels, clever bits) lives elsewhere — seed the
    metafields topic now, pay it off in §5.
- Variants + pricing.
  - **Compare-at price** = the was/now sale display; price = what's charged.
  - Prices per market come from price lists — they maintain AUD; the other markets are
    managed lists, not separate spreadsheets to keep in sync by hand.
- Tags: this store runs on them.
  - Vertical tags (woodworking / masonry / landscaping) decide which audience journeys
    a product appears in.
  - Bucket tags (power-tools / attachments-accessories / spare-parts-consumables) drive
    the collection sidebar filters.
  - Wrong or missing tags = invisible product. Copy tag spellings from a similar
    product, never free-type.
  - DEMO: remove a tag on the draft product, show it vanish from its collection; restore.
- Related accessories / compatible-with metafields (manual §2.6).
  - Do one live: add an accessory to a tool's related list, show the tile appear.
  - This is their first metafield edit — name it as such ("this is what a metafield is").
- ⚠️ Variant options are **market-routed** (voltage etc.).
  - A new variant whose option value the market rules don't know silently doesn't show
    in some countries — no error, no warning.
  - State the standing rule now (formally agreed in §8.5): new variants → tell us first.
- ASK: "Does the tag system make sense, or do you want a cheat-sheet card per product
  type?" → remedy list if hesitation.

**TEST — client driving, on the practice draft product:**
- [ ] Client edits the title + description, saves, and finds the change on the storefront.
- [ ] Client changes a price and a compare-at price and sees the was/now display.
- [ ] Client removes a bucket tag, confirms the product drops out of its collection,
      then restores it (copy-pasting the tag spelling from another product).
- [ ] Client adds a related accessory via the metafield and sees the tile appear on
      the tool's page.
- [ ] Verbal check: client can say back the rule for new variants ("tell Juicebox first").

## 3 · Pages & the sitemap tab (~10 min) — Manual §3, Sitemap tab

- SHOW the **Sitemap tab**: the menu tree, then the 134-page inventory *grouped by kind*.
  - The tree is what customers see; the inventory is what actually exists — a page can
    exist and be linked nowhere.
  - **Standard pages (32)** — fully theirs, rich-text editing, go for it.
  - **Everything else (~100)** — designed templates (verticals, artists, tool resources,
    power-carve landings). Content there is theme sections or structured data; the
    Content box often does nothing.
  - **This is the biggest expectation gap in the whole CMS — land it explicitly**, and
    point at the group notes in the Sitemap tab as the permanent reference.
- DEMO: create a page → publish → *show it's invisible* → add to a menu → visible.
  - Use the draft practice page.
  - Say the sentence: "Publishing doesn't put it anywhere — linking does."
  - Cross-ref Manual §3.2 step 5, which now spells this out.
- Blog posts: normal posts are easy — demo one end to end.
  - Title, content, featured image (news listing + social shares), tags, schedule.
  - The **designed story articles are not editable via the Content box** — layout/text
    changes go through us (manual §3.3 warn box).
  - Be upfront: this is a known limitation we've already wrestled with, not an
    oversight — the full story is in §8.1.
- ASK: "How often do you expect to want story-style articles? Weekly? Quarterly?"
  - If 'often', §8.1 is the #1 remedy-list item and deserves real time.
  - Also ask who writes them — same person as the day-to-day content owner?

**TEST — client driving:**
- [ ] Client creates a page from scratch, publishes it, and confirms it is NOT
      reachable from the storefront nav.
- [ ] Client links that page into a menu and confirms it appears (then removes it).
- [ ] Client edits a standard page (e.g. a support article) and sees the change live.
- [ ] Client opens a designed page (e.g. Woodworking), looks at the Content box, and
      says back where its real content lives ("theme sections / call Juicebox").
- [ ] Client creates a draft blog post with a featured image and schedules it, then
      deletes it.

## 4 · Navigation (~5 min) — Manual §4

- Edit the main menu live: rename something, drag it, undo.
  - Nesting = mega-menu columns; drag to reorder is safe and instant.
  - Always link via the picker (product/collection/page), not pasted URLs — the picker
    keeps links correct across all five markets.
- ⚠️ Mega-menu **promo images** are NOT in Navigation.
  - They're theme-editor header blocks matched to menu items **by title**.
  - Rename a top-level menu item → its promo imagery silently detaches.
  - Rule of thumb to agree: renaming top-level nav = ping us first.
- Footer.
  - Columns come from Shopify menus where the matching menu exists.
  - The legal menu has a separate German variant — don't edit one and forget the other.

**TEST — client driving:**
- [ ] Client renames a *sub-level* menu item, saves, verifies on the storefront, and
      renames it back.
- [ ] Client drags a menu item to reorder and confirms the storefront follows.
- [ ] Client adds a menu item using the picker (not a pasted URL) and removes it again.
- [ ] Verbal check: client can say back why top-level renames are a call-us item
      (mega-menu promo images match by title).

## 5 · Theme editor & the Module Guide tab (~15 min) — Manual §5, Modules tab

This is the section most likely to lose people. Structure it as: *what's safe* →
*what's data* → *what's ours*.

- SHOW: Customize on the homepage.
  - Click a section, change a heading, DON'T save — show the preview updating live.
  - Then discard. Say it: "Everything previews before it saves — but Save IS live;
    there's no draft mode for the published theme."
  - Sections reorder by drag; the eye icon hides without deleting — safer than removing.
- SHOW the **Module Guide tab** and teach the one distinction that matters.
  - Settings-driven modules: what you type in the editor is what renders.
  - **Data-driven** modules (story panels, clever bits, projects, events, retailers,
    technical documents): the editor holds only headings — content lives in
    Settings → Custom data. Each entry's "Data source" line tells you which kind it is.
  - Do ONE metaobject edit live — an event or retailer is safest; story panels are the
    fiddliest, don't start there.
- Be honest about metaobject forms.
  - They work, but they're clunky: long forms, every field visible whether relevant or not.
  - Say we know — this is Shopify's editing surface; we didn't build it this way.
  - Watch their reaction during the live edit — if they recoil, remedy list (§8.2).
- GUARDRAIL (non-negotiables, stated plainly):
  - Never Publish a different theme — that swaps the whole live site.
  - Never Edit code — no undo, no history.
  - Theme previews/duplicates and the preview-cut ritual are ours to run.
- ASK: "Which homepage/landing content do you expect to change most often?"
  - Then demo exactly that path, whatever it is — leave them having done their own
    most-likely task once already.

**TEST — client driving, in the Theme Editor:**
- [ ] Client changes a homepage heading, previews it, and **discards** without saving
      (the discard is the skill being tested).
- [ ] Client hides a section with the eye icon, previews, un-hides.
- [ ] Client opens the Module Guide tab, picks the section they just touched, and
      identifies from its entry whether it's settings-driven or data-driven.
- [ ] Client edits one metaobject (event or retailer) in Settings → Custom data and
      finds the change on the storefront.
- [ ] Verbal check: client says back the two never-dos (never Publish another theme,
      never Edit code).

## 6 · Media, SEO, orders-lite (~8 min) — Manual §6–8

- Files (Content → Files).
  - Upload once, reuse everywhere — don't re-upload the same image per page.
  - Keep originals big; the theme resizes. Sensible filenames help you find things later.
  - **Alt text lives on each image** — it's the SEO + accessibility text; fill it as you
    upload, retrofitting is misery.
- SEO block (bottom of every page/product edit screen).
  - Page title + meta description = the Google snippet; write for the click.
  - Changing a URL handle prompts "create a redirect?" — **always accept**; declining
    breaks every existing link to that page.
- Orders: read-only tour.
  - Look, refund conversations, customer lookups — but fulfilment is the warehouse +
    the packing-slip automation; deliberately out of scope today.
  - Newsletter signups appear in Customers and sync to Mailchimp — that's expected,
    not a data leak.
- Confirm inbox owners on the spot:
  - contact form → arbortech@arbortech.com.au — monitored by? ____________
  - service/warranty → service@arbortech.com.au — monitored by? ____________
  - store/notifications → steveb@arbortech.com.au — monitored by? ____________

**TEST — client driving:**
- [ ] Client uploads an image to Files, sets its alt text, and places it on the
      practice page.
- [ ] Client edits a page's SEO title/description and previews the snippet.
- [ ] Client renames a URL handle on the practice page, **accepts the redirect
      prompt**, and verifies the old URL still lands.
- [ ] Client submits the storefront contact form and the named inbox owner confirms
      it arrived.

## 7 · German & markets reality check (~5 min) — Manual §10

- Translate & Adapt demo: one product field EN→DE.
  - English left, German right, Save is live.
  - Untranslated = English fallback — the site never breaks, it just goes English.
  - Translations don't update themselves: change the English, the old German stays.
    Habit: after an English edit, glance at the German column.
- German structured content is separate, not translated.
  - Story panels / clever bits: separate `_de` metaobject lists.
  - Story articles: separate `story-de-*` posts entirely.
  - German content is real ongoing work, and it's **their** work (per project scope) —
    confirm who owns it and whether they have a copy/translation pipeline.
- OPEN DECISION to raise: `/en-de` (English-for-Germany).
  - Advertised to Google, but no language selector renders anywhere — no visitor can
    reach it.
  - Fix is either wire a selector (only Germany would see it) or stop publishing
    English for the DE market.
  - Business call, not technical → remedy list, owner + date (details in §8.6).

**TEST — client driving:**
- [ ] Client translates one product field EN→DE in Translate & Adapt and finds it on
      `/de-de`.
- [ ] Client changes the English source field and observes the German did NOT update
      (the drift lesson), then fixes the German.
- [ ] Client browses an untranslated page on `/de-de` and sees the English fallback
      (so they recognise it later instead of reporting it as a bug).
- [ ] German content owner is named and written on the remedy list.

## 8 · The remedy list — seed it yourself (~10 min)

Don't wait for them to find these; put our own known issues on the table first. If we
go first with the awkward stuff, they'll follow — it proves we meant it when we asked
them to be blunt. Each item: the headline, then bullets to speak to.

1. **Story-article editability** — designed articles are Juicebox-gated today.
   - The polished stories (quote banners, carousels, video bands) come from structured
     layout data, not the Content box — that's what makes them look designed.
   - We prototyped admin-native block editing this month and rejected it: the editing
     forms Shopify gives us are poor (every field visible on every block, nothing
     rich-text where it matters). We'd rather tell you that than ship you a bad tool.
   - Realistic options, in cost order: (a) you draft in ordinary posts, we "design
     them up" on a turnaround SLA; (b) a scheduled batch cadence — send us N stories a
     month; (c) budget a proper hosted editor later if volume justifies it.
   - ASK: "How many designed stories a month do you actually expect?" — get a number,
     then pick the option that fits it. Capture the preference.

2. **Metafield discoverability** — the "fields that don't look like fields."
   - Much of the richest content (story panels, clever bits, compatibility, short
     descriptions) hides behind View all / ⋮ → Edit metafields / Settings → Custom data.
   - The real risk: they edit the visible field, nothing changes on the site, and
     they stop trusting the CMS.
   - Candidate remedy: we pin the handful of fields you'll actually touch to the top of
     the product screen and unpin the plumbing. Cheap, high value.
   - ASK: "Which fields did you find yourself hunting for during the demos?" → pin list.

3. **The Content-box trap on designed pages.**
   - ~100 of the 134 pages have bespoke templates where the Content box is secondary
     or ignored (Sitemap tab shows exactly which).
   - Editing the box on those pages does nothing visible — same risk of them losing
     faith in the CMS.
   - Candidate remedies: a naming convention ("[designed]" prefix in the page title?);
     a one-line note in each affected page's body saying where the content really lives;
     or just the Sitemap tab as the reference. ASK: "What would have saved you?"

4. **New-page invisibility** — publish ≠ linked.
   - Shopify never auto-adds pages to menus; a published page is reachable only by URL.
   - Now covered in Manual §3.2 step 5, and demoed today (§3).
   - ASK: "Is the manual note enough, or do you want page-creation to be a call-us
     workflow for the first month?"

5. **Market option rules** — powerful, dangerous, opaque.
   - Which variant options each country sees (voltages, plug types) is rule-driven —
     that's how one product serves five markets cleanly.
   - The failure mode is silent: add a variant with an option value the rules don't
     know, and it simply doesn't appear in some countries. Nobody gets an error.
   - PROPOSE the standing rule: new variants and new option values are a tell-us-first
     item until further notice. Get explicit agreement, note it.

6. **`/en-de` decision** (carried from §7).
   - Google is told an English version of the German store exists; no visitor can
     actually switch to it — there's no language selector anywhere.
   - Two clean fixes: wire a selector into the footer (only Germany would see it), or
     stop advertising English-for-Germany altogether.
   - This is a business call about German-market customers, not a technical one.
     ASK: "Do your German customers expect English?" → owner + date.

7. **USD pricing** — US shoppers currently see AUD-converted prices.
   - The proper USD price list can't switch on until USD is enabled as a presentment
     currency (a store-settings step from the migration's client-action list).
   - Until then US pricing drifts with the exchange rate — fine for a password-gated
     site, not fine for launch.
   - ASK: who owns enabling it, and do they have the intended USD price list ready?

8. **Stamped reviews** — installed but switched off.
   - Reviews are wired into the theme behind a toggle; nothing shows today.
   - Decisions needed before enabling: launch with zero reviews or seed/import some
     first? Who moderates? Which products first?
   - ASK: "When do you want reviews live, and who owns them?" → capture.

**CAPTURE — the section isn't done until:**
- [ ] Every raised item (ours or theirs) has **what / who / by when** — "post-launch
      backlog" is an acceptable answer, silence isn't.
- [ ] Story-article preference recorded: design-up SLA / batch cadence / editor later (§8.1).
- [ ] Metafield pin-list drafted from what they hunted for (§8.2).
- [ ] Standing rule on variants/option values explicitly agreed (§8.5).
- [ ] `/en-de` decision has an owner and a date (§8.6).
- [ ] USD presentment has an owner, and the USD price list status is known (§8.7).
- [ ] Stamped reviews has a go-live intention and an owner (§8.8).

## 9 · Wrap-up (~5 min)

- Read back the remedy list, owners, dates.
  - Every item aloud, with its owner's name — people keep commitments they made out
    loud in front of colleagues.
  - Undecided items get an explicit "parked until <date>", not silence.
- Restate the line (the manual's former summary now lives here, verbally):
  - Safe to edit yourselves: content — product/page/post text and images, prices, tags,
    collections, menus via the picker, homepage section content, SEO, files, redirects.
  - Call us: structure and plumbing — theme code, templates, checkout/payments/shipping/
    tax, apps, domains, publishing themes, market option rules, anything uncertain.
- Confirm the support channel (from §0) and the follow-up session.
  - Repeat the contact + change-request channel you confirmed at the start; they write
    it down somewhere real.
  - Book the ~2-week follow-up **now**, in the meeting, not by email later.
- Hand over: the three-tab manual set + recording.
  - Point out the tabs: Manual (how-to), Sitemap (what exists and how editable), Module
    Guide (every theme section explained).
  - Remind them it's personalised — their menus, pages and inboxes by name.
- Last ask: "What's the one thing you're least confident doing alone?"
  - Do that one live, together, before closing — them driving, you narrating.

**TEST — session close-out:**
- [ ] Remedy list read back in full; no item without an owner.
- [ ] Support contact + change-request channel written down by the client (not just said).
- [ ] Follow-up session booked in calendars before anyone leaves.
- [ ] The "least confident" task performed by the client, unassisted, successfully.
- [ ] Recording stopped and saved; link shared with attendees alongside the manual set.

---

## Parking-lot answers (things they may ask, with our line)

- **"Can we get a nicer article editor?"** — "The built-in options are what you saw; a
  proper editor is a small custom app. If story cadence justifies it, we'll scope it."
- **"Why can't we edit the artist pages' text?"** — Artist pages are metafield-driven;
  the fields ARE editable (page → metafields) but fiddly — offer to walk through one
  if they'll do it often, else it's a call-us.
- **"Can we add a new collection ourselves?"** — Yes (manual §2.4), but the sidebar
  buckets are handle-driven: a new *bucket* collection needs the right handle pattern —
  tell us the intent and we'll confirm the handle.
- **"When does the password come off?"** — launch plan question, not a CMS question;
  park it with a named owner.
- **"Can we see what changed / roll back?"** — Themes: we keep the outgoing preview as
  the undo for one round; content (products/pages/posts): no version history in
  Shopify — edits are live, hence the draft-first habit.
