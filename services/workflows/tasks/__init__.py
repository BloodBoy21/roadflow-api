from loguru import logger
from typing import Dict, Optional
import importlib
from pydantic import BaseModel


def run_task(
    task_name: str,
    payload: Dict,
    context: Dict = {},
    source: str = "",
    source_log_id: Optional[str] = None,
):
    """
    Run a specific task by its name.
    """
    module = importlib.import_module(f"services.workflows.tasks.{task_name}")
    if not hasattr(module, "run"):
        logger.error(f"Task {task_name} does not have a run function.")
        return
    run_function = getattr(module, "run")
    if not callable(run_function):
        logger.error(f"Task {task_name} run is not callable.")
        return
    try:
        logger.info(f"Running task: {task_name} with payload: {payload}")
        res = run_function(
            payload=payload,
            context=context,
            source=source,
            source_log_id=source_log_id,
        )
        if isinstance(res, BaseModel):
            return res.model_dump()
        return res
    except Exception as e:
        logger.error(f"Error running task {task_name}: {e}")
        raise e
