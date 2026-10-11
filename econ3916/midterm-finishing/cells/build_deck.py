"""Build ../index.html for the 3916 midterm-finishing session from midterm.out.json.

    python3 build_deck.py        (run from this folder, after run_snippets.py)

Every number on a data slide is read out of midterm.out.json here, by a regex
that must match or the build stops. Nothing is typed twice: if the snippets
change, rerun ./make.sh and the slides follow.

The page shell (head, Reveal config, poll.js check-in, presenter gate, speaker
view scripts) is copied from the current 3916 house deck, ch13, so this deck
gets the same layers every other 3916 deck has.
"""
from __future__ import annotations

import html
import json
import sys
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE.parent
SHELL = DECK.parent / "ch13-multivariate-ols" / "index.html"
OUT = json.loads((HERE / "midterm.out.json").read_text())
POLL = "midterm-econ3916-poll-1"


# ---------------------------------------------------------------- numbers
def so(name: str) -> str:
    return OUT[name]["stdout"]


def grab(name: str, pat: str, n: int = 1):
    m = re.search(pat, so(name) if name in OUT else name, re.M)
    if not m:
        raise SystemExit(f"build stopped: {pat!r} not found in cell {name}")
    return m.group(n) if isinstance(n, int) else m.groups()


N = {}
N["raw_r"], N["raw_c"] = grab("l1_read", r"\((\d+), (\d+)\)", None)
N["parse_err"] = OUT["l1_read_fails"]["error"]
assert N["parse_err"].startswith("ParserError"), N["parse_err"]
N["last_updated"] = grab("l1_record", r"last updated: (\S+)")
N["downloaded"] = grab("l1_record", r"downloaded: (\S+)")
N["y0"], N["y1"], N["unnamed"] = grab("l2_shape", r"'(\d{4})', '(\d{4})', '(Unnamed: \d+)'\]", None)
N["n_cty"], N["n_ind"] = grab("l2_unit", r"(\d+) countries x (\d+) indicators", None)
N["long_r"], N["long_c"] = grab("l2_melt", r"\((\d+), (\d+)\)", None)
N["year_dtype"] = grab("l2_melt", r"^(object|int64|str)$")
N["pan_r"], N["pan_c"] = grab("l2_pivot", r"\((\d+), (\d+)\)", None)
N["why_int"] = OUT["l2_why_int"]["error"]
assert N["why_int"].startswith("ValueError"), N["why_int"]
N["dup_panel"], N["dup_long"] = grab("l2_check_unit", r"^(\d+)\n(\d+)", None)
N["miss_flfp"] = grab("l3_count", r"^flfp\s+(\d+)")
N["miss_gdp"] = grab("l3_count", r"^gdp_pc\s+(\d+)")
N["miss_fert"] = grab("l3_count", r"^fertility\s+(\d+)")
N["flfp_years"] = [int(y) for y in re.findall(r"\d{4}", grab("l3_where", r"^flfp \[.*?\] \[(.*)\]"))]
N["gdp_years"] = [int(y) for y in re.findall(r"\d{4}", grab("l3_where", r"^gdp_pc \[.*?\] \[(.*)\]"))]
N["fert_years"] = [int(y) for y in re.findall(r"\d{4}", grab("l3_where", r"^fertility \[.*?\] \[(.*)\]"))]
N["med_nogap"] = float(grab("l3_random", r"^False\s+([\d.]+)"))
N["med_gap"] = float(grab("l3_random", r"^True\s+([\d.]+)"))
N["kept_from"], N["kept_to"] = grab("l3_dropna", r"(\d+) -> (\d+)", None)
drops = dict((c, int(k)) for c, k in re.findall(r"^([A-Z]{3})\s+(\d+)$", so("l3_dropna"), re.M))
N["drop_ind"], N["drop_nga"] = drops["IND"], drops["NGA"]
N["drop_total"] = sum(drops.values())
assert N["drop_total"] == int(N["kept_from"]) - int(N["kept_to"])
N["naive"] = grab("l4_naive", r"^(\d+) (\d+) (\d+)$", None)
N["both0"] = grab("l4_indicator", r"^both\s+(\d+)")
N["lonly"] = grab("l4_indicator", r"^left_only\s+(\d+)")
N["ronly"] = grab("l4_indicator", r"^right_only\s+(\d+)")
N["both1"] = grab("l4_fix", r"^both\s+(\d+)")
N["unmatched1"] = int(grab("l4_fix", r"^left_only\s+(\d+)")) + int(grab("l4_fix", r"^right_only\s+(\d+)"))
N["merged_r"], N["merged_c"] = grab("l4_fix", r"\((\d+), (\d+)\)", None)
N["thirds"] = dict(re.findall(r"^(poorest|middle|richest)\s+([\d.]+)$", so("r_figure"), re.M))
N["r_log"] = grab("r_figure", r"^[\d.]+ ([\d.]+)$")
_rm = so("r_model").splitlines()
_cut = next(i for i, l in enumerate(_rm) if re.fullmatch(r"\d+ [\d.]+", l))
coef = dict((k, (float(c), float(s_))) for k, c, s_ in
            (re.match(r"^(\S+)\s+(-?[\d.]+)\s+([\d.]+)$", l).groups() for l in _rm[1:_cut]))
N["coef"] = coef
N["nobs"], N["r2"] = _rm[_cut].split()
ci = dict((k, (a, b)) for k, a, b in
          (re.match(r"^(\S+)\s+(-?[\d.]+)\s+(-?[\d.]+)$", l).groups() for l in _rm[_cut + 2:_cut + 6]))
assert set(ci) == set(coef) == {"Intercept", "np.log(gdp_pc)", "fertility", "leave_weeks"}, (ci, coef)
N["ci"] = ci
N["ten_pct"], N["ten_lo"], N["ten_hi"] = grab("r_model", r"^([\d.]+) \[([\d.]+), ([\d.]+)\]$", None)
N["bp_p"] = grab("r_diag", r"^([\d.]+e-?\d+)$")
N["vif"] = dict(re.findall(r"'([^']+)': ([\d.]+)", so("r_diag")))
N["cook_max"], N["cook_n"], N["cook_of"] = grab("r_diag", r"^([\d.]+) (\d+) (\d+)$", None)
N["cook_rows"] = re.findall(r"^\s*([A-Z]{3})\s+(\d{4})$", so("r_diag"), re.M)
N["sqrt_vif"] = grab("r_diag", r"^(\d\.\d\d)$")
N["refit_from"], N["refit_to"] = grab("r_diag", r"^([\d.]+) -> ([\d.]+)$", None)
assert int(N["cook_n"]) == len(N["cook_rows"])
assert abs(float(N["sqrt_vif"]) - math.sqrt(float(N["vif"]["np.log(gdp_pc)"]))) < 0.01


N["n_years"] = int(N["long_r"]) // int(N["raw_r"])
assert N["n_years"] == int(N["y1"]) - int(N["y0"]) + 1
N["n_sum_cty"], N["sum_y0"], N["sum_y1"] = grab("r_summary", r"^(\d+) countries, (\d{4}) to (\d{4})$", None)


