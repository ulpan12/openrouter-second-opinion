#!/usr/bin/env python3
"""Offline publication checks: bilingual CLI, snapshots, links, and accidental secrets.

This is a lightweight guard, not a comprehensive security audit or DLP system.
No external network access or real credentials are needed.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openrouter_review_v2.py"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_module():
    spec = importlib.util.spec_from_file_location("second_opinion_release_check", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_cli(module, argv):
    output = io.StringIO()
    with mock.patch.object(module.Transport, "send", side_effect=AssertionError("External access forbidden")):
        with mock.patch.object(module.getpass, "getpass", side_effect=AssertionError("Credential access forbidden")):
            with contextlib.redirect_stdout(output):
                result = module.main(argv)
    require(result == 0, f"CLI failed: {argv}")
    return output.getvalue()


def check_languages(module):
    for language, heading, draft_word in (("en", "## Change ledger", "We have proved"),
                                          ("zh", "## 修改账本", "我们已经证明")):
        markdown = run_cli(module, ["--demo", "--language", language])
        require(heading in markdown, f"Wrong {language} heading")
        require("SIMULATED" in markdown, "Demo must be explicitly labeled simulated")
        require(draft_word in markdown, f"Wrong {language} demo content")
        snapshot = ROOT / "examples" / language / "demo-report.md"
        require(snapshot.is_file(), f"Missing {language} demo snapshot")
        require(snapshot.read_text(encoding="utf-8") == markdown, f"Stale {language} demo snapshot")
        data = json.loads(run_cli(module, ["--demo", "--language", language, "--output", "json"]))
        require(data["simulated"] is True and data["budget"] is None, "Demo must not invent measurements")
        require(data["summary"]["decisions"] == {"accept": 2, "reject": 0, "defer": 1}, "Unexpected demo decisions")
        require(data["revision"]["diff"], "Demo needs a reproducible diff")
        require("```diff" in markdown, "Markdown needs a diff block")
        sample = ROOT / "examples" / language
        require((sample / "draft.txt").read_text(encoding="utf-8") == data["input"]["original_answer"],
                f"{language} sample and demo draft diverged")
        preview = json.loads(run_cli(module, [
            "--question-file", str(sample / "question.txt"),
            "--answer-file", str(sample / "draft.txt"),
            "--source-file", str(sample / "source.txt"),
            "--dry-run", "--synthesize", "--language", language, "--output", "json",
        ]))
        require(preview["configuration"]["network_requests"] == 0, "Offline preview must not use network")
        require(preview["configuration"]["credential_reads"] == 0, "Offline preview must not read credentials")
        require(preview["input"]["sources"][0]["id"] == "S1", "Missing source mapping")
        print(f"OK bilingual CLI, offline preview, and snapshot: {language}")
    default = run_cli(module, ["--demo"])
    require("## Change ledger" in default, "Default published CLI language must be English")


def publication_files():
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__", ".venv"} for part in relative.parts):
            continue
        if path.is_symlink():
            raise AssertionError(f"Unexpected symlink: {relative}")
        if path.is_file():
            yield path


def check_publication():
    # Only recognizable token/private-key forms are checked. Synthetic fixtures
    # use non-hex strings so they do not look like real OpenRouter credentials.
    patterns = {
        "OpenRouter key": re.compile(r"sk-or-v1-[0-9a-fA-F]{64}"),
        "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}"),
        "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "personal home path": re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/"),
    }
    count = 0
    for path in publication_files():
        relative = path.relative_to(ROOT)
        require(not (path.name.startswith(".env") or path.suffix in {".key", ".pem", ".p12", ".pfx"}
                     or ".openrouter.key" in path.name), f"Credential/config file must not be published: {relative}")
        require(path.stat().st_size < 1024 * 1024, f"Unexpected large file: {relative}")
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            require(pattern.search(text) is None, f"Possible {label} in {relative}; value suppressed")
        if path.suffix == ".py":
            compile(text, str(relative), "exec")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^\s)]+)\)", text):
                if target.startswith(("https://", "http://", "mailto:", "#")):
                    continue
                destination = target.split("#", 1)[0]
                require((path.parent / destination).is_file(), f"Broken local link in {relative}: {target}")
        count += 1
    for name in ("README.md", "README.zh-CN.md", "SKILL.md", "SKILL.zh-CN.md", "LICENSE", ".github/workflows/test.yml"):
        require((ROOT / name).is_file(), f"Missing publication file: {name}")
    print(f"OK publication scan, local links, and Python syntax: {count} files")


def main():
    module = load_module()
    check_languages(module)
    check_publication()
    print("All release checks passed. No real model calls or credential access.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
