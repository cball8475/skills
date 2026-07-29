# The Process-Safety Teardown Checklist (lead magnet)

The one-page checklist promised in every issue's pinned first comment and
delivered by the beehiiv welcome automation. One section per published issue,
three checks each.

## Regenerate

```bash
pip install pillow cairosvg
python3 make_checklist.py     # writes checklist-v3.{svg,png,pdf}
```

The script expects these files in a `fonts/` directory beside it. They are not
committed (Google Fonts, freely redistributable, but no need to vendor
binaries). Fetch the current URLs from the Google Fonts CSS API with a browser
User-Agent, which returns TTF rather than WOFF2:

```bash
mkdir -p fonts
for q in "Inter:wght@400" "Inter:wght@600" "Roboto+Mono:wght@400"; do
  curl -sS -A "Mozilla/5.0" "https://fonts.googleapis.com/css2?family=$q&display=swap"
done | grep -oE "https://fonts.gstatic.com[^)]+\.ttf"
# save as fonts/Inter.ttf, fonts/InterSemiBold.ttf, fonts/RobotoMono.ttf
```

`cairosvg` renders text using **system-installed** fonts, not the files in
`fonts/`. Install them system-wide before rendering or the output silently
falls back to a default face:

```bash
cp fonts/*.ttf /usr/share/fonts/truetype/bhe/ && fc-cache -f
```

## Adding an issue

Append a tuple to `CASES` — `(name, metadata, finding, [three checks])`. Keep
the metadata format identical to the issue covers:
`LOCATION · DD MMM YYYY · N FATALITIES · CSB CASE-NO`. Update the deck line
(`Twenty-one checks drawn from seven investigated disasters`) to the new
counts. Canvas height is computed from `len(CASES)`, so nothing else moves.

Take the three checks from the article's Monday Morning Checklist. The pinned
first comment usually points at one of them by number, so they should match.

## The width guard

`make_checklist.py` measures every check line against the content column in the
real font and **exits non-zero** if any overflows. This is not decoration: on
the v3 build it caught three lines that had already been eyeballed and passed,
and one of those had shipped visibly clipped in v2. Do not remove it, and do
not raise the limit to make a line fit — shorten the line.

## Design notes

Type system matches the current cover era: Inter for anything readable, Roboto
Mono (letter-spaced) for technical furniture, single red accent `#c0392b`, no
serif, no rounded corners, hairline rules. An earlier version used Georgia on
cream with numbered discs and was rejected as looking machine-generated.

Full cover/brand spec lives in D1 `operating_guide`, section
"Issue cover template (visual system)".

## Hosting

Embedded directly in the beehiiv welcome automation email. beehiiv uploads it
to its own CDN, so right-clicking the embedded image in the editor yields a
permanent public `beehiiv-images-production.s3.amazonaws.com` URL — use that
for the "open full size" link rather than standing up separate hosting. The
email is re-edited each time a section is added, so a stable external URL buys
nothing.