def yr(ys):  # 2010..2013 -> "2010&ndash;13"
    ys = sorted(set(ys))
    return f"{ys[0]}&ndash;{str(ys[-1])[2:]}" if len(ys) > 1 else str(ys[0])


# ---------------------------------------------------------------- html helpers
def esc(s: str) -> str:
    return html.escape(s, quote=False)


def attr(s: str) -> str:
    return html.escape(s, quote=True)


def cell(name: str, *, out_frag: str | None = None, idx: int | None = None,
         cell_frag: str | None = None, cidx: int | None = None, code: str | None = None,
         out_text: str | None = None, small: bool = False) -> str:
    """A Colab-looking cell: code always from the json, output from the json."""
    c = OUT[name]
    code = c["code"] if code is None else code
    if out_text is None:
        out_text = c["error"] if c["error"] else c["stdout"].rstrip("\n")
    err = bool(c["error"]) and out_text == c["error"]
    fs = "11.5pt" if small else "12.5pt"
    o_cls = "cell-out err" if err else "cell-out"
    frag_o = (f' class="{o_cls} fragment" data-notes="{attr(out_frag)}"'
              + (f' data-fragment-index="{idx}"' if idx is not None else "")) if out_frag else f' class="{o_cls}"'
    frag_c = (f' class="cell fragment" data-notes="{attr(cell_frag)}"'
              + (f' data-fragment-index="{cidx}"' if cidx is not None else "")) if cell_frag else ' class="cell"'
    return (f'<div{frag_c} data-cell="{name}">'
            f'<div class="cell-code"><span class="cell-run"><i class="fa-solid fa-circle-play"></i></span>'
            f'<pre style="font-size:{fs}">{esc(code)}</pre></div>'
            f'<div{frag_o}><pre style="font-size:{fs}">{esc(out_text)}</pre></div></div>')


SYN = ('<p class="syn">Synthetic data in the WDI download layout: real country names and codes, '
       'generated numbers. Code and output: <code>cells/midterm.py</code></p>')

UL = 'style="margin:0 0 0.8em 1.1em;padding:0"'
LI = 'style="margin:0 0 0.35em"'


TERM = {}   # section id -> THIS TERM text, added by add_term() after notes_speaker_view.py


sys.path.insert(0, str(Path.home() / "Resilio Sync/documents/econ-lecture-material/TA/teaching-improvement/tools"))
from notes_speaker_view import LEAD, REST, TIME, WARN   # the house speaker-view styles, not a copy


def notes(dur: str, say: str, rest: list[str] | None = None, extra: str = "", warn: str = "") -> str:
    """3916 house note in its final speaker-view form (four levels, nothing folds):
    clock, prohibition (optional), the line to say, everything else."""
    w = f'<p style="{WARN}">{warn}</p>' if warn else ""
    lis = "".join(f"<li {LI}>{r}</li>" for r in (rest or []))
    body = (f"<ul {UL}>{lis}</ul>" if lis else "") + extra
    r = f'<div class="sv-rest" style="{REST}">{body}</div>' if body else ""
    return (f'<aside class="notes" data-sv="1"><p style="{TIME}">{dur}</p>{w}'
            f'<div class="sv-lead" style="{LEAD}"><p>{say}</p></div>{r}</aside>')


def h2(icon: str, text: str, color: str = "var(--secondary-color)") -> str:
    return f'<h2><i class="fa-solid fa-{icon}" style="color: {color};"></i> {text}</h2>'


def divider(i: int, title: str, sub: str, minutes: int, note: str) -> str:
    return (f'<section id="divider-{i}" class="section-divider" data-state="is-section-divider">'
            f'<h1>{title}</h1><p class="subtitle">{sub} &nbsp;&bull;&nbsp; {minutes} min</p>'
            + notes(f"{minutes} minutes for this section.", note) + '</section>')


S = []   # top-level slides, in order

# ---------------------------------------------------------------- 1 title
S.append(f'''
<section id="title" class="section-divider" data-state="is-section-divider" style="padding: 0;">
  <div style="display: grid; grid-template-columns: 55% 45%; height: 720px;">
    <div style="display: flex; flex-direction: column; justify-content: center; padding: 50px 50px 50px 60px;">
      <p style="font-size: 12pt; color: var(--secondary-color); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 12px;">ECON 3916 &bull; Applied Machine Learning for Economists &bull; Midterm Project</p>
      <h1 style="font-size: 32pt; line-height: 1.25; color: var(--primary-color); margin-bottom: 25px;">Finishing Your Midterm</h1>
      <div style="width: 50px; height: 3px; background: var(--secondary-color); margin-bottom: 0;"></div>
      <p style="font-size: 14pt; color: var(--muted-color); font-style: italic; margin-top: 22px; line-height: 1.6;">Cleaning and joining the data you found,<br>and what each section is graded on.</p>
      <div style="margin-top: auto; padding-bottom: 15px;">
        <p style="font-size: 16pt; color: var(--primary-color); font-weight: 700; font-family: var(--heading-font); margin-bottom: 8px;">Dr. Richeng Piao</p>
        <p style="font-size: 12pt; color: var(--muted-color); font-weight: 400; font-style: italic; line-height: 1.8;">Department of Economics<br>Northeastern University</p>
      </div>
    </div>
    <div style="background: #f0f5f8; display: flex; flex-direction: column; justify-content: center; padding: 40px 48px; gap: 14px;">
      <p style="font-size: 12pt; color: var(--secondary-color); letter-spacing: 2px; text-transform: uppercase;">Four lines about your data</p>
      <p style="font-size: 18pt; line-height: 1.5;"><b>1</b>&ensp;Where it comes from</p>
      <p style="font-size: 18pt; line-height: 1.5;"><b>2</b>&ensp;Its shape</p>
      <p style="font-size: 18pt; line-height: 1.5;"><b>3</b>&ensp;What is missing</p>
      <p style="font-size: 18pt; line-height: 1.5;"><b>4</b>&ensp;The one join or reshape</p>
    </div>
  </div>
  {notes("65 minutes.", "Today we finish the midterm: the four lines about your data, then what each rubric row is looking for, then ten minutes on your own file.", ["This session is recorded and becomes the guidance video for later terms, so everything except the next slide is written to hold for any term."])}
</section>''')

# ---------------------------------------------------------------- 2 logistics (the one dated slide)
S.append(f'''
<section id="logistics" style="padding: 40px 50px;">
  {h2("calendar-day", "This Term&rsquo;s Dates", "var(--accent-color)")}
  <div class="content">
    <div style="display: flex; flex-direction: column; gap: 11px; margin-top: 8px;">
      <div class="date-row" style="border-left-color: var(--danger-color);"><p class="d">Mon 9 Nov, 11:59 pm</p><p><strong>Midterm project due.</strong> Colab link (Anyone with the link), report PDF of ten pages at most, GitHub repository.</p></div>
      <div class="date-row"><p class="d">Wed 4 Nov, 11:59 pm</p><p><strong>Lab 14 due</strong> &mdash; the diagnostics lab. Section 4 of the midterm is the same tests on your own data.</p></div>
      <div class="date-row"><p class="d">Sun 8 Nov</p><p><strong>Quiz 1 closes</strong> &mdash; the same weekend as the midterm. Plan for both.</p></div>
      <div class="date-row"><p class="d">Fri 13 Nov</p><p><strong>Problem Set 4 due</strong>, after the midterm.</p></div>
    </div>
    <div class="key-result" style="margin-top: 18px;"><p>Dates are on Canvas too. If this slide and Canvas ever disagree, Canvas is the one that counts.</p></div>
  </div>
  {notes("2 min.", "Four dates, and the one that matters today is the midterm deadline: Colab link, PDF and repository, all three.", ["Say the Quiz 1 weekend out loud; students plan for one deadline and get caught by the other.", "This is the only slide with dates on it. In the recording for later terms, cut it, or replace it with a line pointing at Canvas."], )}
</section>''')

