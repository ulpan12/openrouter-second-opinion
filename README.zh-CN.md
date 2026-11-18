# OpenRouter Second Opinion

**实施之前，让其他模型挑战你的方案。**

[English](README.md) · [简体中文](README.zh-CN.md)

[![离线测试](https://github.com/ulpan12/openrouter-second-opinion/actions/workflows/test.yml/badge.svg)](https://github.com/ulpan12/openrouter-second-opinion/actions/workflows/test.yml)
[![许可证：MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

把 AI 初稿变成一份**可追踪的第二意见**：绑定原文的具体问题、用户提供的证据引句、逐条采纳／拒绝／待确认决策，以及可复现的修订 diff。

不是让几个模型开会投票，而是回答：**哪里需要改、为什么改、什么问题仍未解决。**

> **当前是预览版，不是已验证的事实核查器。** 演示数据为模拟。离线测试不等于多模型一定提升答案质量，目前尚未发布真实模型质量对照基准。本项目独立开发，与 OpenRouter 无隶属关系。

## 30 秒体验：不需要 API Key

需要 Python **3.9+** 和 Git，不需要安装 Python 依赖：

```bash
git clone https://github.com/ulpan12/openrouter-second-opinion.git
cd openrouter-second-opinion
python3 -B openrouter_review_v2.py --demo --language zh
```

Windows 如果没有 `python3` 命令，可改用 `python`。

固定的模拟演示会采纳两项修改，并保留一个待确认问题：

| 初稿判断 | 第二意见 | 决策 |
|---|---|---|
| “所有用户都需要这个功能” | 三位受访者不能代表所有用户 | 采纳 |
| “直接投入三个月开发” | 先用短周期、可逆的步骤验证假设 | 采纳 |
| “成功指标是注册人数” | 应先明确业务目标，再确定指标 | 待确认 |

**以下是模拟演示节选，不是真实模型调用结果：**

```diff
-我们已经证明所有用户都需要这个功能。
+模拟访谈中的3位用户有2位表达了兴趣，但不能证明普遍需求或付费意愿。
-下一步直接投入三个月开发，无需再做验证。
+建议先用一周制作原型并验证关键假设，再决定是否投入三个月开发。
 成功指标是上线后的注册人数。
```

[中文完整演示报告](examples/zh/demo-report.md) · [英文完整演示报告](examples/en/demo-report.md)

## 为什么做这个工具

生成一份自信的初稿很容易。有价值的反对意见应该能展示依据和修改过程。

- **原文锚点**：每条问题对应精确引句，本地计算行号。
- **证据来源**：只匹配你提供的文件，不假装联网搜索或编造外部引用。
- **修改账本**：请求综合时，每条问题都有采纳、拒绝或待确认决策及理由。
- **保守修订**：只在内存中应用唯一、无重叠、通过检查的修改，不覆盖输入文件。
- **诚实统计**：坏 JSON、Schema 错误、空回答、拒答和截断都不算成功评审。
- **模型与费用追踪**：记录请求模型、实际模型、尝试次数、结束原因、token，以及接口返回的实际费用。
- **受约束选模**：实时读取目录能力、价格和上下文信息；没有合适模型就明确失败，不偷偷突破限制换模型。

适用于产品提案、实施方案、研究总结和文章论证。不能替代实际测试、安全审计、专业意见或一手证据。

## 评审自己的初稿

先做离线配置检查：

```bash
python3 -B openrouter_review_v2.py \
  --preset product \
  --question-file examples/zh/question.txt \
  --answer-file examples/zh/draft.txt \
  --source-file examples/zh/source.txt \
  --synthesize --dry-run --language zh
```

**真实运行会把问题、初稿及来源材料发送给 OpenRouter 和路由到的模型供应商，并可能产生费用：**

```bash
python3 -B openrouter_review_v2.py \
  --preset product \
  --question-file examples/zh/question.txt \
  --answer-file examples/zh/draft.txt \
  --source-file examples/zh/source.txt \
  --reviewer-count 3 \
  --synthesize \
  --budget-usd 0.10 \
  --language zh
```

在终端隐藏提示处输入 OpenRouter Key。**不要把 key 粘贴到聊天、Issue 或命令行参数中。** V2 只在内存中使用 key，不读密钥环境变量、不读旧版密钥文件，也不保存 key。当前认证方式不支持在无人交互的 CI 中执行真实评审。

自动选模默认优先选择不同目录作者下的低价付费模型，不代表这些模型已被证明评审效果更好。免费模型需显式加 `--allow-free`。重要任务建议使用 `--models` 指定经过评测的模型，必要时用 `--synthesis-model` 指定综合模型；都必须符合价格和能力限制。目录中存在的 latest 别名可以使用，响应中的实际模型会另行记录。

全部参数：`python3 openrouter_review_v2.py --help`。

## 常用控制项

| 参数 | 默认值／行为 |
|---|---|
| `--demo` | 完全离线，展示模拟账本和 diff |
| `--dry-run` | 只检查离线配置，不验证模型可用性，也不估算真实账单 |
| `--self-test` | 内置离线回归，包含本机 HTTP 端到端测试 |
| `--language en\|zh` | 报告标题和演示语言，默认 `en` |
| `--output markdown\|json` | 默认 Markdown，JSON 字段名保持稳定 |
| `--source-file FILE` | 可重复传入，材料编号为 `S1`、`S2` 等 |
| `--preset` | `general`、`product`、`code`、`writing`、`research` |
| `--reviewer-count` | 自动选模默认 3 个，不重复同一模型凑数 |
| `--synthesize` | 增加逐条决策、最小修改、修订稿与 diff |
| `--max-input-usd-per-million` | `0.50` 美元／百万输入 token |
| `--max-output-usd-per-million` | `2.00` 美元／百万输出 token |
| `--max-request-usd` | `0`，默认不接受额外按次收费的路由 |
| `--budget-usd` | `0.10`，属于客户端估算记账，**不是账单硬上限** |
| `--reasoning` | 默认 `off`，也可选 `auto`、`low`、`medium`、`high` |
| `--retries` | 临时错误最多额外重试 1 次；状态不明的请求仍可能已计费 |

`--language` 不会翻译你的初稿或模型生成内容；真实评审的提示词要求跟随初稿语言。CLI 帮助和机器可读状态名保留英文。

### 退出码

- `0`：完整评审或离线操作成功，**不代表初稿正确**。
- `1`：运行失败或没有有效评审。
- `2`：参数错误。
- `3`：部分成功、原文／来源锚点异常、综合失败或部分修改无法安全应用，仍会输出可用结果。

## 必须了解的边界

**引句匹配不等于事实核实。** 只能证明所给材料包含这些文字，不能证明来源可靠、推理正确；没有证据的意见会保留标识。置信度是模型自报值，未校准。

**估算预算不等于支出保证。** 客户端按路由单价上限保守预留费用，未知费用按估算记账，接口返回费用时记录实际值。供应商计费仍可能不同，建议同时设置上游支出限制。

**结构化输出不等于正确推理。** Schema 只验证格式。不同模型作者仅是多样性代理，不保证推理独立。提示注入防护属于提示约束和局部检查，不是完整安全边界。

报告包含初稿和来源引句，分享前请检查。凭据、隐私和漏洞反馈说明见 [SECURITY.md](SECURITY.md)。

## 作为 Agent Skill 使用

[SKILL.zh-CN.md](SKILL.zh-CN.md) 提供中文执行说明，[SKILL.md](SKILL.md) 为英文版。请按宿主支持的方式加载，并将 Python 文件保留在 Skill 文件旁。本仓库不会自动安装插件、配置 MCP 或修改助手设置。

助手可以执行离线预览。真实运行由人在终端执行并私下输入 key，不应通过聊天收集密钥。

## 测试与贡献

```bash
python3 -B openrouter_review_v2.py --self-test
python3 -B tools/check_release.py
```

测试使用假响应、假 key、临时目录和本机回环服务器，不调用付费模型，也不读取真实密钥。CI 在 Linux、macOS、Windows 上覆盖 Python 3.9、3.12、3.14，并执行上述检查。

欢迎提供可复现的解析失败、更加保守的修订行为、双语文档改进和严谨的质量评测。参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 下一步，不是已实现的功能

- 固定测试集，对比直接修订、单模型自检和多模型评审。
- 重复测量有效问题、误报、错误修改、费用与耗时。
- 改进终端可读性和分发体验。

当前不包含 Fusion 后端、联网搜索、MCP、Web UI、自动修改文件和真实模型 CI 评审。

## 许可证

[MIT](LICENSE)。如果工具确实帮到了你，欢迎点 Star；可复现的案例和诚实的边界说明更有价值。
