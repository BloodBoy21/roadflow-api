from repository import repository


async def get_user_organizations(user_id: int):
    """Get all organizations for a user."""
    return await repository.sql.organization_user.get_organizations_by_user_id(
        user_id=user_id
    )
