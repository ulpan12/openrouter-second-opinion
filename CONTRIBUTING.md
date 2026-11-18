# Contributing / 贡献指南

Thanks for helping make second opinions more useful and less misleading.
感谢你帮助第二意见变得更有用、更诚实。

## Before a pull request / 提交前

1. Use Python 3.9+ and keep the runtime standard-library-only.
2. Run both checks from the repository root:

```bash
python3 -B openrouter_review_v2.py --self-test
python3 -B tools/check_release.py
```

3. Keep English and Chinese documentation aligned. Use `--language en` and `--language zh` to check report headings.
4. Never add real API keys, private inputs, live reports, home-directory paths, or paid model calls to tests or CI.
5. Add an offline test for a behavior change. Label fixtures as simulated; do not present them as actual model results.

运行时请保持 Python 3.9+ 与标准库约束；同步中英文文档，行为变化应补离线测试。不要把真实 key、私有输入、真实报告、本机路径或付费模型调用放进测试与 CI。

## Useful issues / 有价值的反馈

- Minimal, sanitized reproductions of invalid responses and unsafe edits.
- Documentation or terminal accessibility problems.
- Evaluation designs that measure false positives and harmful revisions, not just persuasive answers.
- Actual catalog/provider compatibility problems, with keys and private text removed.

欢迎最小且脱敏的解析失败、错误修改、可读性问题、真实接口兼容性问题，以及能够衡量误报和错误修订的评测设计。

## Changing generated examples / 修改演示快照

The committed reports are deterministic simulated fixtures, not benchmark results. Regenerate them after an intentional demo change:

```bash
python3 -B openrouter_review_v2.py --demo --language en > examples/en/demo-report.md
python3 -B openrouter_review_v2.py --demo --language zh > examples/zh/demo-report.md
```

Use a UTF-8 shell or editor. Check the diff before committing. Do not replace the simulation label with an unverified claim of a real run.

演示报告是固定模拟样例，不是质量基准。重新生成后检查 UTF-8 编码与 diff，不要移除模拟标识或宣称未经验证的真实效果。

## Scope / 范围

The project focuses on traceable draft review: anchors, provenance, honest failure accounting, decisions, and minimal revisions. Discuss larger features before implementing a provider framework, autonomous browsing, persistent credentials, or a web application.

本项目优先做好原文锚点、证据来源、诚实统计、逐条决策和最小修改。供应商框架、自主浏览、持久化密钥、Web 应用等大型功能请先讨论。

By contributing, you agree that your contribution may be distributed under the repository's MIT license. / 提交贡献即同意按本仓库 MIT 许可证分发相关贡献。
