"""Portable deterministic task-to-skill router; no hook integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CLASSIFIER_VERSION = "1"
MAX_CONFIGURED_SKILL_BYTES = 8 * 1024 * 1024

# These source patterns are fixed, bounded, and contain no nested or
# unbounded repetition. User-controlled configuration cannot supply regexes.
RULES: dict[str, tuple[re.Pattern[str], ...]] = {
    "implementation": tuple(
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bimplement\b",
            r"\b(add|build|create|write|introduce)\b.{0,48}\b(feature|function|class|module|endpoint|component|code|support)\b",
            r"\b(change|modify|update|refactor|edit)\b.{0,48}\b(code|file|function|class|module|component|behavior)\b",
            r"\bfix\b.{0,48}\b(implement|code|file|function|class|module|component)\b",
        )
    ),
    "debugging": tuple(
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\b(debug|debugging|troubleshoot|diagnose|investigate)\b",
            r"\b(failing|broken|crash(?:es|ed|ing)?|error|exception|regression|bug)\b",
            r"\b(why|what causes?)\b.{0,50}\b(fail|failing|broken|crash|error|exception|bug)\b",
        )
    ),
    "review": tuple(
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\b(review|code review|audit|inspect)\b",
            r"\b(find|identify|look for)\b.{0,40}\b(bug|issue|risk|regression|security flaw)s?\b",
        )
    ),
    "planning": tuple(
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\b(plan|planning|roadmap|proposal|design)\b",
            r"\boutline\b.{0,40}\b(steps|approach|work|implementation)\b",
            r"\bhow should we\b.{0,40}\b(approach|plan|design)\b",
        )
    ),
}
TASK_CLASSES = {"implementation", "debugging", "review", "planning", "unrelated"}


class RoutingError(Exception):
    """Expected invalid input, metadata, or skill-file failure."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _error(code: str, message: str, skill_id: str | None = None) -> dict[str, str]:
    item = {"code": code, "message": message}
    if skill_id is not None:
        item["skill_id"] = skill_id
    return item


