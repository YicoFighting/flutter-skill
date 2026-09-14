#!/usr/bin/env python3
"""Validate Tuqiang locale JSON and changed literal translation calls."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


I18N_DIR = Path("apps/tuqiang_app/assets/i18n")
DART_SCOPE = ("apps/tuqiang_app", "apps/standard", "apps/ohos", "packages")
TOKEN_RE = re.compile(r"\{([^{}]*)\}")
NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
CALL_RE = re.compile(r"\.(tr\b|keyTr\s*\(|multiKeyTr\s*\()")
BRACKETS = {"(": ")", "[": "]", "{": "}"}
ESCAPES = {"n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f"}


class ValidationError(Exception):
    pass

class Call(NamedTuple):
    key: str
    method: str
    parameters: frozenset[str] | None
    source: str
    first_line: int
    last_line: int

def _git(root: Path, *args: str, required: bool = True) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, encoding="utf-8", errors="strict", check=False,
    )
    if not result.returncode:
        return result.stdout
    if not required:
        return None
    detail = result.stderr.strip() or result.stdout.strip()
    raise ValidationError(f"git {' '.join(args)} 失败: {detail}")

def _json_object(text: str, label: str) -> dict[str, object]:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in items:
            if key in result:
                raise ValidationError(f"重复 JSON key: {key!r}")
            result[key] = value
        return result

    def reject(value: str) -> object:
        raise ValidationError(f"非标准 JSON 数值: {value}")

    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=reject)
    except (json.JSONDecodeError, ValidationError) as error:
        raise ValidationError(f"{label}: {error}") from error
    if not isinstance(value, dict): raise ValidationError(f"{label}: 顶层必须是 JSON object")
    return value

def _read_json(path: Path) -> dict[str, object]:
    try:
        return _json_object(path.read_text(encoding="utf-8"), str(path))
    except (OSError, UnicodeError) as error:
        raise ValidationError(f"{path}: 无法按 UTF-8 读取: {error}") from error

def _head_json(root: Path, relative: Path) -> dict[str, object]:
    text = _git(root, "show", f"HEAD:{relative.as_posix()}", required=False)
    try:
        return {} if text is None else _json_object(text, str(relative))
    except ValidationError:
        return {}

def _unescape(body: str, raw: bool) -> str:
    if raw or "\\" not in body:
        return body
    result: list[str] = []
    index = 0
    while index < len(body):
        slash = body.find("\\", index)
        if slash < 0:
            result.append(body[index:])
            break
        result.append(body[index:slash])
        index = slash + 1
        if index == len(body):
            result.append("\\")
            break
        escape = body[index]
        index += 1
        if escape in ESCAPES:
            result.append(ESCAPES[escape])
        elif escape == "x" and index + 2 <= len(body):
            result.append(chr(int(body[index : index + 2], 16)))
            index += 2
        elif escape == "u" and index < len(body) and body[index] == "{":
            end = body.find("}", index + 1)
            if end < 0:
                raise ValidationError(f"无法解析 Dart unicode escape: {body!r}")
            result.append(chr(int(body[index + 1 : end], 16)))
            index = end + 1
        elif escape == "u" and index + 4 <= len(body):
            result.append(chr(int(body[index : index + 4], 16)))
            index += 4
        else:
            result.append(escape)
    return "".join(result)

def _literal(text: str, start: int) -> tuple[str, int] | None:
    boundary = start == 0 or not (text[start - 1].isalnum() or text[start - 1] in "_$")
    raw = text[start : start + 1] == "r" and text[start + 1 : start + 2] in "'\"" and boundary
    quote_at = start + 1 if raw else start
    if quote_at >= len(text) or text[quote_at] not in "'\"": return None
    quote = text[quote_at]
    delimiter = quote * (3 if text.startswith(quote * 3, quote_at) else 1)
    body_at = quote_at + len(delimiter)
    index = body_at
    while index < len(text):
        if text.startswith(delimiter, index):
            return _unescape(text[body_at:index], raw), index + len(delimiter)
        index += 2 if not raw and text[index] == "\\" else 1
    return None

def _comment_end(text: str, start: int) -> int | None:
    if text.startswith("//", start):
        end = text.find("\n", start + 2)
        return len(text) if end < 0 else end + 1
    if text.startswith("/*", start):
        end = text.find("*/", start + 2)
        return None if end < 0 else end + 2
    return start

def _nonspace(text: str, start: int, end: int) -> int:
    while start < end and text[start].isspace():
        start += 1
    return start

def _closing(text: str, start: int) -> int | None:
    if start >= len(text) or text[start] not in BRACKETS: return None
    stack = [BRACKETS[text[start]]]
    index = start + 1
    while index < len(text):
        comment_end = _comment_end(text, index)
        if comment_end is None:
            return None
        if comment_end != index:
            index = comment_end
            continue
        if literal := _literal(text, index):
            index = literal[1]
            continue
        char = text[index]
        if char in BRACKETS:
            stack.append(BRACKETS[char])
        elif char in ")]}":
            if char != stack[-1]:
                return None
            stack.pop()
            if not stack:
                return index
        index += 1
    return None

def _map_keys(text: str, open_paren: int, close_paren: int) -> frozenset[str] | None:
    start = text.find("{", open_paren + 1, close_paren)
    if start < 0 or (end := _closing(text, start)) is None or end > close_paren:
        return None
    keys: set[str] = set()
    stack: list[str] = []
    expect_key = True
    dynamic = False
    index = start + 1
    while index < end:
        comment_end = _comment_end(text, index)
        if comment_end is None:
            return None
        if comment_end != index:
            index = comment_end
            continue
        if literal := _literal(text, index):
            value, literal_end = literal
            after = _nonspace(text, literal_end, end)
            if not stack and expect_key and after < end and text[after] == ":":
                keys.add(value)
                expect_key = False
            index = literal_end
            continue
        char = text[index]
        dynamic |= not stack and expect_key and not char.isspace() and char != ","
        if char in BRACKETS:
            stack.append(BRACKETS[char])
        elif char in ")]}":
            if stack and char == stack[-1]:
                stack.pop()
        elif not stack and char == ",":
            expect_key = True
        index += 1
    return None if dynamic else frozenset(keys)

def _calls(text: str, source: str) -> list[Call]:
    result: list[Call] = []
    index = 0
    while index < len(text):
        comment_end = _comment_end(text, index)
        if comment_end is None:
            break
        if comment_end != index:
            index = comment_end
            continue
        if not (literal := _literal(text, index)):
            index += 1
            continue
        key, literal_end = literal
        suffix = _nonspace(text, literal_end, len(text))
        match = CALL_RE.match(text, suffix)
        if not match:
            index = literal_end
            continue
        method = match.group(1).split("(", 1)[0]
        end = match.end()
        parameters = None
        if method == "multiKeyTr" and (close := _closing(text, match.end() - 1)) is not None:
            end = close + 1
            parameters = _map_keys(text, match.end() - 1, close)
        first = text.count("\n", 0, index) + 1
        result.append(Call(key, method, parameters, source, first, text.count("\n", 0, end) + 1))
        index = max(literal_end, end)
    return result

def _changed_lines(root: Path, relative: str) -> set[int]:
    diff = _git(root, "diff", "--unified=0", "--no-color", "HEAD", "--", relative) or ""
    result: set[int] = set()
    current: int | None = None
    for line in diff.splitlines():
        header = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if header:
            current = int(header.group(1))
        elif current is not None and line.startswith("+") and not line.startswith("+++"):
            result.add(current)
            current += 1
        elif current is not None and line.startswith(" "):
            current += 1
        elif current is not None and not line.startswith(("-", "\\")):
            current = None
    return result

def _paths(root: Path, *args: str) -> set[str]:
    return {path for path in (_git(root, *args) or "").split("\0") if path.endswith(".dart")}

def _collect_calls(root: Path, all_files: bool) -> dict[str, list[Call]]:
    untracked: set[str] = set()
    if all_files:
        files = _paths(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", *DART_SCOPE)
    else:
        files = _paths(root, "diff", "--name-only", "-z", "HEAD", "--", *DART_SCOPE)
        untracked = _paths(root, "ls-files", "--others", "--exclude-standard", "-z", "--", *DART_SCOPE)
        files |= untracked
    grouped: dict[str, list[Call]] = {}
    for relative in sorted(files):
        path = root / relative
        if not path.is_file():
            continue
        touched = None if all_files or relative in untracked else _changed_lines(root, relative)
        for call in _calls(path.read_text(encoding="utf-8"), relative):
            changed = touched is None or any(call.first_line <= line <= call.last_line for line in touched)
            if changed:
                grouped.setdefault(call.key, []).append(call)
    return grouped

def _placeholders(text: str) -> tuple[frozenset[str], tuple[str, ...]]:
    names: set[str] = set()
    malformed: list[str] = []
    for match in TOKEN_RE.finditer(text):
        token = match.group(1)
        if NAME_RE.fullmatch(token):
            names.add(token)
        else:
            malformed.append(match.group(0))
    remainder = TOKEN_RE.sub("", text)
    if "{" in remainder or "}" in remainder:
        malformed.append("未配对或嵌套的花括号")
    return frozenset(names), tuple(malformed)

def _load_locales(root: Path) -> tuple[dict[str, dict[str, str]], set[str]]:
    directory = (root / I18N_DIR).resolve()
    manifest_path = directory / "manifest.json"
    manifest = _read_json(manifest_path)
    locales, fallback = manifest.get("locales"), manifest.get("fallbackLocale")
    if not isinstance(locales, dict) or not locales: raise ValidationError(f"{manifest_path}: locales 必须是非空 object")
    if not isinstance(fallback, str) or fallback not in locales: raise ValidationError(f"{manifest_path}: fallbackLocale 未出现在 locales")
    result: dict[str, dict[str, str]] = {}
    changed: set[str] = set()
    for locale, filename in locales.items():
        if not isinstance(locale, str) or not isinstance(filename, str):
            raise ValidationError(f"{manifest_path}: locale 与文件名必须是字符串")
        path = (directory / filename).resolve()
        if path.parent != directory:
            raise ValidationError(f"{manifest_path}: locale 文件必须直接位于 i18n 目录: {filename}")
        current = _read_json(path)
        invalid = [key for key, value in current.items() if not key.strip() or not isinstance(value, str) or not value.strip()]
        if invalid:
            raise ValidationError(f"{path}: 存在空 key、非字符串或空值: {invalid[:10]!r}")
        result[locale] = {key: value for key, value in current.items() if isinstance(value, str)}
        previous, sentinel = _head_json(root, path.relative_to(root)), object()
        changed |= {key for key in set(previous) | set(current) if previous.get(key, sentinel) != current.get(key, sentinel)}
    return result, changed

def validate(root: Path, explicit: set[str]) -> None:
    git_root = Path((_git(root, "rev-parse", "--show-toplevel") or "").strip()).resolve()
    if git_root != root:
        raise ValidationError(f"--root 必须是 Git 根目录: 当前解析为 {git_root}")
    locales, resource_changes = _load_locales(root)
    current_keys = set().union(*(set(values) for values in locales.values()))
    all_calls = _collect_calls(root, True) if resource_changes or explicit else {}
    errors: list[str] = []
    still_used = (resource_changes - current_keys) & set(all_calls)
    if still_used:
        errors.append(f"已从全部 locale 删除但 Dart 仍调用的 key: {sorted(still_used)!r}")

    changed_calls = _collect_calls(root, False)
    resource_keys = resource_changes & current_keys
    target_keys = resource_keys | set(changed_calls) | explicit
    for key in sorted(target_keys):
        missing = [locale for locale, values in locales.items() if key not in values]
        if missing:
            errors.append(f"{key!r}: 缺少 locale {', '.join(missing)}")
            continue
        sets: dict[str, frozenset[str]] = {}
        for locale, values in locales.items():
            names, malformed = _placeholders(values[key])
            sets[locale] = names
            if malformed:
                errors.append(f"{key!r}: {locale} 含畸形占位符 {list(malformed)!r}；仅允许 {{identifier}}")
        if len(set(sets.values())) != 1:
            detail = ", ".join(f"{locale}={sorted(names)}" for locale, names in sets.items())
            errors.append(f"{key!r}: 占位符不一致: {detail}")
        expected = next(iter(sets.values()))
        calls = all_calls.get(key, []) if key in resource_keys or key in explicit else changed_calls.get(key, [])
        for call in calls:
            location = f"{call.source}:{call.first_line}"
            if call.method == "tr" and expected:
                errors.append(f"{location}: {key!r} 的 tr 不会替换占位符 {sorted(expected)}，应使用 keyTr/multiKeyTr")
            elif call.method == "keyTr" and expected != frozenset({"key"}):
                errors.append(f"{location}: {key!r} 的 keyTr 要求每个 locale 恰好包含 {{key}}")
            elif call.method == "multiKeyTr":
                if call.parameters is None:
                    errors.append(f"{location}: {key!r} 无法解析 multiKeyTr 的内联 Map 参数")
                elif call.parameters != expected:
                    errors.append(
                        f"{location}: {key!r} 的 multiKeyTr 参数 {sorted(call.parameters)} "
                        f"与翻译占位符 {sorted(expected)} 不一致"
                    )
    if errors:
        raise ValidationError("\n".join(errors))
    print(
        f"PASS: {len(locales)} 个 locale 的 JSON/重复 key/非空值有效；"
        f"{len(target_keys)} 个变更或显式 key 已完成全 locale 与占位符校验。"
    )
    print("NOTE: 可见硬编码、语义翻译质量、RTL 与布局仍需 diff 审查和 Widget/真机验证。")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Tuqiang Git 根目录")
    parser.add_argument("--key", action="append", default=[], help="额外校验 source key；可重复")
    args = parser.parse_args()
    try:
        validate(args.root.resolve(), set(args.key))
    except (OSError, UnicodeError, ValueError, ValidationError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
