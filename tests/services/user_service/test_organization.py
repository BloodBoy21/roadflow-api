from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.user_service.organization import get_user_organizations


class TestUserOrganizationService:
    """Test cases for user organization service functions."""

    @patch('services.user_service.organization.repository')
    async def test_get_user_organizations_success(self, mock_repository):
        """Test successful retrieval of user organizations."""
        # Arrange
        expected_organizations = [
            Mock(id=1, name="Org 1"),
            Mock(id=2, name="Org 2"),
            Mock(id=3, name="Org 3")
        ]
        mock_repository.sql.organization_user.get_organizations_by_user_id = AsyncMock(
            return_value=expected_organizations
        )

        # Act
        result = await get_user_organizations(user_id=123)

        # Assert
        mock_repository.sql.organization_user.get_organizations_by_user_id.assert_called_once_with(
            user_id=123
        )
        assert result == expected_organizations

    @patch('services.user_service.organization.repository')
    async def test_get_user_organizations_empty_result(self, mock_repository):
        """Test retrieval of user organizations with empty result."""
        # Arrange
        mock_repository.sql.organization_user.get_organizations_by_user_id = AsyncMock(
            return_value=[]
        )

        # Act
        result = await get_user_organizations(user_id=456)

        # Assert
        mock_repository.sql.organization_user.get_organizations_by_user_id.assert_called_once_with(
            user_id=456
        )
        assert result == []

    @patch('services.user_service.organization.repository')
    async def test_get_user_organizations_exception(self, mock_repository):
        """Test retrieval of user organizations with exception."""
        # Arrange
        mock_repository.sql.organization_user.get_organizations_by_user_id = AsyncMock(
            side_effect=Exception("Database connection error")
        )

        # Act & Assert
        with pytest.raises(Exception, match="Database connection error"):
            await get_user_organizations(user_id=789)

    @patch('services.user_service.organization.repository')
    async def test_get_user_organizations_with_none_user_id(self, mock_repository):
        """Test retrieval of user organizations with None user_id."""
        # Arrange
        mock_repository.sql.organization_user.get_organizations_by_user_id = AsyncMock(
            return_value=[]
        )

        # Act
        result = await get_user_organizations(user_id=None)

        # Assert
        mock_repository.sql.organization_user.get_organizations_by_user_id.assert_called_once_with(
            user_id=None
        )
        assert result == []

    @patch('services.user_service.organization.repository')
    async def test_get_user_organizations_with_zero_user_id(self, mock_repository):
        """Test retrieval of user organizations with zero user_id."""
        # Arrange
        mock_repository.sql.organization_user.get_organizations_by_user_id = AsyncMock(
            return_value=[]
        )

        # Act
        result = await get_user_organizations(user_id=0)

        # Assert
        mock_repository.sql.organization_user.get_organizations_by_user_id.assert_called_once_with(
            user_id=0
        )
        assert result == []
