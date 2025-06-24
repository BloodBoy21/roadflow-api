import os

import jwt
from loguru import logger

from models.invitation import InvitationBase, InvitationCreate, InvitationRead, RoleEnum
from models.organization import OrganizationRead
from models.organization_user import (
    OrganizationUserCreate,
    OrganizationUserRead,
)
from repository import repository
from services.email import send_email
from templates.email.join_org import join_to_org_email
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


TZ = os.getenv("TZ", "America/Mexico_City")
tz_zone = ZoneInfo(TZ)

INVITE_SECRET = os.getenv("INVITE_SECRET")


async def send_invite_to_org(
    org_id: int, users: list[InvitationCreate]
) -> OrganizationUserRead:
    """Invite users to an organization."""
    org: OrganizationRead = await repository.sql.organization.find_by_id(org_id)
    if not org:
        raise ValueError(f"Organization with ID {org_id} does not exist.")
    for user in users:
        # Create an invitation in the database
        has_existing_invitation = await repository.sql.invitation.get_by_email_and_org(
            email=user.email, organization_id=org_id
        )
        if has_existing_invitation:
            logger.warning(
                f"Invitation for {user.email} already exists in organization {org_id}. Skipping."
            )
            continue
        invitation = await repository.sql.invitation.create(
            InvitationBase(
                email=user.email,
                organizationId=org_id,
                role=user.role
                or RoleEnum.MEMBER,  # Default to MEMBER if no role is provided
            )
        )

        # Create a JWT token for the invitation
        token = create_invite_token(invitation)

        # Send the invitation email
        send_email(
            html=join_to_org_email(
                organization_name=org.name.capitalize(),
                token=token,
            ),
            subject="Invitation to join RoadFlow Organization",
            to=user.email,
        )


def create_invite_token(invitation: InvitationRead) -> str:
    """Create a JWT token for inviting a user to an organization."""
    payload = {
        "invitation_id": invitation.id,
        "exp": datetime.now(tz=tz_zone) + timedelta(days=7),  # Token valid for 7 days
    }
    token = jwt.encode(payload, INVITE_SECRET, algorithm="HS256")
    return token


async def validate_invite_token(token: str) -> InvitationRead:
    """Validate the JWT token and return the invitation."""
    try:
        payload: dict = jwt.decode(token, INVITE_SECRET, algorithms=["HS256"])
        if not isinstance(payload, dict):
            raise ValueError("Invalid token: Payload is not a dictionary.")
        invitation_id = payload.get("invitation_id")
        if not invitation_id:
            raise ValueError("Invalid token: 'invitation_id' not found in payload.")

        invitation = await repository.sql.invitation.find_by_id(invitation_id)
        if not invitation:
            raise ValueError(f"Invitation with ID {invitation_id} does not exist.")

        return invitation
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")


async def accept_invite(token: str, user_id: int) -> OrganizationUserRead:
    """Accept an invitation to join an organization."""
    invitation: InvitationRead = await validate_invite_token(token)

    # Check if the user is already a member of the organization
    existing_member: bool = await repository.sql.organization_user.user_in_organization(
        user_id=user_id, organization_id=invitation.organizationId
    )
    if existing_member:
        raise ValueError("User is already a member of this organization.")

    # Create the organization user record
    org_user = await repository.sql.organization_user.create(
        OrganizationUserCreate(
            user_id=user_id,
            organization_id=invitation.organizationId,
            role=invitation.role,
        )
    )

    # Optionally delete the invitation after accepting it
    await repository.sql.invitation.delete({"id": invitation.id})

    return org_user


async def resend_invite_to_org(invitation_id: int) -> InvitationRead:
    """Resend an invitation to a user."""
    invitation: InvitationRead = await repository.sql.invitation.find_by_id(
        invitation_id,
        options={"include": {"organization": True}},
    )
    if not invitation:
        raise ValueError(f"Invitation with ID {invitation_id} does not exist.")

    # Create a JWT token for the invitation
    token = create_invite_token(invitation)
    await repository.sql.invitation.update(
        {"id": invitation.id},
        {"expiresAt": datetime.now(tz=tz_zone) + timedelta(days=7)},
    )
    # Send the invitation email again
    send_email(
        html=join_to_org_email(
            organization_name=invitation.organization.name.capitalize(),
            token=token,
        ),
        subject="Invitation to join RoadFlow Organization",
        to=invitation.email,
    )

    return invitation