"""Process-Safety Teardown Checklist v3.
Type system matches the current brand era: Inter (grotesque) + Roboto Mono for
technical furniture. No serif, no cream, no numbered discs, no rounded corners.
Single red accent, hairline rules, metadata in a left gutter — reads as a
technical bulletin rather than a generated handout.
"""
from xml.sax.saxutils import escape

W = 1200
L, R = 90, 1110          # margins
COL = 216                # content column starts here
PAPER = "#f7f7f4"
INK = "#14161a"
BODY = "#3d434b"
MUTE = "#8b9199"
HAIR = "#dfdfd9"
RED = "#c0392b"

SANS, MONO = "Inter", "Roboto Mono"

CASES = [
    ("Givaudan Sense Colour", "LOUISVILLE, KY · 12 NOV 2024 · 2 FATALITIES · CSB 2024-06-I-KY",
     "The harmless-looking material nobody thought to reactivity-test.",
     ["Reactivity-test your low-hazard materials at real operating and upset conditions.",
      "For anything that could run away, what scenario was the relief actually sized for?",
      "Does your PSM effort chase the scary-sounding chemicals, or the truly reactive ones?"]),
    ("Formosa Plastics", "ILLIOPOLIS, IL · 23 APR 2004 · 5 FATALITIES · CSB 2004-10-I-IL",
     "One bypassable procedure standing in for a real barrier.",
     ["Count the independent protection layers on your top three scenarios. One operator is not one.",
      "Every bypassable interlock: is the bypass managed under MOC, or waved through by phone?",
      "A near-miss at a sister site is your finding too, not “not applicable here.”"]),
    ("Bayer CropScience", "INSTITUTE, WV · 28 AUG 2008 · 2 FATALITIES · CSB 2008-08-I-WV",
     "A startup pushed before the unit was ready to run.",
     ["Your last post-turnaround pre-startup review: performed and closed, or just signed?",
      "New control interface: were operators proven competent before go-live, not during it?",
      "Is the hardest, least-familiar work running on 60-hour weeks and 18-hour shifts?"]),
    ("BP Texas City Refinery", "TEXAS CITY, TX · 23 MAR 2005 · 15 FATALITIES · CSB 2005-04-I-TX",
     "A low injury rate mistaken for a healthy process.",
     ["Split your safety numbers. Can you name one process-safety metric you watch weekly?",
      "Your critical gauges: what is each one calibrated to see, and what is it blind to?",
      "Any relief or PHA study years overdue? That is a decision, not a backlog item."]),
    ("Esso Longford Gas Plant", "LONGFORD, VICTORIA · 25 SEP 1998 · 2 FATALITIES · ROYAL COMMISSION",
     "The people who understood the hazard had been moved off-site.",
     ["Can your shift read the early sign of your worst failure mode, or was it never taught?",
      "Did your last engineering reorg get an MOC review, or pass as an org-chart change?",
      "Near-miss log and HAZOP schedule: is your worst unit's study done, or just planned?"]),
    ("DuPont La Porte", "LA PORTE, TX · 15 NOV 2014 · 4 FATALITIES · CSB 2015-01-I-TX",
     "Every barrier already gone before the last valve was opened.",
     ["Piping moved to clear a plug or restore flow: did that change ever get an MOC?",
      "Is your toxic-gas detection sized for toxicity, or borrowed from a flammability limit far above it?",
      "Count last month's alarms your crews treated as normal. That count is normalized deviance."]),
    ("Aghorn Operating", "ODESSA, TX · 26 OCT 2019 · 2 FATALITIES · CSB 2020-01-I-TX",
     "A safety system that lived in one man's memory.",
     ["Which alarms send a person into the hazard just to learn what the alarm means?",
      "Pull the calibration records for your toxic-gas detection. No records, no detection.",
      "Any energy-isolation step that is not written down is a program running on memory."]),
]

CLOSER_1 = "Seven investigations. Seven headlines that blamed an operator."
CLOSER_2 = "Not one of them held up."


# --- width guard: no check line may exceed the content column ---
from PIL import ImageFont, ImageDraw, Image
_f = ImageFont.truetype("fonts/Inter.ttf", 19)
_d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
_max = R - (COL + 32)
_bad = []
for _n, _m, _fi, _cs in CASES:
    for _c in _cs:
        _w = _d.textlength(_c, font=_f)
        if _w > _max:
            _bad.append((round(_w), _max, _c))
if _bad:
    for _w, _mx, _c in _bad:
        print(f"  OVERFLOW {_w}px > {_mx}px :: {_c}")
    raise SystemExit("width guard failed")
print(f"width guard passed (limit {_max}px)")

