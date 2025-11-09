from pathlib import Path

from fastapi import HTTPException

BASE_DIR = Path(__file__).resolve().parents[2]
PROMPT_ROOT = BASE_DIR / "prompts" / "collection"


def get_workflow_base(workflow_id: str) -> Path:
    """Return prompts/collection/{workflow_id} folder."""
    workflow_path = PROMPT_ROOT / workflow_id
    if not workflow_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Workflow '{workflow_id}' not found under prompts/collection/",
        )
    return workflow_path


def get_env_path(workflow_id: str, env: str) -> Path:
    """Return prompts/collection/{workflow_id}/{env} folder."""
    env_path = PROMPT_ROOT / workflow_id / env
    if not env_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Env folder '{env}' not found under workflow '{workflow_id}'",
        )
    return env_path
