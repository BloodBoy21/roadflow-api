from unittest.mock import Mock, patch


class TestCeleryTasks:
    """Test cases for Celery tasks."""

    @patch('builtins.print')
    def test_hello_task(self, mock_print):
        """Test hello task execution."""
        # Import and call the task function directly
        from services.celery_jobs.tasks import hello

        # Arrange
        mock_self = Mock()

        # Act - call the underlying function with correct signature
        hello.run()

        # Assert
        mock_print.assert_called_once_with("hello world")


    @patch('services.celery_jobs.tasks.repository')
    @patch('services.celery_jobs.tasks.WorkflowService')
    def test_run_workflow_success(self, mock_workflow_service, mock_repository):
        """Test successful workflow execution."""
        from services.celery_jobs.tasks import run_workflow

        # Arrange
        mock_self = Mock()
        mock_workflow = Mock()
        mock_workflow.id = "workflow_123"
        mock_repository.mongo.workflow.find_by_id.return_value = mock_workflow

        workflow_id = "workflow_123"
        payload = {"test": "data"}
        source = "test_source"
        source_log_id = "log_456"

        # Act - call using task.run() method
        run_workflow.run(
            workflow_id,
            payload=payload,
            source=source,
            source_log_id=source_log_id
        )

        # Assert
        mock_repository.mongo.workflow.find_by_id.assert_called_once_with(workflow_id)
        mock_workflow_service.run_workflow.assert_called_once_with(
            mock_workflow,
            payload,
            context={},
            source=source,
            source_log_id=source_log_id
        )

    @patch('services.celery_jobs.tasks.repository')
    @patch('services.celery_jobs.tasks.WorkflowService')
    def test_run_workflow_not_found(self, mock_workflow_service, mock_repository):
        """Test workflow execution when workflow not found."""
        from services.celery_jobs.tasks import run_workflow

        # Arrange
        mock_self = Mock()
        mock_repository.mongo.workflow.find_by_id.return_value = None

        workflow_id = "nonexistent_workflow"

        # Act
        result = run_workflow.run(workflow_id)

        # Assert
        mock_repository.mongo.workflow.find_by_id.assert_called_once_with(workflow_id)
        mock_workflow_service.run_workflow.assert_not_called()
        assert result is None

    @patch('services.celery_jobs.tasks.repository')
    @patch('services.celery_jobs.tasks.WorkflowService')
    def test_run_workflow_with_defaults(self, mock_workflow_service, mock_repository):
        """Test workflow execution with default parameters."""
        from services.celery_jobs.tasks import run_workflow

        # Arrange
        mock_self = Mock()
        mock_workflow = Mock()
        mock_repository.mongo.workflow.find_by_id.return_value = mock_workflow

        workflow_id = "workflow_123"

        # Act
        run_workflow.run(workflow_id)

        # Assert
        mock_workflow_service.run_workflow.assert_called_once_with(
            mock_workflow,
            None,  # payload default
            context={},
            source="",  # source default
            source_log_id=None  # source_log_id default
        )

    @patch('services.celery_jobs.tasks.repository')
    @patch('services.celery_jobs.tasks.WorkflowService')
    def test_run_workflow_with_all_parameters(self, mock_workflow_service, mock_repository):
        """Test workflow execution with all parameters provided."""
        from services.celery_jobs.tasks import run_workflow

        # Arrange
        mock_self = Mock()
        mock_workflow = Mock()
        mock_repository.mongo.workflow.find_by_id.return_value = mock_workflow

        workflow_id = "workflow_789"
        payload = {"complex": {"nested": "data"}}
        source = "api_endpoint"
        source_log_id = "detailed_log_123"

        # Act
        run_workflow.run(
            workflow_id,
            payload=payload,
            source=source,
            source_log_id=source_log_id
        )

        # Assert
        mock_workflow_service.run_workflow.assert_called_once_with(
            mock_workflow,
            payload,
            context={},
            source=source,
            source_log_id=source_log_id
        )

    @patch('services.celery_jobs.tasks.repository')
    @patch('services.celery_jobs.tasks.WorkflowService')
    @patch('services.celery_jobs.tasks.logger')
    def test_run_workflow_logs_workflow_not_found(self, mock_logger, mock_workflow_service, mock_repository):
        """Test that workflow not found scenario is logged."""
        from services.celery_jobs.tasks import run_workflow

        # Arrange
        mock_self = Mock()
        mock_repository.mongo.workflow.find_by_id.return_value = None

        workflow_id = "missing_workflow"

        # Act
        run_workflow.run(workflow_id)

        # Assert
        mock_logger.error.assert_called_once_with(
            f"Workflow with ID {workflow_id} not found."
        )
