import os

PAGE_URL = os.getenv("APP_WEB_URL", "http://localhost:3001")


def signup_email(name: str, token: str) -> str:
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #2c3e50;">Welcome to <span style="color: #4CAF50;">RoadFlow</span>, {name}!</h1>
                <p style="font-size: 16px; color: #555;">Thank you for signing up. Please click the link below to verify your email address:</p>
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{PAGE_URL}/verify?token={token}"
                       style="background-color: #4CAF50; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Verify Email
                    </a>
                </p>
                <p style="font-size: 14px; color: #888;">If you did not sign up for this account, please ignore this email.</p>
            </div>
        </body>
    </html>
    """