# ---------------------------------------------------------------- 3 plan
S.append(f'''
<section id="plan" style="padding: 40px 50px;">
  {h2("list-check", "Today: Four Lines, Then the Rubric, Then Your File")}
  <div class="content">
    <p class="text-lg" style="line-height: 1.6;">Before you commit to a dataset you write four lines about it. They are the part of the midterm nobody can do for you two days before it is due, and they are most of Section 1.</p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 14px;">
      <div class="line-card"><p class="n">1</p><p><strong>Where it comes from</strong><br>the URL, and the date you downloaded it</p></div>
      <div class="line-card"><p class="n">2</p><p><strong>Its shape</strong><br>rows, columns, and what one row is</p></div>
      <div class="line-card"><p class="n">3</p><p><strong>What is missing</strong><br>which columns, how many, and whether it looks random</p></div>
      <div class="line-card"><p class="n">4</p><p><strong>The one join or reshape</strong><br>merging two files, wide to long, aggregating &mdash; or none</p></div>
    </div>
    <p style="font-size: 14.5pt; color: var(--muted-color); margin-top: 16px;">Each line gets one worked example on the same small file. Then the six rubric rows, then ten minutes on your own data.</p>
  </div>
  {notes("2 min.", "Each of the four lines gets one worked example, in order, on the same small country-year file, so by the end you have seen a whole cleaning run from download to merged panel.", ["The four lines are the data checkpoint students post in the discussion before committing to a dataset; say that those who posted will recognise them.", "Do not promise to answer every dataset question in the room; the working time at the end is for that."])}
</section>''')

# ---------------------------------------------------------------- 4 poll stack
POLL_OPTS = [
    ("A", "<strong>Not line 1 yet</strong> &mdash; I have no file downloaded"),
    ("B", "<strong>Lines 1&ndash;2</strong> &mdash; I have the file and know what one row is"),
    ("C", "<strong>Lines 1&ndash;3</strong> &mdash; I have also counted what is missing"),
    ("D", "<strong>All four</strong> &mdash; the join or reshape is done, or I need none"),
]
opts = "".join(f'<div class="poll-option" data-choice="{k}" style="background: #f0f5f8; padding: 14px 18px; border-radius: 8px; cursor: pointer; transition: all 0.2s; border: 3px solid transparent;">{k}) {t}</div>' for k, t in POLL_OPTS)
S.append(f'''
<section>
  <section id="poll-1" style="padding: 40px 50px;">
    {h2("chart-bar", "Poll: Where Is Your Data Today?", "var(--accent-color)")}
    <div style="background: #f8f6f3; border-radius: 10px; padding: 16px 22px; margin-top: 12px;">
      <p style="font-size: 16.5pt; font-weight: 600;">For your own midterm data: how far down the four lines can you write today?</p>
      <p style="font-size: 14pt; color: var(--muted-color); margin-top: 6px;">Pick the furthest line you could write now, without opening anything.</p>
    </div>
    <div class="poll-grid" data-poll-id="{POLL}" style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 18px; font-size: 14.5pt;">{opts}</div>
    {notes("3 min.", "Vote for your own data, not for what you think the right answer is: there is no right answer, and the bars decide where the next forty minutes go.", ["Students click on their phones; the vote is also today's check-in, so anyone who has not entered an NUID gets the prompt now.", "Leave it up while the room settles; late arrivals vote here or not at all, because this is the only poll in the deck.", "With about thirty in the room one vote is about three percent of the chart; read counts, not percentages."])}
  </section>
  <section id="poll-1-reveal" data-poll-results="{POLL}" style="padding: 34px 50px;">
    {h2("chart-column", "Where the Bars Are Is Where the Time Goes", "var(--success-color)")}
    <div class="poll-results-chart" data-poll-id="{POLL}" style="display:flex; gap:20px; align-items:flex-end; justify-content:center; height:150px; margin:10px 60px;"></div>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 30px;">
      <div class="steer"><p><strong>Mostly A</strong></p><p>The working time at the end is for downloading. Nothing else in the midterm can start before the file exists.</p></div>
      <div class="steer"><p><strong>Mostly B or C</strong></p><p>Lines 3 and 4 are yours today: the missing-data count and the merge check.</p></div>
      <div class="steer"><p><strong>Mostly D</strong></p><p>Use each section to check what you already did, and spend the rubric section on Sections 3 and 4.</p></div>
    </div>
    {notes("2 min.", "The tallest bar tells us which part of today matters most to this room, so let's read it together.", ["Every reading of the chart is fine; a room that is mostly D still gets value from the checks, because the checks are what catch a merge that lost rows.", "If anyone voted A, find them during the working time first: a midterm with no file has no Section 1."])}
  </section>
</section>''')

# ---------------------------------------------------------------- line 1
S.append(divider(1, "Line 1 &middot; Where It Comes From", "The URL and the date you downloaded it", 7,
                 "Line one is where your data comes from: the address you got it from and the day you got it."))

S.append(f'''
<section id="l1-why" style="padding: 40px 50px;">
  {h2("link", "Line 1 Asks for a URL and a Date")}
  <div class="content">
    <p class="text-lg" style="line-height: 1.6;">The same URL gives you a different file next year. Statistical agencies revise: GDP is re-estimated, the World Bank updates its indicators more than once a year, and FRED keeps old versions of a series in ALFRED because the numbers change.</p>
    <div class="fragment fade-up key-result" style="margin-top: 16px;" data-notes="So the date is part of the citation: your coefficient belongs to one download, and the date tells a reader which one."><p><strong>Your number belongs to one download.</strong> The URL says where; the date says which version.</p></div>
    <div class="fragment fade-up" style="background: #f8f6f3; border-left: 4px solid var(--secondary-color); padding: 14px 20px; border-radius: 6px; margin-top: 14px;" data-notes="Read the rubric sentence: a stranger who clones the repository gets to your number without emailing you. Line 1 is the first half of that.">
      <p style="font-size: 15pt;">Rubric, repository row: <em>&ldquo;A stranger who clones it should be able to get to your number without emailing you.&rdquo;</em> Line 1 is the start of that.</p>
    </div>
  </div>
  {notes("2 min.", "The date is there because data change after you download them, and a reader needs to know which version your number came from.", ["IF ASKED which sources revise: almost all national accounts do; survey-based series are revised when weights are updated.", "Keep this to two minutes; the example on the next slide makes the same point with a file."])}
</section>''')

