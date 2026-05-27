#!/usr/bin/env python3
"""
Extend the Test 1 Review deck: for each Ch 1-8 flow-chart slide, add
6 vertical sub-slides (5 MC + 1 handout problem) drawn from the
existing review-guide markdown. Pressing 'Down' from each chapter
flow chart reveals the practice problems one at a time.

Reveal.js vertical-slide convention:
   <section>           ← outer wrapper (acts as a horizontal slide column)
     <section>...</section>   ← vertical position 1 (flow chart, unchanged)
     <section>...</section>   ← vertical position 2 (MC #1)
     ... etc
   </section>

This script:
  1. Reads the review-guide markdown to extract per-chapter MC + handout + answers.
  2. Reads the current index.html.
  3. For each Ch 1-8 <section id="ch0N">…</section> block, wraps it in an
     outer <section> and appends 6 sub-section <section> blocks (5 MC + 1 handout).
  4. Writes the rebuilt index.html.

Idempotent: re-runs detect the existing wrapper structure and re-replace.
"""
from __future__ import annotations
import re
from pathlib import Path

HERE = Path(__file__).parent
INDEX = HERE / "index.html"
GUIDE = Path("/Users/openclaw/Resilio Sync/documents/econ-project-book/principles-of-microeconomics/study-guides/test-1-ch1-8/test-1-review-guide.md")


# ---------- Parse the review guide MD ----------
def parse_review_guide(md: str) -> dict[int, dict]:
    """Return {chapter_num: {'mc': [...], 'handout': {...}, 'answers': {...}}}."""
    out: dict[int, dict] = {}
    # Split on chapter headings "# Chapter N — Title"
    chapter_blocks = re.split(r"^# Chapter (\d+) — (.+?)$", md, flags=re.MULTILINE)
    # chapter_blocks: [pre, '1', 'Title', body, '2', 'Title', body, ...]
    for i in range(1, len(chapter_blocks), 3):
        n = int(chapter_blocks[i])
        body = chapter_blocks[i + 2]
        out[n] = {
            "title": chapter_blocks[i + 1].strip(),
            "mc": extract_mc(body),
            "handout": extract_handout(body),
            "answers": extract_answers(body, n),
        }
    return out


def extract_mc(body: str) -> list[dict]:
    """Pull the 5 ## Sample Multiple Choice questions out of a chapter body."""
    sec = re.search(r"## Sample Multiple Choice\s*\n(.+?)(?=^## |\Z)", body, flags=re.DOTALL | re.MULTILINE)
    if not sec:
        return []
    text = sec.group(1)
    # Each MC starts with "**N.** ..." followed by 4 bullets "- A) …", "- B) …" etc.
    qs = []
    # Split text by leading **N.**
    parts = re.split(r"^\*\*(\d+)\.\*\*\s+", text, flags=re.MULTILINE)
    # parts: [pre, '1', q1_body, '2', q2_body, ...]
    for i in range(1, len(parts), 2):
        qnum = int(parts[i])
        qbody = parts[i + 1]
        # The stem is everything before the first bullet "- A)"
        lines = qbody.split("\n")
        stem_lines = []
        choices = []
        for line in lines:
            m = re.match(r"^\s*-\s+([A-D])\)\s*(.+)$", line)
            if m:
                choices.append((m.group(1), m.group(2).strip()))
            elif line.strip().startswith("- "):
                # bullet that isn't A)-D) → end of this question (probably hint)
                break
            elif re.match(r"^\*?Hint:", line.strip()):
                # hint line — stop collecting stem
                break
            else:
                if choices:
                    # already collecting choices; stop on non-choice line
                    break
                stem_lines.append(line)
        stem = " ".join(s.strip() for s in stem_lines if s.strip()).strip()
        if stem and choices:
            qs.append({"num": qnum, "stem": stem, "choices": choices})
    return qs


def extract_handout(body: str) -> dict | None:
    sec = re.search(r"## Handout-Style Problem\s*\n(.+?)(?=^## |\Z)", body, flags=re.DOTALL | re.MULTILINE)
    if not sec:
        return None
    text = sec.group(1).strip()
    # Title: starts with "**Problem N.A — Title.**"
    m = re.match(r"\*\*Problem ([\d.A-Za-z]+)\s+—\s+([^.]+?)\.\*\*\s*(.+)", text, flags=re.DOTALL)
    if not m:
        return {"label": "Problem", "title": "", "body": text}
    return {
        "label": f"Problem {m.group(1)}",
        "title": m.group(2).strip(),
        "body": m.group(3).strip(),
    }


def extract_answers(body: str, ch: int) -> dict:
    sec = re.search(rf"## Answer Key — Chapter {ch}\s*\n(.+?)(?=^# |^---|\Z)", body, flags=re.DOTALL | re.MULTILINE)
    if not sec:
        return {"mc_line": "", "handout": ""}
    txt = sec.group(1)
    mc_match = re.search(r"\*\*MC:\*\*\s*(.+?)(?=\n\*\*\d|\n\n|\Z)", txt, flags=re.DOTALL)
    handout_match = re.search(rf"\*\*{ch}\.A:\*\*\s*(.+?)(?=\n\*\*|\n\n|\Z)", txt, flags=re.DOTALL)
    return {
        "mc_line": mc_match.group(1).strip() if mc_match else "",
        "handout": handout_match.group(1).strip() if handout_match else "",
    }


