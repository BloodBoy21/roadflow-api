from repository import repository
from models.user import UserCreate, UserRead
from models.organization import OrganizationRead, OrganizationCreate
import bcrypt


async def exits_user(email: str) -> bool:
    """Check if a user exists by email."""
    return await repository.sql.user.exists(email=email)


async def create_user(user: UserCreate) -> UserRead:
    """Create and return the user service."""
    if await exits_user(email=user.email):
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
        user_id=user_id, org_id=org_id
    )


async def login_user(user: UserCreate) -> UserRead:
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
