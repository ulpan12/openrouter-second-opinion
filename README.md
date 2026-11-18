# OpenRouter Second Opinion

**Before you ship, let other models challenge the plan.**

[English](README.md) · [简体中文](README.zh-CN.md)

[![Offline tests](https://github.com/ulpan12/openrouter-second-opinion/actions/workflows/test.yml/badge.svg)](https://github.com/ulpan12/openrouter-second-opinion/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Turn an AI-generated draft into a **traceable second opinion**: exact draft quotes, supplied-source citations, explicit accept/reject/defer decisions, and a reproducible revision diff.

Not another chat room where several models vote. The useful output is **what should change, why, and what remains unresolved**.

> **Preview, not a verified fact-checker.** The demo is simulated. Offline tests do not establish that multiple models improve answer quality. No live quality benchmark is published yet. Independent project; not affiliated with OpenRouter.

## Try it in 30 seconds — no API key

Python **3.9+**, Git, and no Python dependencies:

```bash
git clone https://github.com/ulpan12/openrouter-second-opinion.git
cd openrouter-second-opinion
python3 -B openrouter_review_v2.py --demo --language en
```

On Windows, use `python` instead of `python3` if necessary.

The fixed, clearly labeled demo accepts two changes and leaves one question open:

| Draft claim | Second opinion | Decision |
|---|---|---|
| “All users need this feature.” | Three interviewees cannot establish universal demand. | Accept |
| “Commit to a three-month build immediately.” | Recommend a short, reversible validation step. | Accept |
| “Success means sign-ups.” | Clarify the goal before choosing a metric. | Defer |

**Illustrative excerpt from the simulated demo, not real model output:**

```diff
-We have proved that all users need this feature.
+Two of three simulated interviewees expressed interest; broad demand and willingness to pay remain unproven.
-Commit to a three-month build immediately; no further validation is needed.
+Prototype for one week and test the key assumptions before deciding on a three-month build.
 Success means the number of sign-ups after launch.
```

[Full English demo report](examples/en/demo-report.md) · [Full Chinese demo report](examples/zh/demo-report.md)

## Why this exists

A confident draft is easy to produce. A useful challenge should show its work.

- **Anchored findings:** exact draft quotations with locally computed line numbers.
- **Evidence provenance:** quote matching against files you provide, not invented browsing or citations.
- **Decision ledger:** each finding is accepted, rejected, or deferred with a reason when synthesis is requested.
- **Conservative revisions:** only unique, non-overlapping, validated edits are applied in memory. Your files are never overwritten.
- **Honest success accounting:** malformed JSON, invalid schemas, empty answers, refusals, and truncated output are not successful reviews.
- **Model and cost trace:** requested and resolved models, attempts, finish reasons, token usage, and reported cost when available.
- **Constrained model discovery:** current catalog metadata, strict-output capability checks, context checks, and price ceilings; no silent unconstrained fallback.

Useful for product proposals, implementation plans, research summaries, and written arguments. It is **not** a substitute for tests, security audits, professional advice, or primary evidence.

## Review your own draft

Start with an offline configuration check:

```bash
python3 -B openrouter_review_v2.py \
  --preset product \
  --question-file examples/en/question.txt \
  --answer-file examples/en/draft.txt \
  --source-file examples/en/source.txt \
  --synthesize --dry-run --language en
```

A **live run sends your question, draft, and supplied sources to OpenRouter and the routed providers**, and may incur charges:

```bash
python3 -B openrouter_review_v2.py \
  --preset product \
  --question-file examples/en/question.txt \
  --answer-file examples/en/draft.txt \
  --source-file examples/en/source.txt \
  --reviewer-count 3 \
  --synthesize \
  --budget-usd 0.10 \
  --language en
```

Enter your OpenRouter key at the hidden terminal prompt. **Do not paste keys into chat, issues, or arguments.** V2 keeps the key in memory only; it does not read environment variables or legacy key files, and it never saves the key. Non-interactive CI cannot run live reviews with this authentication design.

By default, selection favors inexpensive paid models from distinct catalog authors, not proven review quality. Zero-priced models require `--allow-free`. For important work, pass evaluated catalog IDs using `--models` and choose an editor with `--synthesis-model`; all must satisfy your constraints. Catalog aliases are accepted when present, and the actual response model is recorded.

Run `python3 openrouter_review_v2.py --help` for the complete CLI.

## Controls worth knowing

| Option | Default / behavior |
|---|---|
| `--demo` | Fully offline, simulated ledger and diff |
| `--dry-run` | Offline configuration only; does not query model availability or estimate a real bill |
| `--self-test` | Built-in offline regression suite, including loopback HTTP |
| `--language en\|zh` | Report headings and demo language; default `en` |
| `--output markdown\|json` | Default `markdown`; JSON field names remain stable |
| `--source-file FILE` | Repeatable; files become `S1`, `S2`, … |
| `--preset` | `general`, `product`, `code`, `writing`, or `research` |
| `--reviewer-count` | Default 3 for auto-selection; never duplicates reviewers to fill a shortage |
| `--synthesize` | Adds decisions, minimal edits, revised draft, and diff |
| `--max-input-usd-per-million` | `0.50` |
| `--max-output-usd-per-million` | `2.00` |
| `--max-request-usd` | `0`; rejects per-call paid routes unless changed |
| `--budget-usd` | `0.10`; estimated client-side accounting, **not a billing hard cap** |
| `--reasoning` | `off`; also `auto`, `low`, `medium`, `high` |
| `--retries` | 1 extra attempt for transient errors; an ambiguous request may still be billed |

`--language` does not translate your draft or model-authored content. Live prompts request the draft's language. English is used for CLI help and machine-readable states.

### Exit codes

- `0`: complete review or successful offline action. It does **not** mean the draft is correct.
- `1`: operational failure or no valid reviews.
- `2`: invalid arguments.
- `3`: partial results, anchor/source problems, failed synthesis, or edits that could not safely be applied. Useful partial output is still printed.

## Trust boundaries

**Quote match ≠ fact verification.** A matching quotation only shows that supplied text contains those words. It does not prove the source is reliable or the conclusion is true. Missing evidence remains visible. Model confidence is self-reported, not calibrated.

**Estimated budget ≠ guaranteed spend cap.** The client reserves conservative estimates against routing price ceilings, keeps unknown-cost attempts as estimates, and reports actual cost when returned. Provider billing can differ. Set an upstream spending limit as well.

**Structured output ≠ correct reasoning.** Schema validation checks shape, not truth. Distinct model authors are a diversity proxy, not proof of independent reasoning. Prompt-injection defenses are instructions and local safeguards, not a complete security boundary.

Reports contain your draft and evidence quotations. Review them before sharing. See [SECURITY.md](SECURITY.md) for credential, privacy, and disclosure guidance.

## Use as an agent skill

[SKILL.md](SKILL.md) contains host-neutral instructions for a coding assistant; [SKILL.zh-CN.md](SKILL.zh-CN.md) is the Chinese version. Load it using your host's supported skill mechanism and keep the Python file beside it. This repository does not auto-install plugins, configure an MCP server, or change your assistant settings.

An assistant can perform the offline preview. A person must run the live command in a terminal and enter the key privately. Never ask the assistant to collect the key through chat.

## Test and contribute

```bash
python3 -B openrouter_review_v2.py --self-test
python3 -B tools/check_release.py
```

Tests use fake responses, fake keys, temporary directories, and a loopback server. They do not call paid models or read real credentials. CI runs both checks on Linux, macOS, and Windows with Python 3.9, 3.12, and 3.14.

Contributions most welcome: reproducible parsing failures, safer revision behavior, bilingual documentation improvements, and well-designed quality evaluations. See [CONTRIBUTING.md](CONTRIBUTING.md).

### Next, not already shipped

- A fixed evaluation set comparing direct revision, self-review, and multi-model review.
- Repeated measurements of useful findings, false positives, regressions, cost, and latency.
- More accessible terminal output and distribution improvements.

Fusion, web search, MCP, a web UI, automatic file changes, and live CI reviews are not implemented in this preview.

## License

[MIT](LICENSE). If this is useful, a star helps other people discover it. Reproducible examples and honest limitations help even more.
