#!/usr/bin/env python3
"""Render session-script.md → script.html: the facilitator run sheet as a
self-contained page with tickable checkboxes (state persists in localStorage,
so ticks survive a refresh on meeting day). Reuses index.html's stylesheet.

Usage: python3 build/render_script.py   (from the repo root or anywhere)
Re-run after editing session-script.md.

NOTE: script.html is deliberately NOT linked from the client-facing tab bar —
it's reachable only by URL (/script.html). Do not add it to the tabs.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = (ROOT / "session-script.md").read_text(encoding="utf-8")
style = re.search(r"(<style>.*?</style>)", (ROOT / "index.html").read_text(encoding="utf-8"), re.S).group(1)

EXTRA_CSS = """
    .script-page .article { max-width: 52em; margin: 0 auto; }
    .check-item { list-style: none; margin: 0.45em 0; display: flex; gap: 0.6em; align-items: baseline; }
    .check-item input { width: 1.05em; height: 1.05em; accent-color: var(--accent); flex: none; transform: translateY(0.15em); cursor: pointer; }
    .check-item label { cursor: pointer; }
    .check-item input:checked + label { color: var(--muted); text-decoration: line-through; text-decoration-color: rgba(232,119,34,.55); }
    ul.check-list { padding-left: 0.2em; border-left: 3px solid var(--accent); padding-left: 1em; margin: 0.8em 0 1.6em; }
    .test-head { color: var(--accent-dark); font-weight: 700; margin: 1.3em 0 0.2em; }
    .script-quote { border-left: 3px solid var(--accent); background: var(--accent-soft); padding: 0.8em 1.1em; margin: 1em 0; border-radius: 0 6px 6px 0; }
    .reset-bar { text-align: right; margin: 0.5em 0 1.5em; }
    .reset-bar button { font: inherit; font-size: 0.8em; color: var(--muted); background: none; border: 1px solid var(--line); border-radius: 6px; padding: 0.35em 0.8em; cursor: pointer; }
    .reset-bar button:hover { color: var(--ink); border-color: var(--ink); }
    @media print { .check-item input { accent-color: #000; } .reset-bar { display: none; } }
"""


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"<em>\1</em>", s)
    return s


lines = MD.splitlines()
out = []
stack = []           # open list contexts: 'ul' | 'check'
checkbox_id = 0
in_quote = False


def close_lists(to_depth=0):
    while len(stack) > to_depth:
        kind = stack.pop()
        out.append("</ul>" if kind in ("ul", "check") else "")


def close_quote():
    global in_quote
    if in_quote:
        out.append("</div>")
        in_quote = False


i = 0
while i < len(lines):
    raw = lines[i]
    line = raw.rstrip()
    i += 1

    if not line.strip():
        close_quote()
        continue

    m = re.match(r"^(#{1,3}) (.*)", line)
    if m:
        close_lists(); close_quote()
        level = len(m.group(1))
        text = inline(m.group(2))
        if level == 1:
            out.append(f"<h1>{text}</h1>")
        else:
            anchor = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f"<h{level} id=\"{anchor}\">{text}</h{level}>")
        continue

    if line.strip() == "---":
        close_lists(); close_quote()
        out.append("<hr>")
        continue

    if line.startswith("> "):
        close_lists()
        if not in_quote:
            out.append('<div class="script-quote">')
            in_quote = True
        out.append(f"<p>{inline(line[2:])}</p>")
        continue
    close_quote()

    m = re.match(r"^- \[ \] (.*)", line)
    if m:
        # absorb hanging continuation lines (6-space indent)
        text = m.group(1)
        while i < len(lines) and re.match(r"^ {4,6}\S", lines[i]) and not re.match(r"^\s*- ", lines[i]):
            text += " " + lines[i].strip(); i += 1
        if not (stack and stack[-1] == "check"):
            close_lists()
            out.append('<ul class="check-list">')
            stack.append("check")
        checkbox_id += 1
        cid = f"chk-{checkbox_id}"
        out.append(f'<li class="check-item"><input type="checkbox" id="{cid}"><label for="{cid}">{inline(text)}</label></li>')
        continue

    m = re.match(r"^(\s*)- (.*)", line)
    if m:
        depth = len(m.group(1)) // 2 + 1
        text = m.group(2)
        while i < len(lines) and re.match(r"^\s{2,}\S", lines[i]) and not re.match(r"^\s*- ", lines[i]) and not re.match(r"^\s*#", lines[i]):
            text += " " + lines[i].strip(); i += 1
        if stack and stack[-1] == "check":
            close_lists()
        while len(stack) > depth:
            out.append("</ul>"); stack.pop()
        while len(stack) < depth:
            out.append("<ul>"); stack.append("ul")
        out.append(f"<li>{inline(text)}</li>")
        continue

    # bold-header paragraph (TEST/CAPTURE) or plain paragraph
    close_lists()
    text = line.strip()
    while i < len(lines) and lines[i].strip() and not re.match(r"^\s*(-|#|>|\||---)", lines[i]):
        text += " " + lines[i].strip(); i += 1
    if re.match(r"^\*\*(TEST|CAPTURE)", text):
        out.append(f'<p class="test-head">{inline(text)}</p>')
    else:
        out.append(f"<p>{inline(text)}</p>")

close_lists(); close_quote()

body = "\n".join(out)
total = checkbox_id

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Arbortech Training – Session Run Sheet (internal)</title>
  {style.replace('</style>', EXTRA_CSS + '</style>')}
</head>
<body class="script-page">
  <header class="page-header">
    <div class="inner">
      <span class="kicker">Internal · Facilitator Run Sheet · not for client distribution</span>
      <h1><span class="brand">Arbortech</span> CMS Training – Session Script</h1>
    </div>
  </header>
  <div class="page-layout">
    <div class="article">
      <div class="reset-bar"><span id="tally"></span> <button id="reset">Reset all checkboxes</button></div>
{body}
    </div>
  </div>
<script>
(function () {{
  var KEY = 'arbt-session-script-checks';
  var state = {{}};
  try {{ state = JSON.parse(localStorage.getItem(KEY) || '{{}}'); }} catch (e) {{}}
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.check-item input'));
  function tally() {{
    var done = boxes.filter(function (b) {{ return b.checked; }}).length;
    document.getElementById('tally').textContent = done + ' / {total} checked';
  }}
  boxes.forEach(function (b) {{
    if (state[b.id]) b.checked = true;
    b.addEventListener('change', function () {{
      state[b.id] = b.checked;
      localStorage.setItem(KEY, JSON.stringify(state));
      tally();
    }});
  }});
  document.getElementById('reset').addEventListener('click', function () {{
    if (!confirm('Clear all {total} checkboxes?')) return;
    boxes.forEach(function (b) {{ b.checked = false; }});
    state = {{}};
    localStorage.removeItem(KEY);
    tally();
  }});
  tally();
}})();
</script>
</body>
</html>
"""

(ROOT / "script.html").write_text(page, encoding="utf-8")
print(f"script.html written — {total} checkboxes")