# ---------- Generate HTML ----------
def md_inline(text: str) -> str:
    """Minimal markdown → HTML inline transforms (bold + italic + code)."""
    # Strip image syntax — the figures aren't in this repo, and slides
    # are too small for them anyway. Keep alt text as a parenthetical.
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", text)
    # Strip explicit link syntax → keep the link text only
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Protect markdown-escaped asterisks (e.g. P\* meaning a literal *)
    text = text.replace(r"\*", "\x01")
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # restore HTML entities we want to keep
    text = text.replace("&amp;mdash;", "&mdash;").replace("&amp;ndash;", "&ndash;")
    text = text.replace("&amp;hellip;", "&hellip;")
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # italic (only when there's at least one non-whitespace char inside)
    text = re.sub(r"(?<!\*)\*(?=[^*\s])([^\n*]+?)\*(?!\*)", r"<em>\1</em>", text)
    # inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Restore literal asterisks
    text = text.replace("\x01", "*")
    # Collapse whitespace runs (image strip can leave gaps)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def mc_answer_letter(ch: int, mc_num: int, answers: dict) -> str:
    """Parse '1-A, 2-B, 3-B, 4-B, 5-B' style → return the letter for mc_num."""
    line = answers.get("mc_line", "")
    m = re.search(rf"{mc_num}-([A-D])", line)
    return m.group(1) if m else "?"


def mc_explanation(ch: int, mc_num: int, answers: dict, qs: list[dict]) -> str:
    """Try to pull a per-question explanation from the answer line.
    Most chapters compress all 5 onto one line; explanations are usually
    written next to the letter, e.g. "2-A (TS = ...)" — extract that.
    Otherwise we just leave a blank."""
    line = answers.get("mc_line", "")
    m = re.search(rf"{mc_num}-[A-D]\s*\(([^)]+)\)", line)
    return m.group(1) if m else ""


def render_chapter_subslides(ch: int, data: dict, chapter_title_pill_text: str) -> str:
    """Build all 6 sub-slide <section> blocks for a chapter."""
    blocks = []
    short_title = chapter_title_pill_text  # e.g., "Economics Is Everywhere"

    # 5 MC sub-slides
    for q in data["mc"]:
        n = q["num"]
        ans_letter = mc_answer_letter(ch, n, data["answers"])
        ans_note = mc_explanation(ch, n, data["answers"], data["mc"])

        choice_cards = []
        for letter, ctext in q["choices"]:
            is_correct = letter == ans_letter
            border = "var(--success-color)" if is_correct else "var(--accent-color)"
            choice_cards.append(
                f'<div class="detail-card" style="border-left-color: {border};">\n'
                f'  <p style="font-size: 12pt;"><strong>{letter})</strong> {md_inline(ctext)}</p>\n'
                f'</div>'
            )
        choices_html = "\n         ".join(choice_cards)

        explanation_html = ""
        if ans_note:
            explanation_html = f'<p style="font-size: 11pt; color: var(--muted-color); margin-top: 6px;">{md_inline(ans_note)}</p>'

        block = f"""
    <!-- ============================================ -->
    <!-- Ch{ch:02d} · MC #{n}                                  -->
    <!-- ============================================ -->
    <section id="ch{ch:02d}-mc{n}">
     <div class="chapter-header" style="margin-bottom: 14px; padding-bottom: 8px;">
      <div class="chapter-num" style="font-size: 16pt; padding: 4px 10px;">{ch:02d}</div>
      <div class="chapter-title-pill" style="font-size: 14pt; padding: 6px 0;">{short_title} &middot; Sample MC #{n}</div>
     </div>
     <div class="detail-card" style="font-size: 13pt; padding: 12px 16px; margin-bottom: 16px; border-left-color: var(--primary-color);">
      <p style="font-size: 13pt;"><strong>Q{n}.</strong> {md_inline(q['stem'])}</p>
     </div>
     <div class="detail-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
         {choices_html}
     </div>
     <div class="tip-box fragment fade-up" style="margin-top: 18px;">
      <span class="label">Answer</span>
      <p style="font-size: 14pt;"><strong>{ans_letter}</strong></p>
      {explanation_html}
     </div>
    </section>"""
        blocks.append(block)

    # 1 handout problem sub-slide
    h = data["handout"]
    if h:
        # parse body into intro + parts
        body = h["body"]
        # parts look like: "(a) ..." separated by newlines
        # Split keeping the (X) markers
        intro_match = re.match(r"(.+?)(?=\(a\))", body, flags=re.DOTALL)
        intro = intro_match.group(1).strip() if intro_match else ""
        if intro_match:
            parts_text = body[intro_match.end():]
        else:
            parts_text = body
        parts = re.findall(r"\(([a-e])\)\s*(.+?)(?=\([a-e]\)|\Z)", parts_text, flags=re.DOTALL)

        parts_cards = []
        for letter, ptext in parts:
            ptext = re.sub(r"\s+", " ", ptext).strip()
            parts_cards.append(
                f'<div class="detail-card" style="font-size: 11.5pt;">\n'
                f'  <p style="font-size: 11.5pt;"><strong>({letter})</strong> {md_inline(ptext)}</p>\n'
                f'</div>'
            )
        parts_html = "\n         ".join(parts_cards)

        ans_text = data["answers"].get("handout", "")
        # Trim long answer to fit slide; render compactly
        ans_html = md_inline(ans_text[:900]) if ans_text else "<em>(see review guide for full solution)</em>"

        block = f"""
    <!-- ============================================ -->
    <!-- Ch{ch:02d} · Handout-style Problem               -->
    <!-- ============================================ -->
    <section id="ch{ch:02d}-handout">
     <div class="chapter-header" style="margin-bottom: 12px; padding-bottom: 8px;">
      <div class="chapter-num" style="font-size: 16pt; padding: 4px 10px;">{ch:02d}</div>
      <div class="chapter-title-pill" style="font-size: 14pt; padding: 6px 0;">{short_title} &middot; {h['label']}: {h['title']}</div>
     </div>
     <p style="font-size: 12pt; margin-bottom: 12px; line-height: 1.45;">{md_inline(intro)}</p>
     <div class="detail-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
         {parts_html}
     </div>
     <div class="tip-box fragment fade-up" style="margin-top: 14px;">
      <span class="label">Answer Sketch</span>
      <p style="font-size: 11pt; line-height: 1.45;">{ans_html}</p>
     </div>
    </section>"""
        blocks.append(block)

    return "\n".join(blocks)


