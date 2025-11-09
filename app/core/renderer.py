from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

TemplateCache = Dict[str, Template]
EnvironmentCache = Dict[Tuple[str, ...], Environment]

_TEMPLATE_CACHE: TemplateCache = {}
_ENVIRONMENT_CACHE: EnvironmentCache = {}


def _build_search_paths(template_path: Path) -> Tuple[str, ...]:
    """Assemble loader search paths to support shared prompt folders."""
    workflow_dir = template_path.parent
    collection_dir = workflow_dir.parent
    prompts_dir = collection_dir.parent

    candidates = [
        workflow_dir,
        workflow_dir / "shared",
        collection_dir,
        collection_dir / "shared",
        prompts_dir,
        prompts_dir / "shared",
    ]

    unique_paths: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        candidate_str = str(candidate)
        if candidate_str not in seen:
            unique_paths.append(candidate_str)
            seen.add(candidate_str)
    return tuple(unique_paths)


def _get_environment(search_paths: Tuple[str, ...]) -> Environment:
    """Return a cached Environment keyed by loader search paths."""
    env = _ENVIRONMENT_CACHE.get(search_paths)
    if env is None:
        env = Environment(loader=FileSystemLoader(list(search_paths)))
        _ENVIRONMENT_CACHE[search_paths] = env
    return env


def _get_template(template_path: Path, template_name: str) -> Template:
    """Resolve (and cache) a compiled template for the given file."""
    cache_key = str(template_path)
    template = _TEMPLATE_CACHE.get(cache_key)
    if template is None:
        search_paths = _build_search_paths(template_path)
        env = _get_environment(search_paths)
        try:
            template = env.get_template(template_name)
        except TemplateNotFound as exc:
            raise HTTPException(
                status_code=404,
                detail=f"Prompt file '{template_name}' not found under {template_path.parent}",
            ) from exc
        _TEMPLATE_CACHE[cache_key] = template
    return template


def render_file_path(template_dir: Path, filename: str, variables: dict):
    file_path = template_dir / filename
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Prompt file '{filename}' not found under {template_dir}",
        )

    template = _get_template(file_path, filename)
    try:
        return template.render(**variables)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to render prompt '{filename}': {exc}",
        ) from exc
