---
name: openrouter-second-opinion
description: 使用 OpenRouter 对初稿、产品提案、实施方案或研究总结做第二意见评审，输出绑定原文与来源的引句、采纳/拒绝/待确认决策，以及保守修订 diff，而不是多数投票。
---

# OpenRouter Second Opinion

[English instructions](SKILL.md) · [项目中文说明](README.zh-CN.md)

当用户希望在实施前复核方案、挑战初稿，或需要可追踪的多模型评审时使用。当前是预览版，不是已验证的独立事实核查器。

## 文件与模式

- `openrouter_review_v2.py`：Python 3.9+，仅依赖标准库。
- `--demo`：明确标注为模拟的离线演示。
- `--dry-run`：离线配置预览，不验证模型可用性。
- `--self-test`：确定性的离线回归测试。

请以本 Skill 文件为基准定位 Python 文件，不要假设某个用户的固定主目录。宿主不支持 Skill 加载时，也能直接运行 CLI；安装方式由宿主决定。

## 工作流

1. 获取原始问题和完整初稿，保留原文。
2. 确认哪些来源材料允许发送给外部供应商，不扫描或读取无关文件及凭据。
3. 选择 `--preset general|product|code|writing|research`。
4. 先用 `--dry-run` 检查输入。中文报告标题使用 `--language zh`，英文使用 `--language en`；模型生成的正文跟随初稿语言。
5. 真实运行前说明：问题、初稿及来源会发送给 OpenRouter 和路由到的模型供应商，可能计费。必须由人在终端执行命令并私下输入 key。不要通过聊天收集密钥，也不要放进参数、文件、日志或环境变量。
6. 阅读账本和修订状态，而不是统计赞成票。明确报告无效输出、来源不匹配、锚点缺失、保留意见和被拒绝的修改。
7. 修订稿只是供人检查的提案。未经另外授权，不要应用到用户文件。

## 命令

离线演示：

```bash
python3 -B openrouter_review_v2.py --demo --language zh
```

使用用户批准的文件做离线预览：

```bash
python3 -B openrouter_review_v2.py \
  --preset product --question-file question.md --answer-file draft.md \
  --source-file evidence.md --synthesize --dry-run --language zh
```

真实运行，由人在可交互终端执行：

```bash
python3 -B openrouter_review_v2.py \
  --preset product --question-file question.md --answer-file draft.md \
  --source-file evidence.md --reviewer-count 3 --synthesize \
  --budget-usd 0.10 --language zh
```

## 规则

- 不读密钥环境变量、不读旧版密钥文件；V2 不持久化保存 key。
- 引句匹配只证明材料包含原文，不证明事实、结论或来源可靠。
- 模型自报置信度未校准；目录作者不同不保证推理独立。
- 预算是客户端估算记账，不是账单硬上限，不得承诺绝对费用保证。
- 坏 JSON 和截断属于失败，即使 HTTP 200。退出码 `3` 表示部分结果可用但不完整。
- 目前没有真实模型质量对照基准，不得把模拟演示冒充真实调用结果。
- 未经明确许可，不上传用户私有输入或报告到公开仓库。
- 不得悄悄更换模型、放宽约束，或为了更有利的结论重跑付费请求。
