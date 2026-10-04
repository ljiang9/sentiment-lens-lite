from __future__ import annotations

import json
import os
import re
import urllib.request

from lexicon import LEXICON, NEUTRAL_THRESHOLD, WINDOW

_EN_WORD_RE = re.compile(r"[a-zA-Z]+")


def scan_hits(text):
    lower = text.lower()
    hits = []

    i, n = 0, len(text)
    while i < n:
        matched = None
        for term, kind, weight in LEXICON:
            if text.startswith(term, i):
                matched = (term, kind, weight)
                break
        if matched is not None:
            term, kind, weight = matched
            hits.append((i, kind, term, weight))
            i += len(term)
        else:
            i += 1

    seen_en = {}
    for m in _EN_WORD_RE.finditer(lower):
        seen_en.setdefault(m.group(0), m.start())
    for term, kind, weight in LEXICON:
        if all(ord(c) < 128 for c in term) and term in seen_en:
            hits.append((seen_en[term], kind, term, weight))

    hits.sort(key=lambda x: x[0])
    return hits


def analyze(text):
    if not text or not text.strip():
        return {"label": "中性", "score": 0.0, "details": "空文本"}

    hits = scan_hits(text)
    score = 0.0
    trace = []

    for pos, kind, term, weight in hits:
        if kind not in ("pos", "neg"):
            continue
        negations = 0
        mult = 1.0
        for ppos, pkind, _, pw in hits:
            if ppos < pos and (pos - ppos) <= WINDOW:
                if pkind == "negation":
                    negations += 1
                elif pkind == "intensifier":
                    mult *= pw
        base = 1.0 if kind == "pos" else -1.0
        flipped = negations % 2 == 1
        sign = -base if flipped else base
        contribution = sign * abs(weight) * mult
        score += contribution
        trace.append(term + "(" + kind + ") base=" + ("+1" if base > 0 else "-1")
                     + " 否定x" + str(negations) + " 程度x" + str(round(mult, 1))
                     + " -> " + ("+" if contribution >= 0 else "") + str(round(contribution, 2)))

    if score > NEUTRAL_THRESHOLD:
        label = "正面"
    elif score < -NEUTRAL_THRESHOLD:
        label = "负面"
    else:
        label = "中性"

    return {"label": label, "score": round(score, 3), "details": trace}


def analyze_llm(text, api_key=None, base_url=None, model=None):
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                or "https://api.openai.com/v1").rstrip("/")
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY")

    prompt = ("请判断下面文本的情感，只返回 JSON，格式 "
              '{"label":"正面/负面/中性","score":数字}。文本：\n' + text)
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }
    req = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + api_key},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"].strip()
    start = content.find("{")
    end = content.rfind("}")
    return json.loads(content[start:end + 1])


def analyze_auto(text, use_llm=True):
    if use_llm and os.environ.get("OPENAI_API_KEY"):
        try:
            return analyze_llm(text)
        except Exception as exc:
            print("[warn] LLM 判定失败，降级词典法：" + str(exc))
    return analyze(text)