S.append(f'''
<section id="l1-read" style="padding: 26px 46px;">
  {h2("file-csv", "Worked Example: The First Read of the Download")}
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 10px;">
    <div>
      {cell("l1_read_fails", small=True, out_frag="It fails on the very first read: the parser expected 3 fields and found 15 on line 5. That error is about the top of the file, not the data.", idx=1)}
      {cell("l1_read", small=True, cell_frag="skiprows=4 jumps the four metadata lines, and the file reads: " + N["raw_r"] + " rows and " + N["raw_c"] + " columns.", cidx=3)}
    </div>
    <div>
      {cell("l1_peek", small=True, cell_frag="Look at the first five lines as text. Lines 1 to 4 are the source and the date the source last updated the file, then a blank line, then the real header on line 5.", cidx=2)}
      <div class="fragment fade-up key-result" data-fragment-index="4" style="margin-top: 10px;" data-notes="The lines the parser choked on are the provenance. Copy them into line 1 before you skip them."><p style="font-size: 14pt;">The four lines the parser choked on are the file&rsquo;s own provenance: the source and its <strong>Last Updated Date</strong>. Copy them into line 1, then skip them.</p></div>
    </div>
  </div>
  {SYN}
  {notes("3 min.", "This is the World Bank's bulk download layout, and the first read_csv on it fails, which is the most common first error on a downloaded file.", ["Click order: the error, then the first five lines, then the read that works, then the takeaway.", "IF ASKED: FRED and BLS files have their own headers; the fix is the same, open the file as text before you read it as a table."])}
</section>''')

S.append(f'''
<section id="l1-write" style="padding: 32px 50px;">
  {h2("pen", "What to Write, and Where It Goes Again")}
  <div class="content">
    {cell("l1_record")}
    <div class="fragment fade-up" style="background: #f8f6f3; border-left: 4px solid var(--accent-color); padding: 14px 20px; border-radius: 6px; margin-top: 14px;" data-notes="Line 1 as you would post it, for this file. The same two facts go in the notebook's first cell and in the README's data section.">
      <p style="font-size: 12pt; color: var(--accent-color); text-transform: uppercase; letter-spacing: 2px;">Line 1, as you would post it</p>
      <p style="font-size: 15pt; margin-top: 6px;">World Bank, World Development Indicators, databank.worldbank.org/source/world-development-indicators, downloaded {N["downloaded"]} (the file says last updated {N["last_updated"]}).</p>
    </div>
    <p class="fragment fade-up" style="font-size: 14.5pt; margin-top: 14px;" data-notes="If your data come from an API, the download is code. Then the series id and the day you ran it are line 1, and the repository has the download step instead of the file.">Downloaded by code instead (FRED, an API)? Then the series id and the day you ran it are line 1, and the repository documents the download step.</p>
  </div>
  {SYN}
  {notes("2 min.", "Put the source and the date in the first cell of the notebook, the same two facts in the README, and you have written line 1 three times for the price of once.", ["The download date is typed by the student; the last-updated date is read from the file, so it cannot drift from the file in the repository."])}
</section>''')

# ---------------------------------------------------------------- line 2
S.append(divider(2, "Line 2 &middot; Its Shape", "Rows, columns, and what one row is", 8,
                 "Line two is the shape of the file, and the sentence that matters is what one row is."))

S.append(f'''
<section id="l2-shape" style="padding: 26px 46px;">
  {h2("table-cells", "Worked Example: What Is One Row?")}
  {cell("l2_shape", out_frag=f"{N['raw_r']} rows and {N['raw_c']} columns. The years are columns, and the last column is called {N['unnamed']}: it is empty, made by the comma at the end of every line.", small=True)}
  {cell("l2_unit", out_frag=f"{N['n_cty']} countries times {N['n_ind']} indicators is {N['raw_r']}: one row is one country and one indicator.", small=True)}
  <div class="fragment fade-up key-result" style="margin-top: 8px;" data-notes="A model of female participation needs one row per country-year. This file has one row per country-indicator, so line 2 already tells you line 4: a reshape."><p style="font-size: 14.5pt;">One row here is <strong>a country &times; an indicator</strong>, with years across. Your regression needs <strong>one row per country-year</strong>, so line 2 already tells you what line 4 will be.</p></div>
  {SYN}
  {notes("3 min.", "Line 2 is the shape plus a sentence saying what one row is, and the sentence matters more than the numbers.", ["Ask the room what one row is before the second output shows; most will say a country.", "The Unnamed column is a real feature of this download layout; dropping it is part of cleaning, and the notebook should say it was dropped."])}
</section>''')

S.append(f'''
<section id="l2-melt" style="padding: 26px 46px;">
  {h2("arrows-rotate", "Wide to Long: One Number per Row")}
  <div style="display: grid; grid-template-columns: 1.25fr 0.75fr; gap: 16px; margin-top: 8px;">
    {cell("l2_melt", out_frag=f"melt makes one row per country, indicator and year: {N['raw_r']} rows times {N['n_years']} years is {N['long_r']}. And the year column came out as text, dtype {N['year_dtype']}.")}
    <div class="shape-steps">
      <div class="shape"><p class="k">as downloaded</p><p class="v">{N["raw_r"]} &times; {N["raw_c"]}</p><p class="u">country &times; indicator</p></div>
      <div class="shape fragment fade-up" data-notes="Count the rows at every step: {N['raw_r']} times {N['n_years']} years is {N['long_r']}, a product you can check in your head."><p class="k">after melt</p><p class="v">{N["long_r"]} &times; {N["long_c"]}</p><p class="u">country &times; indicator &times; year</p></div>
    </div>
  </div>
  <div class="fragment fade-up key-result" style="margin-top: 10px;" data-notes="After melt every number has its own row, with the country, the indicator and the year beside it. That is the long form; the next step makes it a panel."><p style="font-size: 14.5pt;">After <code>melt</code> every number has its own row, labelled by country, indicator and year. One more step makes it a panel.</p></div>
  {SYN}
  {notes("1.5 min.", "Melt turns the year columns into rows, so every number in the file gets its own row with its labels beside it.", ["dropna(axis=1, how='all') removes the empty Unnamed column; say it in a comment, because a reader cannot reproduce a step nobody wrote down."])}
</section>''')

S.append(f'''
<section id="l2-pivot" style="padding: 26px 46px;">
  {h2("table-columns", "Then One Row per Country-Year")}
  <div style="display: grid; grid-template-columns: 1.25fr 0.75fr; gap: 16px; margin-top: 8px;">
    {cell("l2_pivot", out_frag=f"pivot puts the three indicators back as columns: {N['pan_r']} rows, one per country-year, {N['n_cty']} countries times {N['n_years']} years. Then year becomes an integer.", small=True)}
    <div class="shape-steps">
      <div class="shape"><p class="k">after pivot</p><p class="v">{N["pan_r"]} &times; {N["pan_c"]}</p><p class="u">country &times; year</p></div>
      <div class="fragment fade-up misconception" style="margin-top: 4px;" data-notes="Why the astype(int) line is there: leave year as text and the merge in line 4 stops with this error, because the other file stores year as a number.">
        <p style="font-size: 12.5pt;"><strong>Skip <code>astype(int)</code></strong> and the merge in line 4 stops:</p>
        <p style="font-size: 11.5pt; font-family: monospace; color: #b3261e;">{esc(N["why_int"][:86])}&hellip;</p>
      </div>
    </div>
  </div>
  {SYN}
  {notes("1.5 min.", "Pivot puts the three indicators back as columns, and now one row is one country in one year, which is the unit the regression needs.", ["The error in the box is real output: cell l2_why_int runs the merge with year left as text.", "{N['raw_r']}, then {N['long_r']}, then {N['pan_r']}: say the three counts out loud once more."])}
</section>''')

