import os

import resend

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


def send_email(
    to: str = None,
    subject: str = "",
    html: str = "",
    from_email: str = DEFAULT_FROM_EMAIL,
    text: str = "",
) -> dict:
    """
    Send an email using the Resend API.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        html (str): The HTML content of the email.

    Returns:
        dict: The response from the Resend API.
    """
    if not to:
        raise ValueError("Recipient email address is required.")
    return resend.Emails.send(
        {"from": from_email, "to": to, "subject": subject, "html": html, "text": text}
    )
