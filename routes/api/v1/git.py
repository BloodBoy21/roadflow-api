from fastapi import APIRouter, Depends, HTTPException, Request
from repository import repository
from loguru import logger

git_router = APIRouter()


@git_router.post("/{webhook_id}", status_code=200)
async def handle_git_webhook(webhook_id: str, request: Request):
    try:
        # Process the webhook data
        data = await request.json()
        # Here you would typically process the data, e.g., update a database, trigger a build, etc.
        # For now, we just log it
        logger.info(f"Received webhook for {webhook_id}: {data}")
        webhook = await repository.sql.input_webhook.get_by_key(webhook_id)
        if not webhook:
            logger.error(f"Webhook with ID {webhook_id} not found.")
            raise HTTPException(status_code=404, detail="Webhook not found.")
        logger.info(f"Webhook {webhook_id} found: {webhook}")
    except Exception as e:
        logger.error(f"Error processing webhook {webhook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e