def classify_task(task: str) -> dict[str, Any]:
    """Apply fixed phrase rules; any multi-class match is deliberately ambiguous."""
    if not isinstance(task, str):
        raise TypeError("task must be a string")
    if not task.strip():
        return {"class": "ambiguous", "matched_classes": [], "reason": "empty_task"}
    hits = [
        name
        for name, patterns in RULES.items()
        if any(pattern.search(task) for pattern in patterns)
    ]
    if len(hits) > 1:
        return {"class": "ambiguous", "matched_classes": hits, "reason": "multiple_classes_matched"}
    if not hits:
        return {"class": "unrelated", "matched_classes": [], "reason": "no_supported_rule_matched"}
    return {"class": hits[0], "matched_classes": hits, "reason": "single_class_matched"}


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def _safe_relative_path(value: str, field: str) -> Path:
    if not value or "\\" in value or ":" in value:
        raise RoutingError("invalid_metadata", f"{field} must use a portable relative path")
    path = Path(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise RoutingError("invalid_metadata", f"{field} must be a normalized relative path")
    return path


def _load_catalog(catalog_path: Path) -> dict[str, Any]:
    try:
        raw = catalog_path.read_text(encoding="utf-8")
        catalog = json.loads(
            raw,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise RoutingError("invalid_catalog", f"Cannot read valid routing JSON: {exc}") from exc

    expected_fields = {"schema_version", "task_classes", "skill_roots", "max_skill_bytes", "skills", "routes"}
    if not isinstance(catalog, dict) or set(catalog) != expected_fields:
        raise RoutingError("invalid_metadata", "Catalog must contain exactly the documented fields")
    if type(catalog["schema_version"]) is not int or catalog["schema_version"] != 1:
        raise RoutingError("invalid_metadata", "schema_version must be integer 1")
    max_bytes = catalog["max_skill_bytes"]
    if type(max_bytes) is not int or not 1 <= max_bytes <= MAX_CONFIGURED_SKILL_BYTES:
        raise RoutingError("invalid_metadata", f"max_skill_bytes must be between 1 and {MAX_CONFIGURED_SKILL_BYTES}")

    classes = catalog["task_classes"]
    if not isinstance(classes, list) or not all(isinstance(item, str) for item in classes):
        raise RoutingError("invalid_metadata", "task_classes must be a list of strings")
    if set(classes) != TASK_CLASSES or len(classes) != len(TASK_CLASSES):
        raise RoutingError("invalid_metadata", "task_classes must define the five supported classes exactly")

    roots = catalog["skill_roots"]
    if not isinstance(roots, list) or not roots or not all(isinstance(item, str) for item in roots):
        raise RoutingError("invalid_metadata", "skill_roots must be a non-empty list of relative paths")
    root_paths = [_safe_relative_path(item, "skill root") for item in roots]
    if len(set(root_paths)) != len(root_paths):
        raise RoutingError("invalid_metadata", "skill_roots must not contain duplicates")

    skills, routes = catalog["skills"], catalog["routes"]
    if not isinstance(skills, dict) or not isinstance(routes, dict) or set(routes) != TASK_CLASSES:
        raise RoutingError("invalid_metadata", "skills and complete routes objects are required")
    for skill_id, spec in skills.items():
        if not isinstance(skill_id, str) or not skill_id or not isinstance(spec, dict):
            raise RoutingError("invalid_metadata", "Each skill must have a non-empty id and object metadata")
        if set(spec) != {"path", "required", "task_classes"}:
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} has unexpected or missing metadata fields")
        if not isinstance(spec["path"], str):
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} path must be a string")
        skill_path = _safe_relative_path(spec["path"], f"skill {skill_id!r} path")
        if skill_path.name != "SKILL.md":
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} path must identify SKILL.md")
        if not any(skill_path.is_relative_to(root_path) and skill_path != root_path for root_path in root_paths):
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} is outside every approved skill root")
        if not isinstance(spec["required"], bool):
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} required must be boolean")
        mapped = spec["task_classes"]
        if not isinstance(mapped, list) or not all(isinstance(item, str) and item in TASK_CLASSES - {"unrelated"} for item in mapped):
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} task_classes is invalid")
        if len(set(mapped)) != len(mapped):
            raise RoutingError("invalid_metadata", f"Skill {skill_id!r} task_classes contains duplicates")

    for task_class, skill_ids in routes.items():
        if not isinstance(skill_ids, list) or not all(isinstance(item, str) and item in skills for item in skill_ids):
            raise RoutingError("invalid_metadata", f"Route {task_class!r} must list known skill ids")
        if len(set(skill_ids)) != len(skill_ids):
            raise RoutingError("invalid_metadata", f"Route {task_class!r} contains duplicate skills")
        if task_class == "unrelated" and skill_ids:
            raise RoutingError("invalid_metadata", "Unrelated tasks must not route to skills")
        for skill_id in skill_ids:
            if task_class not in skills[skill_id]["task_classes"]:
                raise RoutingError("invalid_metadata", f"Route {task_class!r} disagrees with skill {skill_id!r} metadata")
    for task_class in TASK_CLASSES - {"unrelated"}:
        if not routes[task_class] or not any(skills[item]["required"] for item in routes[task_class]):
            raise RoutingError("invalid_metadata", f"Task class {task_class!r} needs a required skill route")
    return catalog


def _reject_symlink_components(base: Path, relative: Path) -> None:
    current = base
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise RoutingError("invalid_skill_path", "Symlinks are not allowed in skill roots or skill paths")


def _resolve_approved_roots(package_root: Path, catalog: dict[str, Any]) -> tuple[Path, list[Path]]:
    try:
        root = package_root.resolve(strict=True)
    except OSError as exc:
        raise RoutingError("invalid_package_root", f"Package root is unavailable: {exc}") from exc
    approved: list[Path] = []
    for root_text in catalog["skill_roots"]:
        relative = _safe_relative_path(root_text, "skill root")
        _reject_symlink_components(root, relative)
        try:
            resolved = (root / relative).resolve(strict=True)
        except OSError as exc:
            raise RoutingError("invalid_skill_path", f"Approved skill root {root_text!r} is unavailable") from exc
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise RoutingError("invalid_skill_path", f"Approved skill root {root_text!r} escapes package root") from exc
        if not resolved.is_dir():
            raise RoutingError("invalid_skill_path", f"Approved skill root {root_text!r} is not a directory")
        approved.append(resolved)
    return root, approved


def _read_skill(
    package_root: Path,
    approved_roots: list[Path],
    spec: dict[str, Any],
    max_bytes: int,
) -> tuple[str, str]:
    relative = _safe_relative_path(spec["path"], "skill path")
    _reject_symlink_components(package_root, relative)
    candidate = package_root / relative
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise RoutingError("missing_skill", f"Required skill file is unavailable: {exc}") from exc
    root = next((item for item in approved_roots if resolved.is_relative_to(item)), None)
    if root is None:
        raise RoutingError("invalid_skill_path", "Skill file resolves outside approved skill roots")
    if not resolved.is_file():
        raise RoutingError("invalid_skill_file", "Skill path is not a regular file")
    try:
        with resolved.open("rb") as stream:
            raw = stream.read(max_bytes + 1)
    except OSError as exc:
        raise RoutingError("unreadable_skill", f"Skill file cannot be read: {exc}") from exc
    if len(raw) > max_bytes:
        raise RoutingError("oversized_skill", f"Skill file exceeds configured limit of {max_bytes} bytes")
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RoutingError("invalid_skill_encoding", "Skill file is not valid UTF-8") from exc
    if not content.strip():
        raise RoutingError("invalid_skill_file", "Skill file is empty")
    return content, hashlib.sha256(raw).hexdigest()