S.append(f'''
<section id="l2-check" style="padding: 30px 50px;">
  {h2("check-double", "The Check That Proves the Unit")}
  {cell("l2_check_unit", out_frag=f"On the panel: {N['dup_panel']} duplicated country-years. On the long table, the same check finds {N['dup_long']}. So the check can fail, and the zero means something.")}
  <div class="fragment fade-up key-result" style="margin-top: 12px;" data-notes="A zero from a check you have never seen fail proves nothing. Run it once where it must fail, here the long table, and then the zero on the panel is evidence."><p style="font-size: 15pt;">A check you have never seen fail proves nothing. Run it once where it must fail, and then the zero is evidence.</p></div>
  <div class="fragment fade-up" style="background: #f8f6f3; border-left: 4px solid var(--accent-color); padding: 14px 20px; border-radius: 6px; margin-top: 12px;" data-notes="Line 2 as you would post it for this file.">
    <p style="font-size: 12pt; color: var(--accent-color); text-transform: uppercase; letter-spacing: 2px;">Line 2, as you would post it</p>
    <p style="font-size: 15pt; margin-top: 6px;">Downloaded as {N["raw_r"]} rows &times; {N["raw_c"]} columns, one row per country-indicator. After the reshape, {N["pan_r"]} rows, one per country-year: {N["n_cty"]} countries, {N["y0"]}&ndash;{N["y1"]}.</p>
  </div>
  {SYN}
  {notes("2 min.", "Before you trust that one row is one country-year, count the duplicates on your key, and run the same count once on a table where it has to find some.", ["The key is whatever your unit is: country and year, county and year, person id.", "Do not skip the second line of output; it is the reason the first line can be believed."])}
</section>''')

# ---------------------------------------------------------------- line 3
gap_line = (f"female LFP {N['miss_flfp']} (India {yr(N['flfp_years'][:4])}, Nigeria {yr(N['flfp_years'][4:])}), "
            f"GDP {N['miss_gdp']} (Nigeria {yr(N['gdp_years'])}), fertility {N['miss_fert']} single years")
S.append(divider(3, "Line 3 &middot; What Is Missing", "Which columns, how many, and whether it looks random", 8,
                 "Line three is what is missing: how much, where, and whether it looks random."))

S.append(f'''
<section id="l3-count" style="padding: 26px 46px;">
  {h2("magnifying-glass", "Count First, Then Ask Where")}
  <div style="display: grid; grid-template-columns: 0.8fr 1.2fr; gap: 16px; margin-top: 8px;">
    {cell("l3_count", out_frag=f"{N['miss_flfp']} gaps in female participation, {N['miss_gdp']} in GDP, {N['miss_fert']} in fertility, out of {N['pan_r']} country-years.", small=True)}
    {cell("l3_where", out_frag="Now where: the participation gaps are India and Nigeria in the early years, the GDP gap is Nigeria at the end, and the fertility gaps are three single years in three different countries.", small=True)}
  </div>
  <div class="fragment fade-up key-result" style="margin-top: 10px;" data-notes="A count tells you how much is missing. Grouping the gaps by country and by year tells you whether they look random, which is the second half of line 3."><p style="font-size: 14.5pt;">The count says how much. Grouping the gaps by unit and by year says whether they look random.</p></div>
  {SYN}
  {notes("3 min.", "isna().sum() gives you the count, and one groupby of the gaps by country and year gives you the pattern; line 3 needs both.", ["Fertility gaps are scattered; participation gaps are concentrated; that contrast is the next slide.", "IF ASKED about the indicator: the national-estimate series has gaps because it comes from each country's own labour force survey; the ILO's modelled series fills them with a model, which is a measurement decision worth a sentence in Section 1."])}
</section>''')

S.append(f'''
<section id="l3-random" style="padding: 26px 46px;">
  {h2("shuffle", "Random or Not: Three Gaps, Three Labels")}
  {cell("l3_random", out_frag=f"Median GDP per capita is about {N['med_gap']:,.0f} dollars in the countries with participation gaps and {N['med_nogap']:,.0f} in the rest. The gaps sit in the poorer countries.", small=True)}
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 12px;">
    <div class="fragment fade-up mech" data-notes="Fertility: three single years in three countries, no pattern by country or year. Calling that MCAR is defensible, and you say why."><p class="m">MCAR</p><p><strong>Fertility.</strong> {N["miss_fert"]} single years in three countries, no pattern by country or year. Defensible, and you say why.</p></div>
    <div class="fragment fade-up mech" data-notes="Participation: the series starts late in two poorer countries. The gaps depend on things you can see, income and year, so the label is MAR given country and year."><p class="m">MAR</p><p><strong>Female LFP.</strong> The series starts late in two poorer countries. The gaps depend on what you can see: income and year.</p></div>
    <div class="fragment fade-up mech" data-notes="GDP stops after {min(N['gdp_years']) - 1} in one country. The file does not say why. If it stopped because the economy was in crisis, the missing years are the bad years, which is MNAR, and dropping them makes the country look better than it was. Find out from the source's country notes."><p class="m">MNAR?</p><p><strong>GDP</strong> stops after {min(N["gdp_years"]) - 1} in one country. The file does not say why; the source&rsquo;s notes do. If the bad years are the missing ones, that is MNAR.</p></div>
  </div>
  {SYN}
  {notes("3 min.", "The rubric asks you to name the mechanism and defend the label, and the defence is a fact about your data, like the income gap in this output.", ["MCAR, MAR and MNAR are Topic 1's labels; the rubric row for Section 1 asks for one and a reason.", "The third card is a question on purpose: students must go to the documentation, because the file cannot tell them why a series stops."])}
</section>''')

S.append(f'''
<section id="l3-dropna" style="padding: 30px 50px;">
  {h2("filter-circle-xmark", "dropna() Decides Who Is in Your Sample")}
  {cell("l3_dropna", out_frag=f"{N['kept_from']} rows become {N['kept_to']}. Nigeria loses {N['drop_nga']} of its {N['n_years']} years and India {N['drop_ind']}: {N['drop_nga'] + N['drop_ind']} of the {N['drop_total']} dropped rows come from the two poorest countries.")}
  <div class="fragment fade-up" style="background: #f8f6f3; border-left: 4px solid var(--accent-color); padding: 14px 20px; border-radius: 6px; margin-top: 12px;" data-notes="Line 3 as you would post it for this file, and the sentence for Section 1 that says what the gaps do to the answer.">
    <p style="font-size: 12pt; color: var(--accent-color); text-transform: uppercase; letter-spacing: 2px;">Line 3, as you would post it</p>
    <p style="font-size: 14.5pt; margin-top: 6px;">Missing: {gap_line}. The gaps sit in the poorer countries, so not random; dropping them keeps {N["kept_to"]} of {N["kept_from"]} rows and leaves the sample richer than the twelve countries are.</p>
  </div>
  {SYN}
  {notes("2 min.", "Dropping rows with a gap is a choice about who is in your sample, and Section 1 asks you to say what that choice does to your answer.", ["The sentence for Section 1 is the last clause of the card: the sample left after dropna is richer than the population of countries you started with.", "IF ASKED about filling gaps instead: interpolating a missing year is a modelling choice too; say it and show the answer with and without."])}
</section>''')

