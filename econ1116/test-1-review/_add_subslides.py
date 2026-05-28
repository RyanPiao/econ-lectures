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

# Bank questions reference figures with paths like /images/quiz/ch04/foo.png.
# Those images are hosted on the ebook's Vercel deployment, so we just
# prefix the path to get a working URL inside the slide.
EBOOK_BASE = "https://econ-1116-microeconomics-lac.vercel.app"

# Bank IDs to explicitly exclude from deck picks (e.g. questions whose
# subject overlaps another deck question or instructor preference). Keyed
# by chapter for quick scanning.
DECK_EXCLUDE: dict[int, set[str]] = {
    5: {"q075-carbon-tax-welfare-graph"},  # instructor pref — swap for another Ch 5 Q
}

# Manual image overrides for bank questions that reference a "diagram" or
# "figure" in the stem but don't have an image field of their own. Keyed by
# question id; value is the figure path (absolute Vercel path, joined with
# EBOOK_BASE at render time).
IMAGE_OVERRIDES: dict[str, str] = {
    # Q5.2 — "Government tax revenue from a per-unit tax appears on a
    # supply-and-demand diagram as a:" — show the tax wedge chart so the
    # rectangle answer is grounded in the picture students are reading.
    "q028-tax-revenue-rectangle": "/images/quiz/ch05/tax-wedge.png",
}


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
    """Pick `target` MC for the deck — different from the exam picks AND
    from the per-chapter DECK_EXCLUDE set. Same 2 easy / 2 medium / 1 hard mix."""
    mc = load_bank(ch)
    exam_ids = exam_picks_for_chapter(ch)
    excluded = exam_ids | DECK_EXCLUDE.get(ch, set())
    available = [q for q in mc if q["id"] not in excluded]

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
        "title": "Read CS, PS, and Total Surplus from the Diagram",
        "image": "figures/ch5-handout-donuts.png",
        "intro": (
            "The diagram shows the Cambridge artisanal-donut market. The shaded yellow region is "
            "<strong>consumer surplus</strong>; the shaded green region is <strong>producer surplus</strong>. "
            "Read all values directly from the figure — no algebra needed."
        ),
        "parts": [
            ("a", "From the diagram, identify <strong>P*</strong> and <strong>Q*</strong>."),
            ("b", "Read the <strong>demand intercept</strong> (the highest price any buyer is willing to pay). Then calculate <strong>consumer surplus</strong> using the triangle area formula."),
            ("c", "Read the <strong>supply intercept</strong> (the lowest price any seller will accept). Then calculate <strong>producer surplus</strong>."),
            ("d", "Calculate <strong>total surplus</strong>."),
            ("e", "Suppose a $4 per-dozen tax is imposed. On the diagram (in your head), where would the <strong>deadweight loss triangle</strong> appear? Describe it in one sentence — no math required."),
        ],
        "answer": (
            "<strong>(a)</strong> Read directly: <strong>P* = $8, Q* = 40 dozen</strong>. "
            "<strong>(b)</strong> Demand intercept = <strong>$12</strong>. CS triangle = ½ × 40 × ($12 − $8) = ½ × 40 × $4 = <strong>$80</strong>. "
            "<strong>(c)</strong> Supply intercept = <strong>$4</strong>. PS triangle = ½ × 40 × ($8 − $4) = ½ × 40 × $4 = <strong>$80</strong>. "
            "<strong>(d)</strong> TS = CS + PS = $80 + $80 = <strong>$160</strong>. "
            "<strong>(e)</strong> The $4 tax would create a wedge between the buyer's price and the seller's price; the DWL triangle sits between Q at the new (lower) equilibrium and Q* = 40, bounded above by D and below by S. Its area depends on the new quantity, but conceptually it's the lost surplus from trades that no longer happen."
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
        "title": "Read the Rent Ceiling Diagram",
        "image": "figures/ch7-handout-rent-ceiling.png",
        "intro": (
            "The diagram shows the NYC apartment market with a binding <strong>$2,000/month rent ceiling</strong>. "
            "The orange bar marks the shortage; the pink triangle marks the deadweight loss. "
            "Read every value off the figure — no algebra required."
        ),
        "parts": [
            ("a", "From the diagram, identify the <strong>free-market equilibrium</strong> P* and Q*."),
            ("b", "Read Q_s and Q_d at the $2,000 ceiling. What is the <strong>shortage</strong>?"),
            ("c", "Read the dimensions of the <strong>DWL triangle</strong> (base = Q* − Q_s; height = vertical wedge between D and S at Q_s). Calculate its area."),
            ("d", "In one sentence, name <strong>two unintended consequences</strong> economists have documented from rent ceilings."),
        ],
        "answer": (
            "<strong>(a)</strong> Read directly: <strong>P* = $3,000/month, Q* = 1,000 (thousand apts)</strong>. "
            "<strong>(b)</strong> Q_s = 500 (where supply meets the ceiling), Q_d = 1,500 (where demand meets the ceiling). <strong>Shortage = 1,500 − 500 = 1,000 thousand apartments</strong>. "
            "<strong>(c)</strong> Base = 1,000 − 500 = 500. Height at Q = 500: D = $4,000 and S = $2,000, so wedge = <strong>$2,000</strong>. <strong>DWL = ½ × 500 × $2,000 = $500,000/month</strong>. "
            "<strong>(d)</strong> Acceptable: reduced new construction; deferred maintenance / quality decline; black-market subletting / key fees; misallocation (apartments go to who got there first, not who values them most)."
        ),
    },
    8: {
        "title": "Budget Constraint + Equimarginal Principle",
        # MU table shown inline in the set-up (HTML)
        "intro": (
            "Jordan has <strong>$40/week</strong> to spend on Netflix (<strong>$4/week</strong>) and concerts "
            "(<strong>$20/ticket</strong>). Their marginal utility for each is shown in the table.<br><br>"
            "<table style=\"border-collapse: collapse; margin: 6px auto 4px auto; font-size: 10.5pt;\">\n"
            "  <thead><tr style=\"background: var(--surface-color);\">\n"
            "    <th style=\"padding: 4px 12px; border: 1px solid var(--line-color); text-align: right;\">Quantity</th>\n"
            "    <th style=\"padding: 4px 12px; border: 1px solid var(--line-color); text-align: right;\">MU Netflix</th>\n"
            "    <th style=\"padding: 4px 12px; border: 1px solid var(--line-color); text-align: right;\">MU Concert</th>\n"
            "  </tr></thead>\n"
            "  <tbody>\n"
            "    <tr><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">1</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">30</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">80</td></tr>\n"
            "    <tr><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">2</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">24</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">60</td></tr>\n"
            "    <tr><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">3</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">18</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">40</td></tr>\n"
            "    <tr><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">4</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">12</td><td style=\"padding: 3px 12px; border: 1px solid var(--line-color); text-align: right;\">20</td></tr>\n"
            "  </tbody>\n"
            "</table>"
        ),
        "parts": [
            ("a", "Write Jordan's <strong>budget constraint</strong>. What are the X- and Y-intercepts?"),
            ("b", "Calculate <strong>MU per dollar</strong> for each row of the table (both goods)."),
            ("c", "Find Jordan's <strong>optimal bundle</strong> using the equimarginal principle. Show that (i) the entire budget is spent and (ii) MU/$ is equalized across goods."),
            ("d", "Netflix raises its price to <strong>$10/week</strong>. Describe (in words) how Jordan's budget line and optimum change."),
        ],
        "answer": (
            "<strong>(a)</strong> 4N + 20C = 40. X-intercept (all on Netflix): 10 Netflix-weeks. Y-intercept (all on concerts): 2 concerts. "
            "<strong>(b)</strong> Netflix MU/$ (÷$4): 7.5, 6, 4.5, 3. Concert MU/$ (÷$20): 4, 3, 2, 1. "
            "<strong>(c)</strong> Best feasible bundle: <strong>5 Netflix + 1 concert = $20 + $20 = $40</strong>. "
            "MU/$ for 5th Netflix unit is extrapolated lower than 3; MU/$ for 1st concert is 4. So Jordan is approximately indifferent at the margin. "
            "(Strict equimarginal can't be hit exactly because the goods don't align cleanly — pick the bundle that uses the whole budget and gets MU/$ as close to equal as possible.) "
            "<strong>(d)</strong> Budget line <strong>rotates inward on the Netflix axis</strong> (steeper slope, new X-intercept = 40/10 = 4 Netflix-weeks). Y-intercept (concerts) unchanged. Jordan substitutes <strong>toward concerts and away from Netflix</strong> at the new optimum."
        ),
    },
}


