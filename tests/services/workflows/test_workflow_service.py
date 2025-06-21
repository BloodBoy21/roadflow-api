from unittest.mock import AsyncMock, Mock, patch

import pytest

from models.mongo.workflow import Workflow
from services.workflows import WorkflowService


class TestWorkflowService:
    """Test cases for WorkflowService class."""

    def test_workflow_service_init(self):
        """Test WorkflowService initialization."""
        # Act
        service = WorkflowService(org_id=123, event="test_event")

        # Assert
        assert service.org_id == 123
        assert service.event == "test_event"

    @patch('services.workflows.repository')
    def test_get_workflow(self, mock_repository):
        """Test getting workflows."""
        # Arrange
        expected_workflows = [Mock(), Mock()]
        mock_repository.mongo.workflow.get_main_workflows_by_org_id.return_value = expected_workflows

        service = WorkflowService(org_id=123, event="test_event")

        # Act
        result = service.get_workflow()

        # Assert
        mock_repository.mongo.workflow.get_main_workflows_by_org_id.assert_called_once_with(
            org_id=123, event="test_event"
        )
        assert result == expected_workflows

    @patch('services.workflows.repository')
    @patch('services.celery_jobs.tasks.run_workflow')
    def test_run_with_workflows(self, mock_run_workflow_task, mock_repository):
        """Test running workflows."""
        # Arrange
        mock_workflow1 = Mock()
        mock_workflow1.id = "workflow_1"
        mock_workflow2 = Mock()
        mock_workflow2.id = "workflow_2"
        workflows = [mock_workflow1, mock_workflow2]

        mock_log = Mock()
        mock_log.id = "log_123"
        mock_repository.mongo.logs.create.return_value = mock_log
        mock_repository.mongo.workflow.get_main_workflows_by_org_id.return_value = workflows
        mock_run_workflow_task.delay = Mock()

        service = WorkflowService(org_id=123, event="test_event")
        payload = {"test": "data"}

        # Act
        service.run(payload)

        # Assert
        mock_repository.mongo.logs.create.assert_called_once()
        log_call_args = mock_repository.mongo.logs.create.call_args[0][0]
        assert log_call_args.organizationId == 123
        assert log_call_args.type == "input"
        assert log_call_args.source == "test_event"
        assert log_call_args.data == payload

        assert mock_run_workflow_task.delay.call_count == 2
        mock_run_workflow_task.delay.assert_any_call(
            workflow_id="workflow_1",
            payload=payload,
            source="test_event",
            source_log_id="log_123"
        )
        mock_run_workflow_task.delay.assert_any_call(
            workflow_id="workflow_2",
            payload=payload,
            source="test_event",
            source_log_id="log_123"
        )

    @patch('services.workflows.repository')
    def test_run_with_no_workflows(self, mock_repository):
        """Test running with no workflows."""
        # Arrange
        mock_log = Mock()
        mock_log.id = "log_123"
        mock_repository.mongo.logs.create.return_value = mock_log
        mock_repository.mongo.workflow.get_main_workflows_by_org_id.return_value = []

        service = WorkflowService(org_id=123, event="test_event")

        # Act
        service.run()

        # Assert
        mock_repository.mongo.logs.create.assert_called_once()

    @patch('services.workflows.repository')
    @patch('services.workflows.AgentCaller')
    def test_run_workflow_with_agent(self, mock_agent_caller, mock_repository):
        """Test running a workflow with an agent."""
        # Arrange
        workflow = Mock(spec=Workflow)
        workflow.id = "workflow_123"
        workflow.organizationId = 456
        workflow.enabled = True
        workflow.is_task = False
        workflow.agent = "TestAgent"
        workflow.prompt = "Test prompt"
        workflow.next_flow = None

        mock_agent_instance = Mock()
        mock_agent_instance.generate = AsyncMock(return_value="Test response")
        mock_agent_caller.create.return_value = mock_agent_instance

        mock_log = Mock()
        mock_log.id = "log_456"
        mock_repository.mongo.logs.create.return_value = mock_log

        payload = {"input": "test"}

        # Act
        with patch('services.workflows.ObjectId') as mock_object_id:
            mock_object_id.return_value = "507f1f77bcf86cd799439011"
            WorkflowService.run_workflow(workflow, payload, source="test", source_log_id="507f1f77bcf86cd799439011")

        # Assert
        mock_agent_caller.create.assert_called_once_with(org_id=456, agent="TestAgent")
        mock_agent_instance.generate.assert_called_once()
        mock_repository.mongo.logs.create.assert_called_once()

    @patch('services.workflows.repository')
    def test_run_workflow_disabled(self, mock_repository):
        """Test running a disabled workflow."""
        # Arrange
        workflow = Mock(spec=Workflow)
        workflow.id = "workflow_123"
        workflow.enabled = False

        # Act
        result = WorkflowService.run_workflow(workflow, {})

        # Assert
        assert result is None
        mock_repository.mongo.logs.create.assert_not_called()

    def test_run_workflow_invalid_type(self):
        """Test running workflow with invalid type."""
        # Act & Assert
        with pytest.raises(TypeError):
            WorkflowService.run_workflow("not_a_workflow", {})

    @patch('services.workflows.repository')
    @patch('services.workflows.run_task')
    def test_run_task_workflow(self, mock_run_task, mock_repository):
        """Test running a task workflow."""
        # Arrange
        workflow = Mock(spec=Workflow)
        workflow.id = "task_workflow_123"
        workflow.organizationId = 789
        workflow.enabled = True
        workflow.is_task = True
        workflow.agent = "TaskAgent"
        workflow.task_template_id = "task_template_456"
        workflow.parameters = {"param": "value"}
        workflow.next_flow = None

        mock_task_template = Mock()
        mock_task_template.id = "task_template_456"
        mock_task_template.function_name = "test_task_function"
        mock_repository.mongo.task.find_by_id.return_value = mock_task_template

        mock_run_task.return_value = {"result": "success"}

        mock_log = Mock()
        mock_repository.mongo.logs.create.return_value = mock_log

        payload = {"input": "test"}

        # Act
        with patch('services.workflows.ObjectId') as mock_object_id:
            mock_object_id.return_value = "507f1f77bcf86cd799439012"
            WorkflowService.run_task(workflow, payload, source="task_test", source_log_id="507f1f77bcf86cd799439012")

        # Assert
        mock_repository.mongo.task.find_by_id.assert_called_once_with("task_template_456")
        mock_run_task.assert_called_once_with(
            task_name="test_task_function",
            payload={"param": "value"},
            context={"last_response": {"result": "success"}},
            source="task_test",
            source_log_id="507f1f77bcf86cd799439012"
        )
        mock_repository.mongo.logs.create.assert_called_once()

    @patch('services.workflows.repository')
    def test_run_task_template_not_found(self, mock_repository):
        """Test running task with missing template."""
        # Arrange
        workflow = Mock(spec=Workflow)
        workflow.id = "task_workflow_123"
        workflow.task_template_id = "missing_template"
        workflow.enabled = True
        workflow.is_task = True

        mock_repository.mongo.task.find_by_id.return_value = None

        # Act
        result = WorkflowService.run_task(workflow)

        # Assert
        assert result is None
        mock_repository.mongo.logs.create.assert_not_called()

    @patch('services.workflows.repository')
    @patch('services.workflows.AgentCaller')
    def test_run_workflow_with_next_flow(self, mock_agent_caller, mock_repository):
        """Test running workflow with next flow."""
        # Arrange
        workflow = Mock(spec=Workflow)
        workflow.id = "workflow_123"
        workflow.organizationId = 456
        workflow.enabled = True
        workflow.is_task = False
        workflow.agent = "TestAgent"
        workflow.prompt = "Test prompt"
        workflow.next_flow = "next_workflow_456"

        next_workflow = Mock(spec=Workflow)
        next_workflow.id = "next_workflow_456"
        next_workflow.enabled = True
        next_workflow.is_task = False
        next_workflow.organizationId = 456
        next_workflow.agent = "NextAgent"
        next_workflow.prompt = "Next prompt"
        next_workflow.next_flow = None

        mock_agent_instance = Mock()
        mock_agent_instance.generate = AsyncMock(return_value="Test response")
        mock_next_agent_instance = Mock()
        mock_next_agent_instance.generate = AsyncMock(return_value="Next response")

        mock_agent_caller.create.side_effect = [mock_agent_instance, mock_next_agent_instance]
        mock_repository.mongo.workflow.find_by_id.return_value = next_workflow
        mock_repository.mongo.logs.create.return_value = Mock()

        payload = {"input": "test"}

        # Act
        WorkflowService.run_workflow(workflow, payload)

        # Assert
        assert mock_agent_caller.create.call_count == 2
        assert mock_repository.mongo.logs.create.call_count == 2
        mock_repository.mongo.workflow.find_by_id.assert_called_once_with("next_workflow_456")
