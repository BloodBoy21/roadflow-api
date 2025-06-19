from fastapi import HTTPException, status

from middleware import Middleware
from repository import repository


async def _validate_workflow_middleware_(
    org_id: int | None = None,
    workflow_id: str | None = None,
    node_id: str | None = None,
    head_node: str | None = None,
    **kwargs,
):
    """
    Middleware for validating workflow access.
    """
    node_id = node_id or workflow_id or head_node
    if not node_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Node ID, workflow ID, or head node ID must be provided.",
        )
    node = repository.mongo.workflow.find_by_id(id=node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found",
        )
    if node.organizationId != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this node.",
        )
    return


validate_workflow_middleware = Middleware(_validate_workflow_middleware_)
