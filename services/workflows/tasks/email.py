
from loguru import logger

from models.response.task import TaskResponse
from services.email import send_email


def run(
    payload: dict,
    context: dict = None,
    source: str = "",
    source_log_id: str | None = None,
    **kwargs,
):
    if context is None:
        context = {}
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
        agent_response: dict = context.get("last_response", {})
        task_data: dict = agent_response.get("next_task", {})
        logger.info(f"Agent response: {agent_response}")
        logger.info(f"Task data: {task_data}")
        for email in emails:
            if not email:
                continue
            # Here you would implement the actual email sending logic.
            # For example, using an email sending service or library.
            logger.info(f"Sending email to: {email}")
            result = send_email(
                to=email,
                subject=payload.get("subject")
                or task_data.get("subject", "No Subject"),
                text=agent_response.get("result", ""),
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
