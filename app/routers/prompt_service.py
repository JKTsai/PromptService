import json

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.core.config_reader import get_workflow_env_config, load_yaml_config
from app.core.loader import get_workflow_base
from app.core.renderer import render_file_path

router = APIRouter()


def parse_variables(raw_vars: str):
    try:
        return json.loads(raw_vars)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON in variables")


@router.get("/collection/{workflow_id}")
def get_prompts_default_env(workflow_id: str, variables: str = Query(...)):
    default_env = "dev"

    cfg = load_yaml_config(workflow_id)
    env_cfg = get_workflow_env_config(cfg, default_env)
    variables_dict = parse_variables(variables)

    workflow_path = get_workflow_base(workflow_id)

    response_data = {
        key: render_file_path(workflow_path, item["file_path"], variables_dict)
        for key, item in env_cfg.items()
    }

    return JSONResponse(response_data)


@router.get("/collection/{workflow_id}/env/{env}")
def get_prompts_with_env(workflow_id: str, env: str, variables: str = Query(...)):
    cfg = load_yaml_config(workflow_id)
    env_cfg = get_workflow_env_config(cfg, env)
    variables_dict = parse_variables(variables)

    workflow_path = get_workflow_base(workflow_id)
    response_data = {
        key: render_file_path(workflow_path, item["file_path"], variables_dict)
        for key, item in env_cfg.items()
    }

    return JSONResponse(response_data)
