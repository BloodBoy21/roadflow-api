from typing import Dict, Optional
from services.email import send_email
from models.response.task import TaskResponse
from loguru import logger


def run(
    payload: Dict,
    context: Dict = {},
    source: str = "",
    source_log_id: Optional[str] = None,
    **kwargs,
):
    try:
        emails: str = payload.get("to", "")
        if not emails:
            return TaskResponse(
                success=False,
                message="No email addresses provided in payload",
                payload={},
            )
        if not context.get("last_response"):
            return TaskResponse(
                success=False,
                message="No last response found in context",
                payload={},
            )
        emails = emails.split(",") if isinstance(emails, str) else emails
        logger.info(f"Preparing to send email to: {emails}")
        for email in emails:
            if not email:
                continue
            # Here you would implement the actual email sending logic.
            # For example, using an email sending service or library.
            logger.info(f"Sending email to: {email}")
            result = send_email(
                to=email,
                subject=payload.get("subject", ""),
                text=context.get("last_response", ""),
            )
            logger.info(f"Emails sent successfully to: {email}: {result}")
        return TaskResponse(
            success=True,
            message="Email sent successfully",
            payload={"emails": emails},
        )
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return TaskResponse(
            success=False,
            message=f"Error sending email: {str(e)}",
            payload={},
        )
