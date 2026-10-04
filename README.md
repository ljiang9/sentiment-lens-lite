# 词典法情感分析小工具（sentiment-lens-lite）

一个 **零第三方依赖** 的 Python 情感分析命令行工具。基于内置小型褒贬义词表，
处理否定词翻转与程度副词加权；有 OpenAI 兼容 Key 时可切换 LLM 判定。

## 功能简介

- 内置小型褒义 / 贬义词表（中英双语）；
- 否定词翻转：「不 / 没 / not / never …」会翻转紧邻情感词的极性，支持双重否定；
- 程度副词加权：「非常 / 极其 / very / extremely …」放大情感强度；
- 输出 `正面 / 负面 / 中性` 判定与数值分数；
- 支持单条文本 `--text` 与批量文件 `--file`（每行一条）；
- 可选 LLM 判定：通过 `urllib` 调 OpenAI 兼容接口，要求返回 JSON。

## 快速开始

环境要求：Python 3.10+（验证于 3.12），无需安装任何依赖。

```bash
git clone https://github.com/ljiang9/sentiment-lens-lite.git
cd sentiment-lens-lite
```

## 使用示例

单条文本：

```bash
python3 cli.py --text "这家餐厅菜很好吃，服务也很棒" --verbose
```

批量文件（每行一条评论）：

```bash
python3 cli.py --file comments.txt
```

启用 LLM 判定：

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可选
python3 cli.py --text "这家店怎么样？" --llm
```

## 无 API Key 如何运行

**完全不需要 Key**。默认走内置词典法，开箱即用：

```bash
unset OPENAI_API_KEY
python3 cli.py --text "这家店太难吃了，服务很差"
```

LLM 调用失败时自动降级回词典法，并打印 `[warn]`。

## 目录结构

```
sentiment-lens-lite/
├── cli.py            # 命令行入口
├── sentiment.py     # 扫描 / 打分 / 判定 / 可选 LLM
├── lexicon.py        # 内置褒贬义词、否定词、程度副词表
├── comments.txt      # 批量示例输入
├── tests/
│   └── test_sentiment.py
├── README.md
├── LICENSE           # MIT
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

MIT License，见 [LICENSE](./LICENSE)。