def _new_result(classification: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "classifier_version": CLASSIFIER_VERSION,
        "classification": classification or {"class": "ambiguous", "matched_classes": [], "reason": "invalid_input"},
        "selected_skills": [],
        "loading_results": [],
        "instructions": {},
        "errors": [],
        "decision": "BLOCK",
    }


def route_task(
    task: str,
    package_root: str | Path,
    catalog_path: str | Path | None = None,
    audit_path: str | Path | None = None,
) -> dict[str, Any]:
    """Classify and load instruction text; required routing failures BLOCK."""
    result = _new_result()
    try:
        if not isinstance(task, str):
            raise RoutingError("invalid_task", "Task description must be a string")
        classification = classify_task(task)
        result["classification"] = classification
        if classification["class"] == "ambiguous":
            result["errors"].append(_error("ambiguous_task", "Task matched multiple classes or was empty; routing is blocked"))
            return _finish(result, audit_path)

        root = Path(package_root)
        catalog_file = Path(catalog_path) if catalog_path is not None else root / "routing.json"
        catalog = _load_catalog(catalog_file)
        task_class = classification["class"]
        selected = catalog["routes"][task_class]
        result["selected_skills"] = list(selected)

        if task_class == "unrelated":
            result["decision"] = "UNRELATED"
            return _finish(result, audit_path)

        root, approved_roots = _resolve_approved_roots(root, catalog)

        failed_required = False
        for skill_id in selected:
            spec = catalog["skills"][skill_id]
            try:
                content, digest = _read_skill(root, approved_roots, spec, catalog["max_skill_bytes"])
                result["instructions"][skill_id] = content
                result["loading_results"].append({"skill_id": skill_id, "status": "loaded", "sha256": digest})
            except RoutingError as exc:
                result["loading_results"].append({"skill_id": skill_id, "status": "failed", "error": exc.code})
                result["errors"].append(_error(exc.code, str(exc), skill_id))
                failed_required = failed_required or spec["required"]
            except Exception as exc:
                result["loading_results"].append({"skill_id": skill_id, "status": "failed", "error": "internal_error"})
                result["errors"].append(_error("internal_error", f"Unexpected skill loading error: {type(exc).__name__}", skill_id))
                failed_required = failed_required or spec["required"]
        if failed_required:
            result["instructions"].clear()
            result["decision"] = "BLOCK"
        else:
            result["decision"] = "ALLOW"
    except RoutingError as exc:
        result["errors"].append(_error(exc.code, str(exc)))
        result["decision"] = "BLOCK"
    except Exception as exc:
        result["errors"].append(_error("internal_error", f"Unexpected routing error: {type(exc).__name__}"))
        result["decision"] = "BLOCK"
    return _finish(result, audit_path)


def _finish(result: dict[str, Any], audit_path: str | Path | None) -> dict[str, Any]:
    """Append one audit record; detect short writes and attempt safe rollback."""
    if audit_path is None:
        return result
    fd: int | None = None
    start_size: int | None = None
    try:
        record = {key: value for key, value in result.items() if key != "instructions"}
        data = (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        path = Path(audit_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        start_size = os.fstat(fd).st_size
        written = os.write(fd, data)
        if written != len(data):
            current_size = os.fstat(fd).st_size
            rollback = current_size == start_size + written
            if rollback:
                os.ftruncate(fd, start_size)
            suffix = " Partial record was rolled back." if rollback else " Partial record could not be safely rolled back."
            raise OSError(f"short audit write ({written}/{len(data)} bytes).{suffix}")
    except Exception as exc:
        result["errors"].append(_error("audit_write_failed", f"Cannot write complete audit record: {type(exc).__name__}: {exc}"))
        result["decision"] = "BLOCK"
        result["audit_write_failed"] = True
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                result["errors"].append(_error("audit_close_failed", "Could not close audit file"))
                result["decision"] = "BLOCK"
                result["audit_write_failed"] = True
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="Task description to classify and route")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent), help="Package root containing routing.json and skills/")
    parser.add_argument("--audit", help="Optional JSONL audit output path")
    args = parser.parse_args(argv)
    result = route_task(args.task, args.root, audit_path=args.audit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["decision"] == "BLOCK":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
