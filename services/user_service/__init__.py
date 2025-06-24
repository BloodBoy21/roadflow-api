import bcrypt
from loguru import logger

from helpers.auth import create_validation_token
from models.inputs.api import UserLogin
from models.organization import OrganizationCreate, OrganizationRead
from models.user import UserCreate, UserRead
from repository import repository
from services.email import send_email
from templates.email.signup import signup_email


async def exists_user(email: str) -> bool:
    """Check if a user exists by email."""
    return await repository.sql.user.exists(email=email)


async def create_user(user: UserCreate) -> UserRead:
    """Create and return the user service."""
    if await exists_user(email=user.email):
        raise ValueError(f"User with email {user.email} already exists.")

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    user_created: UserRead = await repository.sql.user.create(
        data={**user.model_dump(), "password": hashed_password}
    )

    organization = await create_user_org_default(
        user_created.first_name, user_created.id
    )
    await add_user_to_org(user_id=user_created.id, org_id=organization.id)
    logger.info(user_created)
    return user_created


async def create_user_org_default(user_name: str, user_id: int) -> OrganizationRead:
    """Create a default organization for the user."""
    organization = OrganizationCreate(
        name=f"{user_name}'s Organization", ownerId=user_id
    )
    return await repository.sql.organization.create(data=organization.model_dump())


async def add_user_to_org(user_id: int, org_id: int) -> OrganizationRead:
    """Add user to organization."""
    return await repository.sql.organization_user.add_user(
        user_id=user_id, organization_id=org_id
    )


async def login_user(user: UserLogin) -> UserRead:
    """Login user and return user details."""
    user_db: UserRead = await repository.sql.user.get_by_email(email=user.email)
    if not user_db:
        raise ValueError("User not found.")

    if not bcrypt.checkpw(
        user.password.encode("utf-8"),
        user_db.password.get_secret_value().encode("utf-8"),
    ):
        raise ValueError("Invalid password.")

    return user_db


def send_validation_email(user: UserRead) -> None:
    """Send validation email to user."""
    if user.verified:
        raise ValueError("Email already verified.")
    validation_token = create_validation_token(user.id)
    send_email(
        html=signup_email(name=user.first_name, token=validation_token),
        subject="Welcome to RoadFlow",
        to=user.email,
    )


async def verify_user_email(user_id: str) -> UserRead:
    """Verify user's email."""
    user: UserRead = await repository.sql.user.find_by_id(id=user_id)
    if not user:
        raise ValueError("User not found.")

    if user.verified:
        raise ValueError("Email already verified.")

    return await repository.sql.user.update_by_id(id=user_id, data={"verified": True})