# ---------------------------------------------------------------- line 4
S.append(divider(4, "Line 4 &middot; The One Join or Reshape", "Merging two files, wide to long, aggregating &mdash; or none", 8,
                 "Line four is the one join or reshape that makes the file usable, and the numbers that show it worked."))

S.append(f'''
<section id="l4-naive" style="padding: 30px 50px;">
  {h2("code-merge", "Worked Example: A Merge That Runs and Loses Rows")}
  <p style="font-size: 15pt; margin-top: 6px;">A second file from a different source: weeks of paid maternity leave, by country name and year.</p>
  {cell("l4_naive", out_frag=f"{N['naive'][0]} rows in the panel, {N['naive'][1]} in the leave file, {N['naive'][2]} after the merge. No error and no warning, and a third of the rows are gone.")}
  <div class="fragment fade-up misconception" style="margin-top: 12px;" data-notes="pandas did what it was told: an inner merge keeps only the rows whose keys match exactly. Nothing told you that four countries did not match."><p style="font-size: 15pt;">The default merge is an inner join: it keeps only rows whose keys match exactly, and it does not tell you what it dropped.</p></div>
  {SYN}
  {notes("3 min.", "A merge can run without an error and still lose a third of your rows, so the row count before and after is part of every merge.", ["Topic 11 language: this is an inner join; the same thing happens in SQL.", "Ask the room to guess why before the next slide; someone usually says spelling."])}
</section>''')

S.append(f'''
<section id="l4-indicator" style="padding: 26px 46px;">
  {h2("eye", "Find What Did Not Match")}
  {cell("l4_indicator", out_frag=f"An outer merge with indicator=True keeps everything and labels it: {N['both0']} matched, {N['lonly']} only in the panel, {N['ronly']} only in the leave file. The two lists are the same four countries, spelled two ways.", small=True)}
  <div class="fragment fade-up key-result" style="margin-top: 10px;" data-notes="Names change between sources; codes usually do not. When both files carry a code, ISO3 for countries or FIPS for US counties, merge on the code."><p style="font-size: 14.5pt;">Names change between sources; codes mostly do not. When both files carry a code (ISO3 for countries, FIPS for US counties), merge on the code.</p></div>
  {SYN}
  {notes("3 min.", "how='outer' with indicator=True is the merge you run to look, before the merge you keep.", ["Read the two lists side by side: Egypt, Korea, Turkiye, Viet Nam.", "The leave file has no code column, which is why the fix on the next slide is a name crosswalk."])}
</section>''')

S.append(f'''
<section id="l4-fix" style="padding: 26px 46px;">
  {h2("wrench", "Fix the Key, Merge Again, Report Three Numbers")}
  {cell("l4_fix", out_frag=f"After a four-name crosswalk, all {N['both1']} rows match, and validate one_to_one would have stopped the merge if any country-year appeared twice.", small=True)}
  <div class="fragment fade-up" style="background: #f8f6f3; border-left: 4px solid var(--accent-color); padding: 12px 20px; border-radius: 6px; margin-top: 10px;" data-notes="Line 4 as you would post it, with the three numbers: rows before, rows after, rows unmatched.">
    <p style="font-size: 12pt; color: var(--accent-color); text-transform: uppercase; letter-spacing: 2px;">Line 4, as you would post it</p>
    <p style="font-size: 14.5pt; margin-top: 6px;">Reshaped WDI wide to long, then merged a leave table on country and year. Four names did not match; fixed with a crosswalk. {N["naive"][0]} rows before, {N["merged_r"]} after, {N["unmatched1"]} unmatched.</p>
  </div>
  {SYN}
  {notes("2 min.", "The three numbers for line 4 are rows before, rows after and rows unmatched, and they belong in the notebook next to the merge, not only in the post.", ["validate='one_to_one' turns an unnoticed duplicate into an error; m:1 is the right setting when one side is a lookup table.", "If a student's answer to line 4 is none, they say so; that is an allowed answer."])}
</section>''')

# ---------------------------------------------------------------- rubric
c_log, s_log = N["coef"]["np.log(gdp_pc)"]
c_fer, s_fer = N["coef"]["fertility"]
c_lw, s_lw = N["coef"]["leave_weeks"]
c_int, s_int = N["coef"]["Intercept"]
lo_f, hi_f = N["ci"]["fertility"]
S.append(divider(5, "What Each Rubric Row Is Looking For", "Six rows, 100 points, on the same example", 15,
                 "Now the rubric: six rows, and for each one what the grader is looking for, on the same example."))

RUB = [
    ("Question and data provenance", 20, "A measurable question; data described as a measurement product; missingness mechanism named and defended; a summary table that reads on its own"),
    ("Descriptive evidence", 20, "Two or more figures, each making a stated point; captions state findings, not variables; Topic 3&rsquo;s standards"),
    ("Model and interpretation", 25, "A formatted regression table; two coefficients interpreted in full, with units and magnitude; every control justified by its role"),
    ("Diagnostics", 20, "Residuals, heteroskedasticity, VIF and influence, all run and interpreted; robust errors where warranted"),
    ("Threats and conclusion", 10, "The causal claim assessed; the estimand labelled if it is not causal; no new results in the conclusion"),
    ("Repository", 5, "Public repo with notebook and report; data included or the download documented; a README you wrote"),
]
rows = "".join(f'<tr><td>{a}</td><td style="text-align:center;font-weight:700">{p}</td><td>{d}</td></tr>' for a, p, d in RUB)
assert sum(p for _, p, _ in RUB) == 100
S.append(f'''
<section id="r-overview" style="padding: 30px 50px;">
  {h2("table-list", "The Rubric, Row by Row")}
  <table class="rub"><thead><tr><th>Row</th><th>Pts</th><th>What earns full marks</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="misconception" style="margin-top: 12px;"><p style="font-size: 14pt;"><strong>No AI anywhere in this project</strong> &mdash; code, analysis, writing, README. Section 4 uses Topic 14; write Sections 1&ndash;3 first.</p></div>
  {notes("2 min.", "The four lines you just saw are most of the first row, so a third of the grade is already in reach for anyone who has done them.", ["Do not read the table aloud; name the two largest rows, the model at 25 and the two twenties around it, and move.", "The no-AI rule covers the README and the report prose too; say that sentence exactly."])}
</section>''')

