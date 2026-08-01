#!/usr/bin/env python3
"""Measure a Before Human Error draft against the house voice thresholds.

Usage:  python3 check_voice.py draft.md [--baseline published.txt]

The prose rules in SKILL.md and operating_guide "De-AI pass v3" are mostly
judgement calls. These four are not, so they get measured instead of eyeballed.
Everything here is checked against what PUBLISHED issues actually do, not
against a general-purpose ideal — see the TTR note below for why that matters.

Exit code is 0 always; this reports, it does not gate.
"""
import argparse
import re
import statistics
import sys

# House thresholds. Derived from measuring published issues, not adopted blind
# from the avoid-ai-writing skill — see operating_guide "De-AI pass v3".
# Charlie's standing call, 2026-07-29: "basically zero em dashes", all lengths.
# Superseded the earlier 3.0/1k budget that had been derived from published
# Issue 6 (3.70/1k). Issue 8 went to zero with no loss: every one of the 19 in
# the first draft became a comma, a colon or a period, and sentence-length
# variance rose across the edits rather than falling.
EM_DASH_MAX_ABS = 0
ROBOTIC_BAND_MAX_PCT = 45  # share of sentences landing in the 15-25 word band
SENT_STDEV_MIN = 8.0       # sentence-length spread; published Issue 6 ran 8.9

SHORT_FORM_WORDS = 600  # retained: TTR guidance differs by length


def load(path):
    text = open(path, encoding="utf-8").read()
    # Drop markdown headings and emphasis so they don't skew word counts.
    text = re.sub(r"^#+ .*$", "", text, flags=re.M)
    text = re.sub(r"\*\*|\*|`", "", text)
    return text


def measure(text):
    words = re.findall(r"[A-Za-z'’]+", text)
    n = len(words)
    if n == 0:
        raise SystemExit("no prose found")
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if re.findall(r"[A-Za-z'’]+", s)]
    lens = [len(re.findall(r"[A-Za-z'’]+", s)) for s in sents]
    paras = [p for p in text.split("\n\n") if len(p.strip()) > 40]
    plens = [len(re.findall(r"[A-Za-z'’]+", p)) for p in paras] or [0]
    # Unambiguous contraction endings, plus an explicit list for the 's form.
    # A bare \w+'s pattern counts possessives ("the CSB's findings") as
    # contractions, which let a draft with ZERO real ones score as a pass —
    # exactly the tell this check exists to catch.
    contractions = len(re.findall(r"\b\w+['’](?:t|re|ve|ll|d|m)\b", text))
    contractions += len(re.findall(
        r"\b(?:it|that|there|what|he|she|here|let|who|this|one|nobody|"
        r"somebody|everybody|nothing|something)['’]s\b", text, re.I))
    return {
        "words": n,
        "em_per_1k": text.count("—") / n * 1000,
        "em_count": text.count("—"),
        "ttr": len({w.lower() for w in words}) / n,
        "sent_mean": statistics.mean(lens),
        "sent_stdev": statistics.pstdev(lens),
        "robotic_band_pct": sum(1 for l in lens if 15 <= l <= 25) / len(lens) * 100,
        "short_sents": sum(1 for l in lens if l <= 8),
        "long_sents": sum(1 for l in lens if l >= 35),
        "para_stdev": statistics.pstdev(plens),
        "contractions": contractions,
        "contractions_per_1k": contractions / n * 1000,
    }


def report(m, label):
    print(f"\n=== {label} — {m['words']} words ===")

    def line(ok, text):
        print(f"  {'PASS' if ok else 'FLAG'}  {text}")

    line(m["em_count"] <= EM_DASH_MAX_ABS,
         f"em dashes {m['em_count']} (house max {EM_DASH_MAX_ABS}, all lengths; "
         f"{m['em_per_1k']:.2f}/1k)")
    line(m["contractions"] > 0,
         f"contractions {m['contractions']} = {m['contractions_per_1k']:.1f}/1k "
         f"(zero is the single biggest AI tell; Issue 7 shipped with 0)")
    line(m["robotic_band_pct"] <= ROBOTIC_BAND_MAX_PCT,
         f"sentences in the 15-25 word band: {m['robotic_band_pct']:.0f}% (max {ROBOTIC_BAND_MAX_PCT}%)")
    line(m["sent_stdev"] >= SENT_STDEV_MIN,
         f"sentence-length stdev {m['sent_stdev']:.1f} (min {SENT_STDEV_MIN}), "
         f"mean {m['sent_mean']:.1f}, {m['short_sents']} short / {m['long_sents']} long")
    print(f"  ----  paragraph-length stdev {m['para_stdev']:.0f} (want visible variety, no fixed target)")
    print(f"  ----  TTR {m['ttr']:.3f} — REPORTED ONLY, DO NOT CHASE. Type-token ratio falls")
    print("        mechanically as length grows, so the avoid-ai-writing 0.40 floor is a false")
    print("        positive at teardown length: published Issue 6 measured 0.360 at 1,849 words.")
    print("        Compare against a published issue of similar length or ignore it.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--baseline", help="a published issue to compare against")
    a = ap.parse_args()

    report(measure(load(a.draft)), f"DRAFT {a.draft}")
    if a.baseline:
        report(measure(load(a.baseline)), f"BASELINE {a.baseline}")

    print("\nThese four are the measurable slice only. The judgement calls — specific")
    print("first person, one triple-fragment maximum, paragraphs allowed to end flat,")
    print("reshuffle immunity, treadmill test — still need a human read. See SKILL.md.")


if __name__ == "__main__":
    sys.exit(main())
