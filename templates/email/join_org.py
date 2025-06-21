import os

PAGE_URL = os.getenv("APP_WEB_URL", "http://localhost:3001")


def join_to_org_email(organization_name: str, token: str) -> str:
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #2c3e50;">Join {organization_name} on RoadFlow</h1>
                <p style="font-size: 16px; color: #555;">You have been invited to join the organization. Please click the link below to accept the invitation:</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{PAGE_URL}/join?token={token}"
                       style="background-color: #4CAF50; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Join Organization
                    </a>
                </p>
                <p style="font-size: 14px; color: #888;">If you did not expect this invitation, please ignore this email.</p>
            </div>
        </body>
    </html>
    """
