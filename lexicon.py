ZH_POSITIVE = ["好", "棒", "优秀", "喜欢", "开心", "满意", "精彩", "赞",
               "出色", "成功", "漂亮", "舒服", "推荐", "惊喜", "美味", "不错"]

ZH_NEGATIVE = ["差", "坏", "糟糕", "讨厌", "失望", "生气", "难过", "烂",
               "差劲", "投诉", "难吃", "垃圾", "坑", "敷衍", "慢"]

ZH_NEGATION = ["不", "没", "无", "别", "未", "没有"]

ZH_INTENSIFIERS = {
    "很": 1.5,
    "非常": 2.0,
    "极其": 2.5,
    "特别": 1.8,
    "太": 1.8,
    "十分": 1.8,
    "更加": 1.5,
    "最": 2.0,
}

EN_POSITIVE = ["good", "great", "excellent", "happy", "love", "awesome",
               "nice", "wonderful", "amazing", "satisfied", "best", "beautiful"]

EN_NEGATIVE = ["bad", "terrible", "awful", "hate", "poor", "disappointed",
               "worst", "ugly", "broken", "slow", "boring"]

EN_NEGATION = ["not", "no", "never", "dont", "doesnt", "isnt", "arent",
               "wasnt", "wont", "cant"]

EN_INTENSIFIERS = {
    "very": 1.5,
    "extremely": 2.5,
    "really": 1.8,
    "so": 1.5,
    "quite": 1.3,
    "totally": 2.0,
}


def build_lexicon():
    lex = []
    for w in ZH_POSITIVE:
        lex.append((w, "pos", 1.0))
    for w in ZH_NEGATIVE:
        lex.append((w, "neg", 1.0))
    for w in ZH_NEGATION:
        lex.append((w, "negation", 0.0))
    for w, mult in ZH_INTENSIFIERS.items():
        lex.append((w, "intensifier", mult))

    for w in EN_POSITIVE:
        lex.append((w.lower(), "pos", 1.0))
    for w in EN_NEGATIVE:
        lex.append((w.lower(), "neg", 1.0))
    for w in EN_NEGATION:
        lex.append((w.lower(), "negation", 0.0))
    for w, mult in EN_INTENSIFIERS.items():
        lex.append((w.lower(), "intensifier", mult))

    lex.sort(key=lambda x: len(x[0]), reverse=True)
    return lex


LEXICON = build_lexicon()

NEUTRAL_THRESHOLD = 0.5

WINDOW = 4
