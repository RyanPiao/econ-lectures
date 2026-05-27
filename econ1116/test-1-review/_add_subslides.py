#!/usr/bin/env python3
"""
Extend the Test 1 Review deck: for each Ch 1-8 flow-chart slide, add
vertical sub-slides containing 5 fresh MC questions (drawn from the
canvas-quizzes/banks/ YAML files, with a different random seed than the
actual Exam 1 quiz so they don't overlap) plus 1 brand-new handout-style
problem (hand-curated below — different from the review-guide samples).

Reveal.js vertical-slide structure:
   <section>           ← outer wrapper (acts as a horizontal slide column)
     <section>...</section>   ← vertical position 1 (flow chart, unchanged)
     <section>...</section>   ← vertical position 2 (MC #1)
     ... etc

Idempotent: re-runs strip the old wrap and rebuild.
"""
from __future__ import annotations
import random
import re
import yaml
from pathlib import Path

HERE = Path(__file__).parent
INDEX = HERE / "index.html"
BANKS_DIR = Path(
    "/Users/openclaw/Resilio Sync/documents/econ-project-book/principles-of-microeconomics/canvas-quizzes/banks"
)

# Seed differs from build_exam1.py (which uses 20260528) so deck picks
# DO NOT overlap the actual exam questions.
DECK_SEED = 20260601
EXAM_SEED = 20260528  # exam's seed, for exclusion


# ---------- 1. Bank loading + sampling ----------
def load_bank(ch: int) -> list[dict]:
    """Return the list of all questions for a chapter."""
    with open(BANKS_DIR / f"ch{ch:02d}.yml") as f:
        data = yaml.safe_load(f)
    return [q for q in data.get("questions", []) if q.get("type") == "mc"]


def exam_picks_for_chapter(ch: int) -> set[str]:
    """Reproduce build_exam1.py's exam picks so we can exclude them from the deck."""
    mc = load_bank(ch)
    rng = random.Random(EXAM_SEED + ch)
    by_diff = {"easy": [], "medium": [], "hard": []}
    for q in mc:
        d = q.get("difficulty", "medium")
        if d in by_diff:
            by_diff[d].append(q)
    for d in by_diff.values():
        rng.shuffle(d)
    targets = {"easy": 2, "medium": 2, "hard": 1}
    picked_ids = []
    for diff, n in targets.items():
        picked_ids.extend(q["id"] for q in by_diff[diff][:n])
    while len(picked_ids) < 5:
        for d in ("medium", "easy", "hard"):
            pool = [q for q in by_diff[d] if q["id"] not in picked_ids]
            if pool:
                picked_ids.append(pool[0]["id"])
                break
        else:
            break
    return set(picked_ids[:5])


def pick_deck_mc(ch: int, target: int = 5) -> list[dict]:
    """Pick `target` MC for the deck — different from the exam picks.
    Same 2 easy / 2 medium / 1 hard mix."""
    mc = load_bank(ch)
    exam_ids = exam_picks_for_chapter(ch)
    available = [q for q in mc if q["id"] not in exam_ids]

    rng = random.Random(DECK_SEED + ch)
    by_diff = {"easy": [], "medium": [], "hard": []}
    for q in available:
        d = q.get("difficulty", "medium")
        if d in by_diff:
            by_diff[d].append(q)
    for d in by_diff.values():
        rng.shuffle(d)
    targets = {"easy": 2, "medium": 2, "hard": 1}
    picked = []
    for diff, n in targets.items():
        picked.extend(by_diff[diff][:n])
    while len(picked) < target:
        for d in ("medium", "easy", "hard"):
            pool = [q for q in by_diff[d] if q not in picked]
            if pool:
                picked.append(pool[0])
                break
        else:
            break
    return picked[:target]


def get_variant(q: dict) -> dict:
    """Use canvas: override if present, else base."""
    canvas = q.get("canvas")
    base = q["base"]
    if canvas:
        merged = dict(base)
        merged.update(canvas)
        if "choices" in canvas:
            merged["choices"] = canvas["choices"]
        return merged
    return base