STEP = 236
TOP = 322
H = TOP + STEP * len(CASES) + 300

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
     # masthead
     f'<rect x="{L}" y="72" width="38" height="3" fill="{RED}"/>',
     f'<text x="{L}" y="108" font-family="{MONO}" font-size="13" letter-spacing="4.2" fill="{MUTE}">'
     'BEFORE HUMAN ERROR</text>',
     f'<text x="{L}" y="168" font-family="{SANS}" font-weight="600" font-size="46" fill="{INK}">'
     'The Process-Safety Teardown Checklist</text>',
     f'<text x="{L}" y="206" font-family="{SANS}" font-size="21" fill="{BODY}">'
     'Twenty-one checks drawn from seven investigated disasters.</text>',
     f'<text x="{L}" y="234" font-family="{SANS}" font-size="21" fill="{BODY}">'
     'Run them against your own site this week.</text>',
     f'<line x1="{L}" y1="268" x2="{R}" y2="268" stroke="{INK}" stroke-width="1.5"/>']

for i, (name, meta, finding, checks) in enumerate(CASES):
    y = TOP + i * STEP
    o.append(f'<text x="{L}" y="{y}" font-family="{MONO}" font-size="15" fill="{RED}">{i+1:02d}</text>')
    o.append(f'<text x="{COL}" y="{y}" font-family="{SANS}" font-weight="600" font-size="25" fill="{INK}">'
             f'{escape(name)}</text>')
    o.append(f'<text x="{COL}" y="{y+26}" font-family="{MONO}" font-size="11.5" letter-spacing="1.1" '
             f'fill="{MUTE}">{escape(meta)}</text>')
    o.append(f'<text x="{COL}" y="{y+58}" font-family="{SANS}" font-size="19" fill="{BODY}">'
             f'{escape(finding)}</text>')
    for j, c in enumerate(checks):
        by = y + 88 + j * 34
        o.append(f'<rect x="{COL}" y="{by-13}" width="16" height="16" fill="none" '
                 f'stroke="{MUTE}" stroke-width="1.2"/>')
        o.append(f'<text x="{COL+32}" y="{by}" font-family="{SANS}" font-size="18.5" fill="{BODY}">'
                 f'{escape(c)}</text>')
    if i < len(CASES) - 1:
        o.append(f'<line x1="{L}" y1="{y+196}" x2="{R}" y2="{y+196}" stroke="{HAIR}" stroke-width="1"/>')

cy = TOP + STEP * len(CASES) - 30
o.append(f'<rect x="{L}" y="{cy}" width="38" height="3" fill="{RED}"/>')
o.append(f'<text x="{L}" y="{cy+52}" font-family="{SANS}" font-weight="600" font-size="27" fill="{INK}">'
         f'{escape(CLOSER_1)}</text>')
o.append(f'<text x="{L}" y="{cy+90}" font-family="{SANS}" font-weight="600" font-size="27" fill="{INK}">'
         f'{escape(CLOSER_2)}</text>')

fy = cy + 148
o.append(f'<line x1="{L}" y1="{fy}" x2="{R}" y2="{fy}" stroke="{HAIR}" stroke-width="1"/>')
o.append(f'<text x="{L}" y="{fy+36}" font-family="{SANS}" font-size="19" fill="{BODY}">'
         'A new incident teardown every week: the systemic cause behind the '
         '&#8220;operator error&#8221; headline.</text>')
o.append(f'<text x="{L}" y="{fy+66}" font-family="{SANS}" font-weight="600" font-size="19" fill="{INK}">'
         'Subscribe free &#183; before-human-error.beehiiv.com</text>')
o.append(f'<text x="{L}" y="{fy+112}" font-family="{MONO}" font-size="11.5" letter-spacing="0.6" fill="{MUTE}">'
         'SOURCES: U.S. CHEMICAL SAFETY BOARD INVESTIGATION REPORTS; LONGFORD ROYAL COMMISSION (1999).</text>')
o.append(f'<text x="{L}" y="{fy+134}" font-family="{MONO}" font-size="11.5" letter-spacing="0.6" fill="{MUTE}">'
         'BEFORE HUMAN ERROR &#183; PASS IT TO ONE PERSON WHO WOULD GET SOMETHING OUT OF IT.</text>')
o.append('</svg>')

svg = "\n".join(o)
open("checklist-v3.svg", "w").write(svg)
import cairosvg
cairosvg.svg2png(bytestring=svg.encode(), write_to="checklist-v3.png", scale=1.0)
cairosvg.svg2pdf(bytestring=svg.encode(), write_to="checklist-v3.pdf")
from PIL import Image
print("rendered", Image.open("checklist-v3.png").size)
