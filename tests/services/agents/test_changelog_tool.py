from unittest.mock import Mock, patch

from services.agents.tools.changelog import (
    delete_changelog,
    get_changelog,
    save_changelog,
    sort_changelog,
    update_changelog,
)


class TestChangelogTool:
    """Test cases for changelog tool functions."""

    @patch('services.agents.tools.changelog.repository')
    def test_save_changelog_success(self, mock_repository, sample_context, sample_changelog_data):
        """Test successful changelog save."""
        # Arrange
        mock_doc = Mock()
        mock_doc.id = "test_id_123"
        mock_repository.mongo.changelog.create.return_value = mock_doc

        # Act
        save_changelog_func = save_changelog(sample_context)
        result = save_changelog_func(**sample_changelog_data)

        # Assert
        mock_repository.mongo.changelog.create.assert_called_once()
        created_entry = mock_repository.mongo.changelog.create.call_args[0][0]
        assert created_entry["organizationId"] == sample_context["org_id"]
        assert created_entry["title"] == sample_changelog_data["title"]
        assert created_entry["description"] == sample_changelog_data["description"]
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_save_changelog_missing_title(self, mock_repository, sample_context):
        """Test changelog save with missing title."""
        # Act
        save_changelog_func = save_changelog(sample_context)
        result = save_changelog_func(title="", description="test desc", position=1)

        # Assert
        mock_repository.mongo.changelog.create.assert_not_called()
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_save_changelog_exception(self, mock_repository, sample_context, sample_changelog_data):
        """Test changelog save with exception."""
        # Arrange
        mock_repository.mongo.changelog.create.side_effect = Exception("Database error")

        # Act
        save_changelog_func = save_changelog(sample_context)
        result = save_changelog_func(**sample_changelog_data)

        # Assert
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_get_changelog_success(self, mock_repository, sample_context):
        """Test successful changelog retrieval."""
        # Arrange
        expected_changelogs = [
            {"id": "1", "title": "Test 1"},
            {"id": "2", "title": "Test 2"}
        ]
        mock_repository.mongo.changelog.find.return_value = expected_changelogs

        # Act
        get_changelog_func = get_changelog(sample_context)
        result = get_changelog_func()

        # Assert
        mock_repository.mongo.changelog.find.assert_called_once_with(
            {"organizationId": sample_context["org_id"]}
        )
        assert result == expected_changelogs

    @patch('services.agents.tools.changelog.repository')
    def test_get_changelog_exception(self, mock_repository, sample_context):
        """Test changelog retrieval with exception."""
        # Arrange
        mock_repository.mongo.changelog.find.side_effect = Exception("Database error")

        # Act
        get_changelog_func = get_changelog(sample_context)
        result = get_changelog_func()

        # Assert
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_delete_changelog_success(self, mock_repository, sample_context):
        """Test successful changelog deletion."""
        # Act
        delete_changelog_func = delete_changelog(sample_context)
        result = delete_changelog_func("test_id_123")

        # Assert
        mock_repository.mongo.changelog.delete_by_id.assert_called_once_with("test_id_123")
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_delete_changelog_empty_id(self, mock_repository, sample_context):
        """Test changelog deletion with empty ID."""
        # Act
        delete_changelog_func = delete_changelog(sample_context)
        result = delete_changelog_func("")

        # Assert
        mock_repository.mongo.changelog.delete_by_id.assert_not_called()
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_sort_changelog_success(self, mock_repository, sample_context):
        """Test successful changelog sorting."""
        # Arrange
        changelog_ids = ["id1", "id2", "id3"]
        positions = [3, 1, 2]

        # Act
        sort_changelog_func = sort_changelog(sample_context)
        result = sort_changelog_func(changelog_ids, positions)

        # Assert
        assert mock_repository.mongo.changelog.update_by_id.call_count == 3
        mock_repository.mongo.changelog.update_by_id.assert_any_call("id1", {"position": 3})
        mock_repository.mongo.changelog.update_by_id.assert_any_call("id2", {"position": 1})
        mock_repository.mongo.changelog.update_by_id.assert_any_call("id3", {"position": 2})
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_sort_changelog_invalid_input(self, mock_repository, sample_context):
        """Test changelog sorting with invalid input."""
        # Act
        sort_changelog_func = sort_changelog(sample_context)
        result = sort_changelog_func(["id1"], [1, 2])  # Mismatched lengths

        # Assert
        mock_repository.mongo.changelog.update_by_id.assert_not_called()
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_update_changelog_success(self, mock_repository, sample_context):
        """Test successful changelog update."""
        # Arrange
        update_data = {
            "changelog_id": "test_id_123",
            "title": "Updated Title",
            "description": "Updated Description",
            "position": 2,
            "show": False,
            "estimated_date": "2024-02-01"
        }

        # Act
        update_changelog_func = update_changelog(sample_context)
        result = update_changelog_func(**update_data)

        # Assert
        expected_update = {
            "title": "Updated Title",
            "description": "Updated Description",
            "position": 2,
            "show": False,
            "estimated_date": "2024-02-01"
        }
        mock_repository.mongo.changelog.update_by_id.assert_called_once_with(
            "test_id_123", expected_update
        )
        assert result is None

    @patch('services.agents.tools.changelog.repository')
    def test_update_changelog_missing_required_fields(self, mock_repository, sample_context):
        """Test changelog update with missing required fields."""
        # Act
        update_changelog_func = update_changelog(sample_context)
        result = update_changelog_func(changelog_id="", title="", description="test", position=1)

        # Assert
        mock_repository.mongo.changelog.update_by_id.assert_not_called()
        assert result is None