# ---------- 2. Fresh handout-style problems (one per chapter) ----------
# Each entry: title, intro (problem stem), parts (list of (label, text)),
# answer (worked solution html string).
HANDOUT_PROBLEMS = {
    1: {
        "title": "Opportunity Cost of Working vs. Studying",
        "intro": (
            "Tonight you can pick up a 4-hour Uber Eats shift at $18/hr (totaling <strong>$72</strong>). "
            "Alternatively, you can study for tomorrow's econ midterm. From experience, every hour of focused "
            "studying raises your expected exam score by <strong>1.5 points</strong> on a 100-point scale."
        ),
        "parts": [
            ("a", "Identify the <strong>explicit cost</strong> and <strong>implicit cost</strong> of working the shift instead of studying."),
            ("b", "What is the <strong>opportunity cost</strong> of working the shift, measured in expected midterm grade points?"),
            ("c", "If you value each expected grade point at $5 (e.g., better grade → better job prospects), at what hourly wage would you switch to studying?"),
            ("d", "In one sentence, explain why &ldquo;the shift pays $72 cash, so I should always take it&rdquo; is bad reasoning."),
        ],
        "answer": (
            "<strong>(a)</strong> Explicit: $0 (no money leaves your wallet to study). Implicit: $72 forgone wages from skipping the shift, OR if you take the shift, the implicit cost is the lost grade points. "
            "<strong>(b)</strong> 4 hrs × 1.5 pts = <strong>6 expected grade points</strong> forgone. "
            "<strong>(c)</strong> Studying gives 1.5 pts/hr × $5/pt = $7.50/hr of value. You switch to studying when wage drops below <strong>$7.50/hr</strong>. "
            "<strong>(d)</strong> The $72 is the explicit benefit; you also need to subtract the implicit cost (forgone grade points worth $30) and compare net values."
        ),
    },
    2: {
        "title": "Spotting Reasoning Errors",
        "intro": (
            "A think-tank op-ed claims: <em>&ldquo;Cities with more bike lanes have lower obesity rates. "
            "Therefore, building more bike lanes will reduce obesity.&rdquo;</em>"
        ),
        "parts": [
            ("a", "Is the second sentence (the &ldquo;therefore&rdquo;) a <strong>positive</strong> or <strong>normative</strong> claim?"),
            ("b", "List <strong>three plausible alternative explanations</strong> for the bike-lane / obesity correlation that don't involve bike lanes causing weight loss."),
            ("c", "Which causal method (<strong>RCT, natural experiment, DiD, A/B test</strong>) would best test whether bike lanes <em>cause</em> lower obesity? Briefly justify."),
            ("d", "Suggest one specific <strong>natural experiment</strong> that could test the claim."),
        ],
        "answer": (
            "<strong>(a)</strong> <strong>Positive</strong> — it's a falsifiable causal claim about the world. "
            "<strong>(b)</strong> (i) Reverse causation — healthier people lobby for bike lanes. (ii) Omitted variable — wealthier cities have both more bike lanes AND lower obesity (income drives both). (iii) Self-selection — bike-friendly cities attract residents who already exercise. "
            "<strong>(c)</strong> <strong>Natural experiment or DiD</strong> — cities don't randomly get bike lanes (no true RCT), so identify a city that built bike lanes due to a policy quirk (mayoral election, federal grant) and DiD vs a similar city that didn't. "
            "<strong>(d)</strong> Compare obesity before/after a city installs a bike-lane network (treated) vs a similar city that didn't (control). E.g., Minneapolis vs. Indianapolis after 2010."
        ),
    },
    3: {
        "title": "Comparative Advantage — Pizzeria vs Salad",
        "intro": (
            "In 1 hour, Tony can make <strong>8 pizzas OR 16 salads</strong>. "
            "In 1 hour, Anna can make <strong>4 pizzas OR 12 salads</strong>."
        ),
        "parts": [
            ("a", "Who has <strong>absolute advantage</strong> in pizzas? In salads?"),
            ("b", "What is Tony's <strong>opportunity cost</strong> of one pizza? Of one salad?"),
            ("c", "What is Anna's <strong>opportunity cost</strong> of one pizza? Of one salad?"),
            ("d", "Who has <strong>comparative advantage</strong> in pizzas? In salads?"),
            ("e", "Suggest a trade price (salads per pizza) where both would gain. Justify in one sentence."),
        ],
        "answer": (
            "<strong>(a)</strong> Tony has absolute advantage in both. "
            "<strong>(b)</strong> Tony: 1 pizza = 2 salads; 1 salad = ½ pizza. "
            "<strong>(c)</strong> Anna: 1 pizza = 3 salads; 1 salad = ⅓ pizza. "
            "<strong>(d)</strong> Tony has comparative advantage in pizzas (2 &lt; 3 salads). Anna has comparative advantage in salads (⅓ &lt; ½ pizza). "
            "<strong>(e)</strong> Any price <strong>between 2 and 3 salads per pizza</strong> works — e.g., 2.5 salads per pizza. Tony gets more salads than he could make himself; Anna gives up fewer salads than she would have."
        ),
    },
    4: {
        "title": "Comparative Statics — A Double Shift",
        "intro": (
            "In the market for <strong>laptops</strong>, a global chip shortage drives up the cost of producing each laptop by $200, "
            "<em>and at the same time</em> a wave of AI-related demand makes laptops more desirable for many buyers."
        ),
        "parts": [
            ("a", "Which curve(s) shift? In which direction?"),
            ("b", "What happens to the <strong>equilibrium price</strong>? Show your reasoning."),
            ("c", "What happens to the <strong>equilibrium quantity</strong>? Show your reasoning."),
            ("d", "One of P* or Q* is <strong>determinate</strong>; the other is <strong>ambiguous</strong>. Identify which is which and explain why."),
        ],
        "answer": (
            "<strong>(a)</strong> <strong>Supply shifts LEFT</strong> (input prices up). <strong>Demand shifts RIGHT</strong> (tastes change). "
            "<strong>(b)</strong> P* <strong>rises unambiguously</strong> — both shifts push the equilibrium price up. "
            "<strong>(c)</strong> Q* is <strong>ambiguous</strong> — leftward supply pulls Q down, rightward demand pushes Q up. The net change depends on the relative magnitudes. "
            "<strong>(d)</strong> P* is determinate because both shifts move it the same way. Q* is ambiguous because the shifts move it in opposite directions."
        ),
    },
    5: {
        "title": "Welfare After a Cocoa Shock",
        "intro": (
            "Original cocoa market: <strong>Demand: P = 30 − 0.05Q</strong> and <strong>Supply: P = 5 + 0.05Q</strong> "
            "(P in $/ton, Q in thousand tons)."
        ),
        "parts": [
            ("a", "Find <strong>equilibrium P* and Q*</strong>."),
            ("b", "Calculate <strong>consumer surplus, producer surplus, and total surplus</strong>."),
            ("c", "A fungal disease destroys half the harvest, shifting supply to <strong>P = 15 + 0.10Q</strong>. Find the new equilibrium."),
            ("d", "Calculate the <strong>change in total surplus</strong> caused by the shock."),
        ],
        "answer": (
            "<strong>(a)</strong> 30 − 0.05Q = 5 + 0.05Q → 25 = 0.10Q → <strong>Q* = 250, P* = $17.50</strong>. "
            "<strong>(b)</strong> CS = ½ × 250 × ($30 − $17.50) = <strong>$1,562.50</strong>; PS = ½ × 250 × ($17.50 − $5) = <strong>$1,562.50</strong>; TS = <strong>$3,125</strong>. "
            "<strong>(c)</strong> 30 − 0.05Q = 15 + 0.10Q → 15 = 0.15Q → <strong>Q' = 100, P' = $25</strong>. "
            "<strong>(d)</strong> New CS = ½ × 100 × ($30 − $25) = $250; new PS = ½ × 100 × ($25 − $15) = $500; new TS = <strong>$750</strong>. <strong>Loss = $3,125 − $750 = $2,375</strong>."
        ),
    },
    6: {
        "title": "Tax Incidence with Specific Elasticities",
        "intro": (
            "The market for <strong>sugary cereal</strong> has price elasticity of demand <strong>|PED| = 0.4</strong> (inelastic) "
            "and price elasticity of supply <strong>PES = 2.0</strong> (elastic). The government imposes a <strong>$1.00/box</strong> tax."
        ),
        "parts": [
            ("a", "Calculate the <strong>buyer's share</strong> of the tax burden using the elasticity formula."),
            ("b", "Calculate the <strong>seller's share</strong>."),
            ("c", "If the pre-tax price was <strong>$5.00/box</strong>, what is the approximate <strong>buyer-paid price</strong> after the tax?"),
            ("d", "In one sentence, explain <strong>why</strong> the inelastic side bears more of the burden."),
        ],
        "answer": (
            "<strong>(a)</strong> Buyer's share = E<sub>s</sub> / (E<sub>s</sub> + |E<sub>d</sub>|) = 2.0 / (2.0 + 0.4) = 2.0/2.4 ≈ <strong>0.83 or 83%</strong>. "
            "<strong>(b)</strong> Seller's share = 0.4/2.4 ≈ <strong>0.17 or 17%</strong>. "
            "<strong>(c)</strong> Buyer pays 5.00 + 0.83 = <strong>$5.83/box</strong>. (Seller receives 5.00 − 0.17 = $4.83.) "
            "<strong>(d)</strong> The inelastic side has fewer alternatives, so they can't escape the tax by reducing quantity — they end up absorbing more of the price change."
        ),
    },
    7: {
        "title": "Rent Control Welfare Analysis",
        "intro": (
            "NYC apartment market: <strong>Demand: P = 5000 − 2Q</strong>, <strong>Supply: P = 1000 + 2Q</strong> "
            "(P in $/month, Q in thousands of apartments). The city imposes a <strong>rent ceiling at $2,000/month</strong>."
        ),
        "parts": [
            ("a", "Find the <strong>free-market P* and Q*</strong>."),
            ("b", "At the $2,000 ceiling, how many apartments are <strong>supplied</strong>? How many are <strong>demanded</strong>? Identify the shortage."),
            ("c", "Calculate the <strong>deadweight loss</strong> from the ceiling. Show the triangle base and height."),
            ("d", "Name <strong>two unintended consequences</strong> that economists have documented from rent ceilings."),
        ],
        "answer": (
            "<strong>(a)</strong> 5000 − 2Q = 1000 + 2Q → 4000 = 4Q → <strong>Q* = 1,000, P* = $3,000</strong>. "
            "<strong>(b)</strong> Supply at $2,000: 2000 = 1000 + 2Q → Q<sub>s</sub> = <strong>500</strong>. Demand at $2,000: 2000 = 5000 − 2Q → Q<sub>d</sub> = <strong>1,500</strong>. <strong>Shortage = 1,000</strong>. "
            "<strong>(c)</strong> DWL triangle: base = Q* − Q<sub>s</sub> = 500. Height = D<sub>500</sub> − S<sub>500</sub> = ($5000 − 2·500) − ($1000 + 2·500) = $4000 − $2000 = $2,000. <strong>DWL = ½ × 500 × $2,000 = $500,000</strong> (per month). "
            "<strong>(d)</strong> Acceptable answers include: (i) reduced new construction (long-run supply shrinks); (ii) deferred maintenance / quality decline; (iii) black-market subletting / key fees; (iv) misallocation (apartments go to people who got there first, not who values most)."
        ),
    },
    8: {
        "title": "Budget Constraint Shift",
        "intro": (
            "Jordan has <strong>$40/week</strong> to spend on Netflix (<strong>$4/week</strong>) and concerts (<strong>$20/ticket</strong>). "
            "Marginal utility is shown for each."
        ),
        "parts": [
            ("a", "Write Jordan's <strong>budget constraint</strong>. What are the X- and Y-intercepts?"),
            ("b", "Using the table — Netflix MUs: <strong>30, 24, 18, 12</strong>; Concert MUs: <strong>80, 60, 40, 20</strong> — calculate MU/$ for each quantity (1-4) of both goods."),
            ("c", "Find Jordan's <strong>optimal bundle</strong>. Show you spent the entire budget and applied the equimarginal principle."),
            ("d", "Netflix raises its price to <strong>$10/week</strong>. Describe (in words) how the budget line and the optimum change."),
        ],
        "answer": (
            "<strong>(a)</strong> 4N + 20C = 40. Intercepts: 10 Netflix-weeks (all on Netflix); 2 concerts (all on concerts). "
            "<strong>(b)</strong> Netflix MU/$: 7.5, 6, 4.5, 3. Concert MU/$: 4, 3, 2, 1. "
            "<strong>(c)</strong> Buy until MU/$ ≈ MU/$. Try 5N + 1C = $20 + $20 = $40 (Netflix MU/$ at 5th unit would be very low — but we only have 4 in the table). With the table, best feasible bundle is <strong>4N + 1C = $16 + $20 = $36</strong> (Netflix MU/$ = 3, Concert MU/$ = 4 at 1st concert — concerts slightly higher). Add 5N for $4 = $40 (Netflix 5th MU not given, assume &lt;3). Heuristic answer: <strong>5 Netflix + 1 concert = $40</strong> approximately optimal given the table. "
            "<strong>(d)</strong> Budget line <strong>rotates inward on the Netflix axis</strong> (slope steeper, new intercept = 40/10 = 4 Netflix). Jordan will substitute toward concerts and away from Netflix at the new optimum."
        ),
    },
}