tab_rows = re.findall(r"^(.+?)\s{2,}([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)$", so("r_summary"), re.M)
assert len(tab_rows) == 4, tab_rows
sum_html = "".join(f'<tr><td>{esc(v)}</td><td>{float(m):,.1f}</td><td>{float(sd):,.1f}</td><td>{float(lo):,.1f}</td><td>{float(hi):,.1f}</td></tr>' for v, n, m, sd, lo, hi in tab_rows)
n_sum = tab_rows[0][1].split(".")[0]
th = N["thirds"]
S.append(f'''
<section id="r-sections-1-2" style="padding: 24px 46px;">
  {h2("chart-simple", "Sections 1 and 2: The Table and the Caption")}
  <div style="display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 18px; margin-top: 8px;">
    <div>
      <table class="sumtab"><thead><tr><th>Variable (unit)</th><th>Mean</th><th>SD</th><th>Min</th><th>Max</th></tr></thead><tbody>{sum_html}</tbody></table>
      <p style="font-size: 12pt; color: var(--muted-color); margin-top: 6px;">n = {n_sum} country-years, {N["n_sum_cty"]} countries, {N["sum_y0"]}&ndash;{N["sum_y1"]}, after dropping rows with a gap.</p>
      <p class="fragment fade-up" style="font-size: 13.5pt; margin-top: 10px;" data-notes="The table reads alone when the unit is in the variable name and the sample is stated under it. A reader should never have to ask you what {float(tab_rows[0][2]):.1f} is a percentage of.">Units in the row names and the sample under the table: nobody has to ask what {float(tab_rows[0][2]):.1f} is a percentage of.</p>
    </div>
    <div>
      <img src="figures/flfp_gdp.png" alt="Scatter plot of female labour force participation against GDP per capita on a log scale, synthetic data: points cluster by country and rise with income" style="width: 100%; max-height: 330px; object-fit: contain; border: 1px solid #eee;">
      <p class="fragment fade-up cap bad" data-notes="This caption names the variables. The rubric calls that not finished.">&times; &ldquo;Female LFP and GDP per capita.&rdquo;</p>
      <p class="fragment fade-up cap good" data-notes="This one states the finding, with numbers from the data, so a reader who sees nothing else still learns something.">&check; &ldquo;Female participation rises with income: the poorest third of countries averages {th["poorest"]}%, the richest third {th["richest"]}%.&rdquo;</p>
    </div>
  </div>
  {SYN}
  {notes("3.5 min.", "Section 1's table and Section 2's caption are both graded on whether a reader can understand them without asking you a question.", ["Topic 3's standards in this figure: the y-axis runs 0 to 100, the log scale is said in the axis label, no chartjunk.", "Point at the clusters: each tight group is one country across ten years, which matters again on the threats slide.", "If the outcome is skewed, Section 2 asks you to show it and say what you will do about it."])}
</section>''')

S.append(f'''
<section id="r-section-3" style="padding: 24px 46px;">
  {h2("table", "Section 3: The Table, Two Sentences, a Role per Control")}
  <div style="display: grid; grid-template-columns: 0.8fr 1.2fr; gap: 18px; margin-top: 8px;">
    <div>
      <table class="regtab">
        <thead><tr><th></th><th>Female LFP (pp)</th></tr></thead>
        <tbody>
          <tr><td>log GDP per capita</td><td>{c_log:.2f}<br><span>({s_log:.2f})</span></td></tr>
          <tr><td>Fertility (births)</td><td>{c_fer:.2f}<br><span>({s_fer:.2f})</span></td></tr>
          <tr><td>Paid leave (weeks)</td><td>{c_lw:.2f}<br><span>({s_lw:.2f})</span></td></tr>
          <tr><td>Constant</td><td>{c_int:.2f}<br><span>({s_int:.2f})</span></td></tr>
          <tr class="foot"><td>N</td><td>{N["nobs"]}</td></tr>
          <tr class="foot"><td>R&sup2;</td><td>{float(N["r2"]):.3f}</td></tr>
        </tbody>
      </table>
      <p style="font-size: 11pt; color: var(--muted-color); margin-top: 4px;">OLS; robust (HC1) standard errors in parentheses.</p>
    </div>
    <div>
      <p class="fragment fade-up interp" data-notes="In full means magnitude, units, direction and precision in one sentence. Ten percent more GDP per capita goes with {N['ten_pct']} percentage points more participation, holding the other two fixed, with the interval.">&ldquo;Holding fertility and leave fixed, a country-year with <strong>10% higher GDP per capita</strong> has female participation <strong>{N["ten_pct"]} percentage points</strong> higher (95% CI {N["ten_lo"]} to {N["ten_hi"]}).&rdquo;</p>
      <p class="fragment fade-up interp" data-notes="An imprecise coefficient still gets a full sentence. The interval runs from {lo_f} to plus {hi_f}, so this sample cannot rule out no association, and you say that rather than calling it insignificant.">&ldquo;One more birth per woman goes with participation <strong>{abs(c_fer):.1f} points lower</strong>, but the 95% CI runs from {lo_f} to +{hi_f}: this sample cannot rule out no association.&rdquo;</p>
      <p class="fragment fade-up interp role" data-notes="Every control gets a role. If the question is income's total effect, fertility sits on the path from income to fewer children to more work, so it is a mediator and a bad control. If the question holds family size fixed, it belongs. Say which question you are asking.">Role of fertility: if your question is income&rsquo;s <em>total</em> effect, fertility sits on the path income &rarr; fewer children &rarr; more work. That makes it a mediator and a bad control (Topic 10). Say which question you are asking.</p>
    </div>
  </div>
  {SYN}
  {notes("3.5 min.", "Section 3 is the largest row, and it is graded on sentences: two coefficients in full, and a reason for every control, more than on the table itself.", ["The log GDP sentence uses the coefficient times log of 1.1; students with a logged regressor should do the same arithmetic rather than reading the raw number as a percent.", "\"Statistically significant\" on its own earns nothing; the second sentence shows what to write instead.", "OLS is the required model. If a student has a before-and-after with a comparison group, difference-in-differences belongs in Section 4 as an argument, not as an estimate."])}
</section>''')

vif = N["vif"]
NAMES = {"IND": "India", "NGA": "Nigeria", "BRA": "Brazil", "POL": "Poland", "VNM": "Viet Nam"}
cr = N["cook_rows"]
S.append(f'''
<section id="r-section-4" style="padding: 26px 50px;">
  {h2("stethoscope", "Section 4: Run Each Test, Then Say What It Means")}
  <p style="font-size: 14pt; color: var(--muted-color);">Same model, same data; every number below is from <code>cells/midterm.py</code>, cell <code>r_diag</code>.</p>
  <div class="diag-list">
    <div class="fragment fade-up diag" data-notes="Residual plots: against fitted values and against the main predictor. The thing to write is what shape you see and what it would mean, a fan or a curve."><p class="t">Residuals</p><p>Plot against fitted values and against log GDP. Write down the shape you see: a fan means unequal variance, a curve means the line is the wrong shape.</p></div>
    <div class="fragment fade-up diag" data-notes="Breusch-Pagan p is far below 0.05, so constant variance is rejected, which is why the table on the last slide already uses robust standard errors."><p class="t">Constant variance</p><p>Breusch&ndash;Pagan p = {N["bp_p"]}: rejected, so the table reports robust (HC1) standard errors.</p></div>
    <div class="fragment fade-up diag" data-notes="A VIF needs a sentence. {vif['np.log(gdp_pc)']} on log GDP means its standard error is about {N['sqrt_vif']} times what it would be if log GDP were unrelated to the other regressors."><p class="t">VIF</p><p>log GDP {vif["np.log(gdp_pc)"]}, fertility {vif["fertility"]}, leave {vif["leave_weeks"]}. In a sentence: log GDP&rsquo;s standard error is &radic;{vif["np.log(gdp_pc)"]} = {N["sqrt_vif"]} times what it would be if it were unrelated to the other two.</p></div>
    <div class="fragment fade-up diag" data-notes="Influence: {N['cook_n']} country-years pass the 4 over n line, all {' and '.join(sorted({NAMES[c] for c, _ in cr}))}. Without them the log GDP coefficient falls from {float(N['refit_from']):.2f} to {float(N['refit_to']):.2f}. That sentence goes in the report."><p class="t">Influence</p><p>{N["cook_n"]} of {N["cook_of"]} rows have Cook&rsquo;s D above 4/n, all from {" and ".join(sorted({NAMES[c] for c, _ in cr}))}. Without them, the log GDP coefficient goes from {float(N["refit_from"]):.2f} to {float(N["refit_to"]):.2f}. Report that.</p></div>
  </div>
  {SYN}
  {notes("3 min.", "The rubric says run and interpreted, and the interpreted half is a sentence per test saying what the number means for your answer.", ["Lab 14 runs all four tests on real data; Section 4 is the same code pointed at their own model.", "The influence result is large here on purpose: five rows move the main coefficient by two thirds, and a report that does not say so has missed the most important diagnostic finding.", "Do not tell students to delete influential rows; they report the result with and without."])}
</section>''')