# ---------- 3. HTML helpers ----------
SUBSCRIPT_BASES = (
    "MU", "PED", "PES", "P", "Q", "E", "MC", "MB", "TR", "TC",
    "ATC", "AVC", "AFC", "MRP", "VMP", "WTP", "MSC", "MSB", "MPB", "MPC",
)


def _convert_ascii_subscripts(text: str) -> str:
    """Turn P_B / Q_d / MU_x / Q_new etc. into P<sub>B</sub> style.
    Only fires when the base is a known econ identifier."""
    bases = "|".join(sorted(SUBSCRIPT_BASES, key=len, reverse=True))
    pattern = rf"\b({bases})_([A-Za-z]+|\d+)\b"
    return re.sub(pattern, r"\1<sub>\2</sub>", text)


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
    # Convert ASCII subscripts on known econ identifiers (P_B → P<sub>B</sub>)
    text = _convert_ascii_subscripts(text)
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

    # Image source resolution order:
    #   1. variant.image (per-question bank field)
    #   2. IMAGE_OVERRIDES[q.id]  (deck-script override for questions that
    #      reference a figure but don't have an image in the bank)
    image = variant.get("image") or {}
    src_path = image.get("src")
    if not src_path and q.get("id") in IMAGE_OVERRIDES:
        src_path = IMAGE_OVERRIDES[q["id"]]
        image = {"src": src_path, "alt": image.get("alt") or stem[:80]}

    image_html = ""
    if src_path:
        src = src_path
        if src.startswith("/"):
            src = f"{EBOOK_BASE}{src}"
        alt = (image.get("alt") or "").replace('"', "&quot;")
        image_html = (
            f'<div style="text-align: center; margin: 8px 0 16px 0;">\n'
            f'  <img src="{src}" alt="{alt}" '
            f'style="max-width: 90%; max-height: 320px; border-radius: 4px; '
            f'border: 1px solid var(--line-color); background: white;">\n'
            f'</div>'
        )

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
    # Prefer the variant-specific explanation (canvas: override) if it
    # exists, otherwise fall back to the top-level question explanation.
    # The bank schema allows canvas.explanation to differ from base when
    # the canvas variant uses a different scenario (e.g., Canada/Brazil
    # vs U.S./Mexico in q018-us-mexico-abs-adv).
    expl = (variant.get("explanation") or q.get("explanation") or "").strip()
    if expl:
        explanation_html = (
            f'<p style="font-size: 11pt; color: var(--muted-color); '
            f'margin-top: 6px; line-height: 1.4;">{md_inline(expl)}</p>'
        )

    # When there's a figure, shrink the stem box a bit so the layout fits
    stem_margin = "10px" if image_html else "16px"

    return f"""
    <!-- Ch{ch:02d} · MC #{num} -->
    <section id="ch{ch:02d}-mc{num}">
     <div class="chapter-header" style="margin-bottom: 12px; padding-bottom: 8px;">
      <div class="chapter-num" style="font-size: 16pt; padding: 4px 10px;">{ch:02d}</div>
      <div class="chapter-title-pill" style="font-size: 14pt; padding: 6px 0;">{chapter_title} &middot; Practice MC #{num}</div>
     </div>
     <div class="detail-card" style="font-size: 12pt; padding: 10px 14px; margin-bottom: {stem_margin}; border-left-color: var(--primary-color);">
      <p style="font-size: 12pt;"><strong>Q{num}.</strong> {md_inline(stem)}</p>
     </div>
     {image_html}
     <div class="detail-row" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
         {choices_html}
     </div>
     <div class="tip-box fragment fade-up" style="margin-top: 14px;">
      <span class="label">Answer</span>
      <p style="font-size: 14pt;"><strong>{correct_letter}</strong></p>
      {explanation_html}
     </div>
    </section>"""


