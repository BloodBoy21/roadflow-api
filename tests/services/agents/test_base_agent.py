from unittest.mock import Mock, patch

import pytest

from models.inputs.agent import ContentConfig
from services.agents.base import AgentBase, AgentFactory


class TestAgentFactory:
    """Test cases for AgentFactory class."""

    @patch('services.agents.base.LlmAgent')
    @patch('services.agents.base.types')
    def test_create_agent_with_minimal_params(self, mock_types, mock_llm_agent):
        """Test agent creation with minimal parameters."""
        # Arrange
        mock_agent_instance = Mock()
        mock_llm_agent.return_value = mock_agent_instance
        mock_types.GenerateContentConfig.return_value = Mock()

        content_config = ContentConfig()

        # Act
        result = AgentFactory.create_agent_legacy(
            agent_name="TestAgent",
            tools=[],
            content_config=content_config
        )

        # Assert
        mock_llm_agent.assert_called_once()
        call_args = mock_llm_agent.call_args[1]
        assert call_args["name"] == "TestAgent"
        assert call_args["tools"] == []
        assert "TestAgent_output_" in call_args["output_key"]
        assert result == mock_agent_instance

    @patch('services.agents.base.LlmAgent')
    @patch('services.agents.base.types')
    def test_create_agent_with_all_params(self, mock_types, mock_llm_agent):
        """Test agent creation with all parameters."""
        # Arrange
        mock_agent_instance = Mock()
        mock_llm_agent.return_value = mock_agent_instance
        mock_types.GenerateContentConfig.return_value = Mock()

        content_config = ContentConfig(temperature=0.7, top_p=0.9, top_k=40)
        tools = [Mock()]
        sub_agents = [Mock()]

        # Act
        result = AgentFactory.create_agent_legacy(
            agent_name="ComplexAgent",
            tools=tools,
            model="custom-model",
            description="A complex test agent",
            content_config=content_config,
            output_key="custom_output_key",
            global_instruction="Custom global instruction",
            instructions="Custom instructions",
            sub_agents=sub_agents
        )

        # Assert
        call_args = mock_llm_agent.call_args[1]
        assert call_args["name"] == "ComplexAgent"
        assert call_args["model"] == "custom-model"
        assert call_args["description"] == "A complex test agent"
        assert call_args["instruction"] == "Custom instructions"
        assert call_args["output_key"] == "custom_output_key"
        assert call_args["sub_agents"] == sub_agents

    def test_global_prompt_with_custom_prompt(self):
        """Test global prompt generation with custom prompt."""
        # Act
        result = AgentFactory.global_prompt("Custom prompt here")

        # Assert
        assert "Custom prompt here" in result
        assert "Today is:" in result
        assert "save_out_doc" in result

    def test_global_prompt_without_custom_prompt(self):
        """Test global prompt generation without custom prompt."""
        # Act
        result = AgentFactory.global_prompt()

        # Assert
        assert "Today is:" in result
        assert "save_out_doc" in result

    def test_create_output_key(self):
        """Test output key creation."""
        # Act
        result = AgentFactory.create_output_key("TestAgent")

        # Assert
        assert result.startswith("TestAgent_output_")
        assert len(result) > len("TestAgent_output_")


