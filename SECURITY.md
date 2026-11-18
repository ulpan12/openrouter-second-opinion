# Security and privacy / 安全与隐私

## Report a vulnerability / 报告漏洞

Please do not include credentials, private drafts, or personal data in public issues.
For a sensitive issue, use this repository's **Security → Advisories → Report a vulnerability** feature if available. If it is unavailable, open a minimal issue requesting a private reporting channel without sharing exploit details or secrets.

请不要在公开 Issue 中附带密钥、私有初稿或个人信息。敏感漏洞可优先通过本仓库 **Security → Advisories → Report a vulnerability** 私下报告；若未启用，先发一个不含漏洞细节和密钥的最小 Issue，请求私下联系渠道。

## Data flow / 数据流

- `--demo`, `--dry-run`, and `--self-test` do not access credentials or external model endpoints. Self-tests may start a temporary loopback HTTP server.
- A live run sends the question, draft, and explicitly supplied source contents to OpenRouter and the selected routed providers.
- Reports contain drafts and source quotations. Review them before sharing.
- V2 prompts for a key using hidden terminal input, holds it in memory, and does not save it. It does not read a legacy key file or a key environment variable.
- Key redaction is a safeguard, not a guarantee that arbitrary input is free of personal information.

- 离线三种模式不读取凭据、不访问外部模型；自测可能启动临时本机 HTTP 服务器。
- 真实运行会把问题、初稿及明确提供的来源内容发送给 OpenRouter 和所选路由供应商。
- 报告含有初稿和来源引句，分享前需检查。
- V2 在终端隐藏输入 key，只在内存中使用，不保存、不读旧版 key 文件或密钥环境变量。
- 密钥打码是保护措施，不保证输入和报告不包含其他个人信息。

## Boundaries / 边界

- Quote matching is provenance, not factual verification.
- Schema validation does not establish reasoning quality.
- Supplied drafts, sources, and model output are untrusted. Prompt instructions are not a complete prompt-injection defense.
- Revisions are computed in memory; input files are not overwritten. Inspect proposed changes before applying them.
- Budget accounting is estimated, not an upstream hard cap. Requests may be billed even when a connection fails. Configure an upstream spending limit.
- HTTP redirects are rejected so that credentials are not deliberately forwarded to a different host.

- 引句匹配不等于事实核实，Schema 通过不等于推理正确。
- 初稿、来源和模型输出都是不可信数据，提示词约束不是完整的提示注入防御。
- 修订仅发生在内存中，不覆盖输入文件；应用前需检查。
- 预算是估算，上游请求即使连接失败也可能计费，请同时设置上游支出限制。
- 程序拒绝 HTTP 重定向，避免主动向其他主机转发凭据。

## Supported preview / 支持状态

This repository currently contains a preview implementation. No guarantee of model accuracy, provider availability, financial outcomes, or suitability for high-stakes use is made. Use tests, primary evidence, and qualified human review where appropriate.

当前为预览实现，不保证模型准确率、供应商可用性、财务结果或高风险任务适用性。必要时结合实际测试、一手证据及专业人工复核。