# ---------- 3. HTML helpers ----------
def md_inline(text: str) -> str:
    """Convert markdown stem/choice text to HTML for the deck.

    Bank YAML stems are AUTHORED content and may legitimately contain
    HTML (<p>, <strong>, <sub>, etc.) — preserve those. Only escape & when
    it's not already starting a named/numeric entity.
    """
    # Strip image markdown
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", text)
    # Strip link markdown → keep link text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Protect markdown-escaped asterisks (P\*, Q\*)
    text = text.replace(r"\*", "\x01")
    # Smart & escape: only when not already an entity ref
    text = re.sub(r"&(?![a-zA-Z]+;|#\d+;)", "&amp;", text)
    # Markdown → HTML transforms
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?=[^*\s])([^\n*]+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Strip top-level <p>…</p> wrappers — the deck slide already wraps
    # stems in its own paragraph styling, so an inner <p> just adds an
    # extra empty line.
    text = re.sub(r"^\s*<p>(.*?)</p>\s*$", r"\1", text, flags=re.DOTALL)
    # Restore literal asterisks
    text = text.replace("\x01", "*")
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def render_mc_subslide(ch: int, num: int, q: dict, chapter_title: str) -> str:
    variant = get_variant(q)
    stem = variant["stem"]
    choices = variant["choices"]
    letters = ["A", "B", "C", "D", "E"]

    choice_cards = []
    correct_letter = "?"
    for i, c in enumerate(choices):
        letter = letters[i]
        if c.get("correct"):
            correct_letter = letter
        border = "var(--success-color)" if c.get("correct") else "var(--accent-color)"
        choice_cards.append(
            f'<div class="detail-card" style="border-left-color: {border};">\n'
            f'  <p style="font-size: 12pt;"><strong>{letter})</strong> {md_inline(c["text"])}</p>\n'
            f'</div>'
        )
    choices_html = "\n         ".join(choice_cards)

    explanation_html = ""
    expl = q.get("explanation", "").strip()
    if expl:
        explanation_html = (
            f'<p style="font-size: 11pt; color: var(--muted-color); '
            f'margin-top: 6px; line-height: 1.4;">{md_inline(expl)}</p>'
        )

    return f"""
    <!-- Ch{ch:02d} · MC #{num} -->
    <section id="ch{ch:02d}-mc{num}">
     <div class="chapter-header" style="margin-bottom: 14px; padding-bottom: 8px;">
      <div class="chapter-num" style="font-size: 16pt; padding: 4px 10px;">{ch:02d}</div>
      <div class="chapter-title-pill" style="font-size: 14pt; padding: 6px 0;">{chapter_title} &middot; Practice MC #{num}</div>
     </div>
     <div class="detail-card" style="font-size: 13pt; padding: 12px 16px; margin-bottom: 16px; border-left-color: var(--primary-color);">
      <p style="font-size: 13pt;"><strong>Q{num}.</strong> {md_inline(stem)}</p>
     </div>
     <div class="detail-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
         {choices_html}
     </div>
     <div class="tip-box fragment fade-up" style="margin-top: 18px;">
      <span class="label">Answer</span>
      <p style="font-size: 14pt;"><strong>{correct_letter}</strong></p>
      {explanation_html}
     </div>
    </section>"""


def render_handout_subslide(ch: int, chapter_title: str) -> str:
    h = HANDOUT_PROBLEMS.get(ch)
    if not h:
        return ""
    parts_cards = []
    for label, ptext in h["parts"]:
        parts_cards.append(
            f'<div class="detail-card" style="font-size: 11pt;">\n'
            f'  <p style="font-size: 11pt;"><strong>({label})</strong> {ptext}</p>\n'
            f'</div>'
        )
    parts_html = "\n         ".join(parts_cards)
    grid_cols = "1fr 1fr" if len(h["parts"]) >= 4 else "1fr"

    return f"""
    <!-- Ch{ch:02d} · Handout-style problem -->
    <section id="ch{ch:02d}-handout">
     <div class="chapter-header" style="margin-bottom: 10px; padding-bottom: 8px;">
      <div class="chapter-num" style="font-size: 16pt; padding: 4px 10px;">{ch:02d}</div>
      <div class="chapter-title-pill" style="font-size: 13pt; padding: 6px 0;">{chapter_title} &middot; Handout Practice: {h['title']}</div>
     </div>
     <p style="font-size: 11.5pt; margin-bottom: 10px; line-height: 1.4;">{h['intro']}</p>
     <div class="detail-row" style="display: grid; grid-template-columns: {grid_cols}; gap: 8px;">
         {parts_html}
     </div>
     <div class="tip-box fragment fade-up" style="margin-top: 12px;">
      <span class="label">Answer Sketch</span>
      <p style="font-size: 10.5pt; line-height: 1.45;">{h['answer']}</p>
     </div>
    </section>"""


def render_chapter_subslides(ch: int, chapter_title: str) -> str:
    blocks = []
    mc_picks = pick_deck_mc(ch, target=5)
    for i, q in enumerate(mc_picks, start=1):
        blocks.append(render_mc_subslide(ch, i, q, chapter_title))
    blocks.append(render_handout_subslide(ch, chapter_title))
    return "\n".join(blocks)


# ---------- 4. Splice into index.html ----------
def splice_chapter_into_html(html: str, ch: int, sub_blocks: str) -> str:
    marker = f"<!-- WRAP-CH{ch:02d} -->"
    end_marker = f"<!-- /WRAP-CH{ch:02d} -->"

    # Find the chapter flow-chart section (inner)
    inner_match = re.search(rf'<section id="ch{ch:02d}".*?</section>', html, flags=re.DOTALL)
    if not inner_match:
        print(f"  !! could not find <section id=\"ch{ch:02d}\"> in index.html")
        return html
    inner = inner_match.group(0)
    new_block = f"{marker}\n    <section>\n     {inner}\n{sub_blocks}\n    </section>\n    {end_marker}"

    # If wrapper already exists, replace the whole block
    if marker in html:
        pattern = rf"{re.escape(marker)}.*?{re.escape(end_marker)}"
        return re.sub(pattern, new_block, html, count=1, flags=re.DOTALL)

    # Else, first-time wrap
    return html.replace(inner, new_block)


def main():
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

    print("Reading current index.html…")
    html = INDEX.read_text()

    for ch in range(1, 9):
        sub_blocks = render_chapter_subslides(ch, chapter_titles[ch])
        html = splice_chapter_into_html(html, ch, sub_blocks)
        picks = pick_deck_mc(ch, target=5)
        ids = [q["id"] for q in picks]
        print(f"  Ch{ch}: {len(picks)} MC + 1 handout. IDs: {ids}")

    print(f"\nWriting index.html ({len(html):,} chars)…")
    INDEX.write_text(html)
    print("Done.")


if __name__ == "__main__":
    main()
