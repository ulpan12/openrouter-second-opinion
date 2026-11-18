---
name: openrouter-second-opinion
description: Challenge a draft, product proposal, implementation plan, or research summary with independently prompted OpenRouter reviewers. Produce exact draft/source quotes, accept/reject/defer decisions, and a conservative revision diff instead of a majority vote.
---

# OpenRouter Second Opinion

[中文说明](SKILL.zh-CN.md) · [Project README](README.md)

Use when a person asks for a second opinion before implementing a plan, wants a draft challenged, or wants traceable multi-model review. This is a preview, not an independently verified fact checker.

## Files

- `openrouter_review_v2.py`: standard-library-only CLI, Python 3.9+.
- `--demo`: explicitly simulated offline example.
- `--dry-run`: offline configuration preview, not a model availability check.
- `--self-test`: deterministic offline regression suite.

Resolve the Python file relative to this Skill file. Do not assume a particular user's home directory. If the host does not support Skill loading, the CLI still works directly; installation is host-specific.

## Workflow

1. Write or obtain the original question and a complete draft. Preserve the original.
2. Ask which source materials may be sent to external providers. Do not discover or read unrelated files or credentials.
3. Classify the work using `--preset general|product|code|writing|research`.
4. Preview the inputs with `--dry-run`. Use `--language en` for English report headings or `--language zh` for Chinese. Model-authored text follows the draft language.
5. For a live run, explain that question, draft, and supplied sources are transmitted to OpenRouter and routed providers and may incur charges. A person must run the command in a terminal and enter the key privately. Never collect a key through chat or add one to arguments, files, logs, or environment variables.
6. Read the ledger and revision status, not a majority vote. Report invalid completions, source mismatches, missing anchors, unresolved dissent, and rejected edits.
7. Treat the revised answer as a proposal for human inspection. Do not apply it to the user's files without a separate request.

## Commands

Offline demonstration:

```bash
python3 -B openrouter_review_v2.py --demo --language en
```

Offline preview using user-approved local files:

```bash
python3 -B openrouter_review_v2.py \
  --preset product --question-file question.md --answer-file draft.md \
  --source-file evidence.md --synthesize --dry-run --language en
```

Live review, to be run by a person in an interactive terminal:

```bash
python3 -B openrouter_review_v2.py \
  --preset product --question-file question.md --answer-file draft.md \
  --source-file evidence.md --reviewer-count 3 --synthesize \
  --budget-usd 0.10 --language en
```

## Rules

- No key is read from the environment or a legacy key file; V2 has no persistent key storage.
- An exact source match proves provenance only, not truth or source reliability.
- Model self-confidence is uncalibrated. Distinct catalog authors do not prove independent reasoning.
- Budget accounting is estimated, not a billing hard cap. Never promise a guaranteed spend ceiling.
- Malformed/truncated outputs are failures, even with HTTP 200. Exit code `3` means useful but partial results.
- No live model quality benchmark is included. Never present the simulated demo as real model output.
- Do not upload private inputs or reports to public repositories without explicit permission.
- Do not silently change models, weaken constraints, or rerun paid requests to obtain a more favorable verdict.
