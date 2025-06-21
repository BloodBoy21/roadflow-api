from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def mock_repository():
    """Mock repository for testing."""
    mock_repo = Mock()

    # Mock SQL repositories
    mock_repo.sql = Mock()
    mock_repo.sql.organization_user = Mock()
    mock_repo.sql.organization_user.get_organizations_by_user_id = AsyncMock()

    # Mock MongoDB repositories
    mock_repo.mongo = Mock()
    mock_repo.mongo.changelog = Mock()
    mock_repo.mongo.out_document = Mock()
    mock_repo.mongo.workflow = Mock()
    mock_repo.mongo.logs = Mock()
    mock_repo.mongo.agent = Mock()
    mock_repo.mongo.task = Mock()

    return mock_repo


@pytest.fixture
def sample_context():
    """Sample context for agent tools."""
    return {
        "org_id": 123,
        "agent_name": "TestAgent",
        "workflow": "test_workflow"
    }


@pytest.fixture
def sample_changelog_data():
    """Sample changelog data for testing."""
    return {
        "title": "Test Feature",
        "description": "Added new test feature",
        "position": 1,
        "show": True,
        "estimated_date": "2024-01-01"
    }


@pytest.fixture
def sample_document_data():
    """Sample document data for testing."""
    return {
        "text": "This is a test document",
        "publish": False,
        "tags": "test,document,sample"
    }