# ---------- Splice into index.html ----------
def splice_chapter_into_html(html: str, ch: int, sub_blocks: str) -> str:
    """Wrap the existing <section id="chNN">…</section> in an outer
    <section> wrapper and append the sub-slide blocks after it.

    Idempotent: if the chapter is already wrapped (detected by an
    outer marker `<!-- WRAP-CH{ch:02d} -->`), strip and rebuild.
    """
    marker = f"<!-- WRAP-CH{ch:02d} -->"
    end_marker = f"<!-- /WRAP-CH{ch:02d} -->"

    # If already wrapped, find the wrapper span and replace its contents.
    if marker in html:
        pattern = rf"{re.escape(marker)}.*?{re.escape(end_marker)}"
        # Need to reconstruct just the flow-chart inner <section>, plus new subs
        m = re.search(rf'<section id="ch{ch:02d}".*?</section>', html, flags=re.DOTALL)
        if not m:
            return html
        inner = m.group(0)
        new_block = f"{marker}\n    <section>\n     {inner}\n{sub_blocks}\n    </section>\n    {end_marker}"
        return re.sub(pattern, new_block, html, flags=re.DOTALL)

    # First-time wrapping: find the standalone <section id="chNN" …> … </section>
    # in the slides flow and wrap it with the new outer container.
    pat = rf'(<section id="ch{ch:02d}".*?</section>)'
    m = re.search(pat, html, flags=re.DOTALL)
    if not m:
        print(f"  !! could not find <section id=\"ch{ch:02d}\"> in index.html")
        return html
    inner = m.group(1)
    wrapped = f"{marker}\n    <section>\n     {inner}\n{sub_blocks}\n    </section>\n    {end_marker}"
    return html.replace(inner, wrapped)


def main():
    print("Reading review-guide markdown…")
    md = GUIDE.read_text()
    chapters = parse_review_guide(md)
    for ch, d in chapters.items():
        print(f"  Ch{ch}: {len(d['mc'])} MC, handout={'yes' if d['handout'] else 'no'}, "
              f"answers_mc={'yes' if d['answers'].get('mc_line') else 'no'}")

    chapter_titles = {
        1: "Economics Is Everywhere",
        2: "Thinking Like an Economist",
        3: "Gains from Trade",
        4: "Supply, Demand &amp; Market Equilibrium",
        5: "Efficiency and Welfare",
        6: "Elasticity",
        7: "Government Intervention",
        8: "Consumer Choice &amp; Decision-Making",
    }

    print("\nReading current index.html…")
    html = INDEX.read_text()

    for ch in range(1, 9):
        if ch not in chapters:
            print(f"  Ch{ch}: not found in MD — skipping")
            continue
        sub_blocks = render_chapter_subslides(ch, chapters[ch], chapter_titles[ch])
        html = splice_chapter_into_html(html, ch, sub_blocks)
        print(f"  Ch{ch}: spliced {len(chapters[ch]['mc']) + (1 if chapters[ch]['handout'] else 0)} sub-slides")

    print(f"\nWriting index.html ({len(html):,} chars)…")
    INDEX.write_text(html)
    print("Done.")


if __name__ == "__main__":
    main()
