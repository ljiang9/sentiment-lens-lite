from __future__ import annotations

import argparse
import sys

from sentiment import analyze, analyze_auto


def build_parser():
    p = argparse.ArgumentParser(
        prog="sentiment-lens-lite",
        description="零依赖词典法情感分析（可选 LLM 判定）",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="单条文本情感分析")
    src.add_argument("--file", help="批量文件，每行一条")
    p.add_argument("--llm", action="store_true", help="尝试调用 LLM 判定")
    p.add_argument("--no-llm", action="store_true", help="强制使用词典法")
    p.add_argument("--verbose", action="store_true", help="打印逐词打分明细")
    return p


def _print_one(text, result, verbose):
    print("文本: " + text)
    print("  判定: " + result["label"] + "   分数: " + str(result["score"]))
    if verbose and result.get("details"):
        for d in result["details"]:
            print("    - " + d)


def main(argv=None):
    args = build_parser().parse_args(argv)
    use_llm = args.llm and not args.no_llm

    if args.text:
        r = analyze_auto(args.text, use_llm=use_llm)
        _print_one(args.text, r, args.verbose)
        return 0

    with open(args.file, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    pos = neg = neu = 0
    for ln in lines:
        r = analyze_auto(ln, use_llm=use_llm)
        _print_one(ln, r, args.verbose)
        if r["label"] == "正面":
            pos += 1
        elif r["label"] == "负面":
            neg += 1
        else:
            neu += 1
    print("---")
    print("共 %d 条：正面 %d / 负面 %d / 中性 %d" % (len(lines), pos, neg, neu))
    return 0


if __name__ == "__main__":
    sys.exit(main())
