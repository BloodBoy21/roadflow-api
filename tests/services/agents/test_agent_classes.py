from unittest.mock import Mock, patch

import pytest

from services.agents.customer_agent import CustomerAgent
from services.agents.engineer_agent import EngineerAgent
from services.agents.growth_agent import GrowthAgent
from services.agents.operations_agent import OperationsAgent
from services.agents.product_agent import ProductAgent


class TestAgentClasses:
    """Test cases for individual agent classes."""

    @patch('services.agents.base.repository')
    def test_engineer_agent_initialization(self, mock_repository):
        """Test EngineerAgent initialization."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act
        agent = EngineerAgent(org_id=123)

        # Assert
        assert agent.name == "EngineerAgent"
        assert "engineering tasks" in agent.description
        assert "engineer agent" in agent.instructions
        assert "changelog" in agent.instructions
        assert "documentation" in agent.instructions

    @patch('services.agents.base.repository')
    def test_product_agent_initialization(self, mock_repository):
        """Test ProductAgent initialization."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act
        agent = ProductAgent(org_id=456)

        # Assert
        assert agent.name == "ProductAgent"
        assert "product management tasks" in agent.description
        assert "product agent" in agent.instructions
        assert "product roadmaps" in agent.instructions
        assert "feature specifications" in agent.instructions
        assert "user feedback analysis" in agent.instructions

    @patch('services.agents.base.repository')
    def test_operations_agent_initialization(self, mock_repository):
        """Test OperationsAgent initialization."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act
        agent = OperationsAgent(org_id=789)

        # Assert
        assert agent.name == "OperationsAgent"
        assert "operations management tasks" in agent.description
        assert "operations agent" in agent.instructions
        assert "system monitoring" in agent.instructions
        assert "process optimization" in agent.instructions
        assert "incident response" in agent.instructions

    @patch('services.agents.base.repository')
    def test_customer_agent_initialization(self, mock_repository):
        """Test CustomerAgent initialization."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act
        agent = CustomerAgent(org_id=101112)

        # Assert
        assert agent.name == "CustomerAgent"
        assert "customer service tasks" in agent.description
        assert "customer service agent" in agent.instructions
        assert "customer inquiries" in agent.instructions
        assert "support ticket management" in agent.instructions
        assert "customer feedback analysis" in agent.instructions

    @patch('services.agents.base.repository')
    def test_growth_agent_initialization(self, mock_repository):
        """Test GrowthAgent initialization."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act
        agent = GrowthAgent(org_id=131415)

        # Assert
        assert agent.name == "GrowthAgent"
        assert "growth and marketing tasks" in agent.description
        assert "growth agent" in agent.instructions
        assert "marketing campaigns" in agent.instructions
        assert "user acquisition strategies" in agent.instructions
        assert "conversion optimization" in agent.instructions
        assert "growth metrics tracking" in agent.instructions

    @patch('services.agents.base.repository')
    def test_all_agents_have_same_tools(self, mock_repository):
        """Test that all agents have the same tool structure."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        agents = [
            EngineerAgent(org_id=1),
            ProductAgent(org_id=2),
            OperationsAgent(org_id=3),
            CustomerAgent(org_id=4),
            GrowthAgent(org_id=5)
        ]

        # Act & Assert
        for agent in agents:
            tool_callbacks = [tool["callback"].__name__ for tool in agent.tools]
            expected_callbacks = [
                "save_changelog",
                "get_changelog",
                "delete_changelog",
                "sort_changelog"
            ]
            assert tool_callbacks == expected_callbacks

    @patch('services.agents.base.repository')
    def test_agents_with_none_org_id(self, mock_repository):
        """Test agents initialization with None org_id."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act & Assert - should raise ValueError during _get_config call
        with pytest.raises(ValueError):
            EngineerAgent(org_id=None)

        with pytest.raises(ValueError):
            ProductAgent(org_id=None)

        with pytest.raises(ValueError):
            OperationsAgent(org_id=None)

        with pytest.raises(ValueError):
            CustomerAgent(org_id=None)

        with pytest.raises(ValueError):
            GrowthAgent(org_id=None)

    @patch('services.agents.base.repository')
    @patch('services.agents.base.AgentFactory')
    def test_agents_can_build(self, mock_factory, mock_repository):
        """Test that all agents can be built successfully."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()
        mock_built_agent = Mock()
        mock_factory.create_agent.return_value = mock_built_agent

        agents = [
            EngineerAgent(org_id=1),
            ProductAgent(org_id=2),
            OperationsAgent(org_id=3),
            CustomerAgent(org_id=4),
            GrowthAgent(org_id=5)
        ]

        # Act & Assert
        for agent in agents:
            built_agent = agent.build()
            assert built_agent == mock_built_agent
            assert agent.agent == mock_built_agent
