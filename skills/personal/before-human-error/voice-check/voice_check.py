#!/usr/bin/env python3
"""De-AI voice check for Before Human Error drafts.

Exists because "de-AI pass: YES" was self-certified on Issue 7 and the piece
still shipped with zero contractions, four triple-fragments and a balanced
beat closing most paragraphs. A prose rule that a writer grades themselves on
is not a gate. This prints numbers and exits non-zero.

Usage:
    python3 voice_check.py draft.md              # gate: exits 1 on failure
    python3 voice_check.py draft.md --report     # numbers only, always exit 0
"""
import re
import sys
from statistics import mean, pstdev

# Connector throat-clearing. Saying the next thing beats announcing it.
CONNECTORS = [
    "worth stopping on", "here is the thing", "here's the thing",
    "the thing is", "what you're describing is", "what you have added is",
    "what you've added is", "the part that matters", "which is worth saying",
    "it is worth noting", "it's worth noting", "worth noting that",
    "here is what", "here's what", "make no mistake", "let me be clear",
    "the reality is", "at the end of the day", "it is not just", "it's not just",
]

# Explicit list, not a pattern: a regex for apostrophe-s cannot tell the
# contraction "it's" from the possessive "Aghorn's", and counting possessives
# inflates the score badly on copy full of company names.
CONTRACTIONS = [
    "aren't", "can't", "couldn't", "didn't", "doesn't", "don't", "hadn't",
    "hasn't", "haven't", "isn't", "mustn't", "shouldn't", "wasn't", "weren't",
    "won't", "wouldn't", "ain't", "he's", "here's", "how's", "i'd", "i'll",
    "i'm", "i've", "it's", "let's", "she's", "that's", "there's", "they'd",
    "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've",
    "what's", "who's", "you'd", "you'll", "you're", "you've", "would've",
    "could've", "should've",
]
CONTRACTION = re.compile(
    r"\b(" + "|".join(c.replace("'", "['’]") for c in CONTRACTIONS) + r")\b", re.I
)

THRESHOLDS = {
    "contractions_per_1k": (6.0, "min"),   # zero reads synthetic over long copy
    "triple_fragments": (1, "max"),        # great device, once
    "para_punch_rate_pct": (55.0, "max"),  # not every paragraph earns a beat
    "connector_hits": (0, "max"),
    "sentence_len_stdev": (8.0, "min"),    # AI hovers 15-25 words
}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def analyse(text):
    # strip markdown furniture and figure markers so prose is measured, not scaffolding
    body = re.sub(r"^\s*(#{1,6}|>|\||\d+\.|[-*•])\s*", "", text, flags=re.M)
    body = re.sub(r"\[.*?\]|\{.*?\}|https?://\S+", "", body)
    paras = [p.strip() for p in body.split("\n\n") if len(p.strip()) > 40]
    sents = sentences(body)
    words = re.findall(r"[A-Za-z']+", body)
    wc = len(words)

    lens = [len(re.findall(r"[A-Za-z']+", s)) for s in sents]
    lens = [n for n in lens if n > 0]

    # three or more consecutive short sentences = the punch-fragment stack
    triples, run = 0, 0
    for n in lens:
        run = run + 1 if n <= 6 else 0
        if run == 3:
            triples += 1
    # paragraphs whose last sentence is a short beat
    punchy = 0
    for p in paras:
        ss = sentences(p)
        if ss and len(re.findall(r"[A-Za-z']+", ss[-1])) <= 6:
            punchy += 1

    low = body.lower()
    hits = [c for c in CONNECTORS if c in low]

    return {
        "words": wc,
        "sentences": len(sents),
        "paragraphs": len(paras),
        "contractions": len(CONTRACTION.findall(body)),
        "contractions_per_1k": round(len(CONTRACTION.findall(body)) / wc * 1000, 2) if wc else 0,
        "triple_fragments": triples,
        "para_punch_rate_pct": round(punchy / len(paras) * 100, 1) if paras else 0,
        "connector_hits": len(hits),
        "connectors_found": hits,
        "sentence_len_mean": round(mean(lens), 1) if lens else 0,
        "sentence_len_stdev": round(pstdev(lens), 1) if lens else 0,
        "longest_sentence": max(lens) if lens else 0,
        "shortest_sentence": min(lens) if lens else 0,
        "em_dashes_per_1k": round(body.count("—") / wc * 1000, 2) if wc else 0,
    }


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    report_only = "--report" in sys.argv
    m = analyse(open(sys.argv[1], encoding="utf-8").read())

    print(f"\n  {m['words']} words · {m['sentences']} sentences · {m['paragraphs']} paragraphs\n")
    failed = []
    for key, (limit, kind) in THRESHOLDS.items():
        val = m[key]
        ok = val >= limit if kind == "min" else val <= limit
        print(f"  {'PASS' if ok else 'FAIL'}  {key:24} {val:>7}   ({kind} {limit})")
        if not ok:
            failed.append(key)

    print(f"\n  sentence length: mean {m['sentence_len_mean']}, "
          f"stdev {m['sentence_len_stdev']}, range {m['shortest_sentence']}-{m['longest_sentence']}")
    print(f"  em-dashes per 1k words: {m['em_dashes_per_1k']}")
    if m["connectors_found"]:
        print("  connectors found: " + ", ".join(repr(c) for c in m["connectors_found"]))

    if failed and not report_only:
        print(f"\n  VOICE CHECK FAILED on: {', '.join(failed)}\n")
        sys.exit(1)
    print("\n  voice check passed\n" if not failed else "\n  (report mode)\n")


if __name__ == "__main__":
    main()