def render_handout_subslide(ch: int, chapter_title: str) -> str:
    h = HANDOUT_PROBLEMS.get(ch)
    if not h:
        return ""

    # Optional image embed — local files in figures/ are referenced by
    # relative path; the slide deck and figures sit in the same folder
    # so the relative path resolves correctly on GitHub Pages too.
    image_html = ""
    if h.get("image"):
        image_html = (
            f'<div style="text-align: center; margin: 10px 0 8px 0;">\n'
            f'  <img src="{h["image"]}" alt="{h["title"]}" '
            f'style="max-width: 70%; max-height: 280px; border-radius: 4px; '
            f'border: 1px solid var(--line-color); background: white;">\n'
            f'</div>'
        )

    # Two-column layout when a figure is present (figure left, questions
    # right); stacked otherwise.
    if image_html:
        parts_rows = []
        for label, ptext in h["parts"]:
            # Run parts text through md_inline so P_max / Q_s / Q_d
            # get proper <sub> tags (and any **bold** is rendered)
            ptext_html = md_inline(ptext)
            parts_rows.append(
                f'<div style="display: grid; grid-template-columns: 32px 1fr; gap: 10px; align-items: start; '
                f'background: #FAFAFA; border: 1px solid var(--line-color); border-radius: 4px; padding: 6px 10px;">\n'
                f'  <div style="background: var(--primary-color); color: white; border-radius: 4px; '
                f'width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; '
                f'font-weight: 700; font-size: 11pt;">{label}</div>\n'
                f'  <p style="font-size: 10.5pt; line-height: 1.4; margin: 2px 0 0 0;">{ptext_html}</p>\n'
                f'</div>'
            )
        parts_html = "\n         ".join(parts_rows)
        body = (
            f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; align-items: start;">\n'
            f'  <div>{image_html}</div>\n'
            f'  <div>\n'
            f'    <p style="font-size: 9pt; font-weight: 700; letter-spacing: 1px; color: var(--muted-color); '
            f'text-transform: uppercase; margin: 0 0 6px 0;">Read the diagram and answer:</p>\n'
            f'    <div style="display: flex; flex-direction: column; gap: 5px;">\n'
            f'      {parts_html}\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</div>'
        )
    else:
        parts_rows = []
        for label, ptext in h["parts"]:
            ptext_html = md_inline(ptext)
            parts_rows.append(
                f'<div style="display: grid; grid-template-columns: 40px 1fr; gap: 12px; align-items: start; '
                f'background: #FAFAFA; border: 1px solid var(--line-color); border-radius: 4px; padding: 8px 12px;">\n'
                f'  <div style="background: var(--primary-color); color: white; border-radius: 4px; '
                f'width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; '
                f'font-weight: 700; font-size: 12pt;">{label}</div>\n'
                f'  <p style="font-size: 11pt; line-height: 1.4; margin: 4px 0 0 0;">{ptext_html}</p>\n'
                f'</div>'
            )
        parts_html = "\n         ".join(parts_rows)
        body = (
            f'<p style="font-size: 9pt; font-weight: 700; letter-spacing: 1px; color: var(--muted-color); '
            f'text-transform: uppercase; margin: 0 0 6px 0;">Show your work for each part:</p>\n'
            f'     <div style="display: flex; flex-direction: column; gap: 6px;">\n'
            f'         {parts_html}\n'
            f'     </div>'
        )

    return f"""
    <!-- Ch{ch:02d} · Handout-style problem (stacked worksheet) -->
    <section id="ch{ch:02d}-handout">
     <div class="chapter-header" style="margin-bottom: 10px; padding-bottom: 8px;">
      <div class="chapter-num" style="font-size: 16pt; padding: 4px 10px;">{ch:02d}</div>
      <div class="chapter-title-pill" style="font-size: 13pt; padding: 6px 0;">{chapter_title} &middot; Handout Practice: {h['title']}</div>
     </div>
     <div style="background: #FFF8E7; border-left: 4px solid var(--accent-color); border-radius: 4px; padding: 8px 14px; margin-bottom: 10px;">
      <p style="font-size: 11pt; line-height: 1.45; margin: 0;"><span style="font-size: 9pt; font-weight: 700; letter-spacing: 1px; color: var(--accent-color); text-transform: uppercase; margin-right: 8px;">Set-up</span> {h['intro']}</p>
     </div>
     {body}
     <div class="tip-box fragment fade-up" style="margin-top: 10px;">
      <span class="label">Answer Sketch</span>
      <p style="font-size: 10pt; line-height: 1.45;">{h['answer']}</p>
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