S.append(f'''
<section id="r-threats-repo" style="padding: 28px 50px;">
  {h2("scale-balanced", "Threats, Conclusion, and the Repository", "var(--danger-color)")}
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 10px;">
    <div>
      <p class="sub-h">Threats and conclusion &middot; 10</p>
      <p class="fragment fade-up tbox" data-notes="What would have to be true for the coefficient to be causal: nothing else that differs between richer and poorer countries also moves women's participation. Norms, sector mix and schooling all do.">For the log GDP coefficient to be causal, nothing else that differs between richer and poorer countries could move women&rsquo;s work. Norms, sector mix and schooling all do.</p>
      <p class="fragment fade-up tbox" data-notes="So label it: a conditional association, holding fertility and leave fixed. That is a respectable finding, and the rubric gives the marks for labelling it correctly.">So the estimate is <strong>a conditional association</strong>, holding fertility and leave fixed. Labelled that way, it earns the marks.</p>
      <p class="fragment fade-up tbox" data-notes="{N['n_sum_cty']} countries seen about {N['n_years']} times each are closer to {N['n_sum_cty']} independent observations than to {N['nobs']}. Say that in the threats section; the course has not given you the standard errors that fix it.">{N["n_sum_cty"]} countries seen about {N["n_years"]} times each: closer to {N["n_sum_cty"]} independent observations than to {N["nobs"]}. Say so.</p>
    </div>
    <div>
      <p class="sub-h">Repository &middot; 5</p>
      <div class="fragment fade-up readme" data-notes="The README carries four things: the question, the source with its URL, how to run the notebook, and the headline finding. Plus the data folder or the download step.">
        <pre>README.md
  Question     one sentence
  Data         source + URL + download date
  How to run   open in Colab, run all;
               data/ is in the repo
  Finding      the headline number, in words</pre>
      </div>
      <p style="font-size: 13.5pt; margin-top: 10px;">Conclusion: half a page, how confident a reader should be, what you would do with another month. No new results.</p>
    </div>
  </div>
  {notes("3 min.", "Section 4 ends with what your estimate is if it is not causal, and a conditional association, labelled as one, is a finding the rubric rewards.", ["The README is five points and takes twenty minutes; students lose them by leaving the template text in or by pointing at a file that is only on their laptop.", "The conclusion adds no new results; anything new belongs in an earlier section."])}
</section>''')

# ---------------------------------------------------------------- working time
S.append(f'''
<section id="working-time" style="padding: 34px 50px;">
  {h2("laptop-code", "Ten Minutes on Your Own File", "var(--success-color)")}
  <div class="content">
    <div class="step-row"><p class="n">1</p><p>In a <strong>text cell at the top</strong> of your notebook, write the four lines for your data.</p></div>
    <div class="step-row"><p class="n">2</p><p>Run the checks on your own data: <code>df.shape</code> and <code>df.duplicated([your key]).sum()</code>; <code>df.isna().sum()</code> and one groupby of the gaps by unit or year.</p></div>
    <div class="step-row"><p class="n">3</p><p>If you merged: rerun it with <code>how="outer", indicator=True</code> and write down <strong>rows before, rows after, rows unmatched</strong>.</p></div>
    <div class="key-result" style="margin-top: 16px;"><p>Leave with the four lines written and three numbers you trust. Any number that surprises you: hand up now, or bring it to office hours.</p></div>
    <p style="font-size: 13.5pt; color: var(--muted-color); margin-top: 10px;">Watching the recording? Pause here and do the same three steps before the deadline week.</p>
  </div>
  {notes("10 min.", "Ten minutes, your own data: the four lines in a text cell at the top, the shape and duplicate check, the missing count, and if you merged, the three numbers.", ["Press 9 for the countdown and keep the last minute to close.", "Walk to anyone who voted A in the poll first.", "Close by saying where help is: office hours and the discussion thread."])}
</section>''')

TERM["logistics"] = ("dated slide: midterm Mon 9 Nov 23:59, Quiz 1 closes Sun 8 Nov, PS4 Fri 13 Nov, Lab 14 due tonight.")


def add_term(path: Path) -> None:
    """Put each THIS TERM line first in its slide's note, after the speaker-view pass."""
    src = path.read_text(encoding="utf-8")
    for sid, text in TERM.items():
        at = src.index(f'<section id="{sid}"')
        a = src.index('<aside class="notes"', at)
        gt = src.index(">", a) + 1
        line = (f'<p style="margin:0 0 0.7em" data-term="2026-fall"><strong style="color:#B7791F;'
                f'letter-spacing:.4px">THIS TERM:</strong> {text}</p>')
        if 'data-term="2026-fall"' in src[gt:gt + 400]:
            continue
        src = src[:gt] + line + src[gt:]
    path.write_text(src, encoding="utf-8")
    print("THIS TERM lines:", len(TERM))


if "--term" in sys.argv:
    add_term(DECK / "index.html")
    raise SystemExit(0)

# ---------------------------------------------------------------- assemble
shell = SHELL.read_text(encoding="utf-8")
head, rest = shell.split('<div class="slides">', 1)
tail_at = rest.index("\n    </div>\n  </div>\n\n  <script src=\"https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js\"")
tail = rest[tail_at:]
head = re.sub(r"<title>.*?</title>", "<title>Finishing Your Midterm</title>", head, flags=re.S)
head = head.replace('href="styles.css?v=20260905a"', 'href="styles.css?v=midterm1"')
assert "styles.css?v=midterm1" in head
body = "\n".join(s.strip("\n") for s in S)
page = head + '<div class="slides">\n' + body + tail
(DECK / "index.html").write_text(page, encoding="utf-8")
print(f"wrote {DECK / 'index.html'}: {len(S)} top-level slides, {len(page):,} bytes")
