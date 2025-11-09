from pathlib import Path

import yaml
from fastapi import HTTPException

PROMPT_ROOT = Path(__file__).resolve().parents[2] / "prompts" / "collection"


def load_yaml_config(workflow_id: str):
    config_path = PROMPT_ROOT / workflow_id / "config.yml"

    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config.yml not found for workflow '{workflow_id}'"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_workflow_env_config(cfg: dict, env: str):
    if env not in cfg:
        raise HTTPException(
            status_code=404, detail=f"env '{env}' not found in config.yml"
        )
    return cfg[env]