class TestAgentBase:
    """Test cases for AgentBase class."""

    @patch('services.agents.base.repository')
    def test_agent_base_init_success(self, mock_repository):
        """Test successful AgentBase initialization."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Act
        agent = AgentBase(
            name="TestAgent",
            description="Test description",
            org_id=123,
            instructions="Test instructions"
        )

        # Assert
        assert agent.name == "TestAgent"
        assert agent.description == "Test description"
        assert agent.org_id == 123
        assert agent.instructions == "Test instructions"
        assert isinstance(agent.content_config, ContentConfig)
        mock_repository.mongo.agent.create.assert_called_once()

    @patch('services.agents.base.repository')
    def test_agent_base_init_with_existing_config(self, mock_repository):
        """Test AgentBase initialization with existing config."""
        # Arrange
        existing_config = Mock()
        existing_config.instructions = "Existing instructions"
        existing_config.description = "Existing description"
        existing_config.content_config = ContentConfig(temperature=0.5)
        existing_config.global_instruction = "Existing global instruction"

        mock_repository.mongo.agent.get_agent_config.return_value = existing_config

        # Act
        agent = AgentBase(
            name="TestAgent",
            description="Test description",
            org_id=123,
            instructions="Test instructions"
        )

        # Assert
        assert agent.instructions == "Existing instructions"
        assert agent.description == "Existing description"
        assert agent.content_config.temperature == 0.5
        assert agent.global_instruction == "Existing global instruction"
        mock_repository.mongo.agent.create.assert_not_called()

    def test_agent_base_init_without_org_id(self):
        """Test AgentBase initialization without org_id raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="org_id is not set for the agent"):
            AgentBase(name="TestAgent", org_id=None)

    @patch('services.agents.base.repository')
    @patch('services.agents.base.AgentFactory')
    def test_build_agent(self, mock_factory, mock_repository):
        """Test agent building."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        mock_agent_instance = Mock()
        mock_factory.create_agent.return_value = mock_agent_instance

        agent = AgentBase(name="TestAgent", org_id=123)

        # Act
        result = agent.build()

        # Assert
        mock_factory.create_agent.assert_called_once()
        assert result == mock_agent_instance
        assert agent.agent == mock_agent_instance

    @patch('services.agents.base.repository')
    @patch('services.agents.base.AgentFactory')
    def test_build_agent_already_built(self, mock_factory, mock_repository):
        """Test agent building when already built."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        existing_agent = Mock()
        agent = AgentBase(name="TestAgent", org_id=123)
        agent.agent = existing_agent

        # Act
        result = agent.build()

        # Assert
        mock_factory.create_agent.assert_not_called()
        assert result == existing_agent

    @patch('services.agents.base.repository')
    def test_get_agent_info(self, mock_repository):
        """Test getting agent information."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        agent = AgentBase(
            name="TestAgent",
            description="Test description",
            org_id=123,
            instructions="Test instructions"
        )

        # Act
        result = agent.get_agent_info()

        # Assert
        assert result["name"] == "TestAgent"
        assert result["description"] == "Test description"
        assert result["instructions"] == "Test instructions"
        assert "content_config" in result

    @patch('services.agents.base.repository')
    @patch('services.agents.tools.out_docs.save_out_doc')
    def test_build_tools(self, mock_save_out_doc, mock_repository):
        """Test building tools."""
        # Arrange
        mock_repository.mongo.agent.get_agent_config.return_value = None
        mock_repository.mongo.agent.create.return_value = Mock()

        # Create a mock for the tool function returned by the callback
        mock_tool_func = Mock()
        mock_tool_func.__name__ = "mock_tool_function"

        # Create a mock for the callback that returns the tool function
        mock_callback = Mock()
        mock_callback.__name__ = "mock_callback"
        mock_callback.return_value = mock_tool_func

        # Mock the save_out_doc tool function returned by save_out_doc
        mock_save_out_doc_func = Mock()
        mock_save_out_doc_func.__name__ = "save_out_doc_tool"
        mock_save_out_doc.return_value = mock_save_out_doc_func
        mock_save_out_doc.__name__ = "save_out_doc"

        # Create a simple non-dict tool mock that won't interfere
        non_dict_tool = Mock()
        non_dict_tool.__name__ = "non_dict_tool"

        agent = AgentBase(name="TestAgent", org_id=123)
        agent.tools = [
            {"build": True, "callback": mock_callback},
            non_dict_tool  # Non-dict tool
        ]

        # Act
        result = agent.build_tools

        # Assert
        mock_save_out_doc.assert_called_once_with(context={"org_id": 123, "agent_name": "TestAgent"})
        # Result contains: non_dict_tool, built_tool_func, and save_out_doc_func
        assert len(result) == 3
        assert non_dict_tool in result
