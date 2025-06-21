from unittest.mock import Mock, patch

from services.agents.tools.out_docs import save_out_doc


class TestOutDocsTools:
    """Test cases for out_docs tool functions."""

    @patch('services.agents.tools.out_docs.repository')
    def test_save_out_doc_success(self, mock_repository, sample_context, sample_document_data):
        """Test successful document save."""
        # Arrange
        mock_doc = Mock()
        mock_doc.id = "doc_id_123"
        mock_repository.mongo.out_document.create.return_value = mock_doc

        # Act
        save_out_doc_func = save_out_doc(sample_context)
        result = save_out_doc_func(**sample_document_data)

        # Assert
        mock_repository.mongo.out_document.create.assert_called_once()
        created_doc = mock_repository.mongo.out_document.create.call_args[0][0]
        assert created_doc["organizationId"] == sample_context["org_id"]
        assert created_doc["text"] == sample_document_data["text"]
        assert created_doc["publish"] == sample_document_data["publish"]
        assert created_doc["tags"] == ["test", "document", "sample"]
        assert created_doc["workflow"] == sample_context["workflow"]
        assert created_doc["agent"] == sample_context["agent_name"]
        assert result is None

    @patch('services.agents.tools.out_docs.repository')
    def test_save_out_doc_with_defaults(self, mock_repository, sample_context):
        """Test document save with default values."""
        # Arrange
        mock_doc = Mock()
        mock_doc.id = "doc_id_456"
        mock_repository.mongo.out_document.create.return_value = mock_doc

        # Act
        save_out_doc_func = save_out_doc(sample_context)
        result = save_out_doc_func("Test document content")

        # Assert
        mock_repository.mongo.out_document.create.assert_called_once()
        created_doc = mock_repository.mongo.out_document.create.call_args[0][0]
        assert created_doc["text"] == "Test document content"
        assert created_doc["publish"] is False
        assert created_doc["tags"] == []
        assert result is None

    @patch('services.agents.tools.out_docs.repository')
    def test_save_out_doc_empty_text(self, mock_repository, sample_context):
        """Test document save with empty text."""
        # Act
        save_out_doc_func = save_out_doc(sample_context)
        result = save_out_doc_func("")

        # Assert
        mock_repository.mongo.out_document.create.assert_not_called()
        assert result is None

    @patch('services.agents.tools.out_docs.repository')
    def test_save_out_doc_tags_parsing(self, mock_repository, sample_context):
        """Test document save with various tag formats."""
        # Arrange
        mock_doc = Mock()
        mock_doc.id = "doc_id_789"
        mock_repository.mongo.out_document.create.return_value = mock_doc

        test_cases = [
            ("tag1,tag2,tag3", ["tag1", "tag2", "tag3"]),
            ("tag1, tag2 , tag3 ", ["tag1", "tag2", "tag3"]),  # With spaces
            ("tag1,,tag2,", ["tag1", "tag2"]),  # With empty tags
            ("", []),  # Empty tags
            ("single-tag", ["single-tag"]),  # Single tag
        ]

        for tags_input, expected_tags in test_cases:
            mock_repository.mongo.out_document.create.reset_mock()

            # Act
            save_out_doc_func = save_out_doc(sample_context)
            save_out_doc_func("Test content", tags=tags_input)

            # Assert
            created_doc = mock_repository.mongo.out_document.create.call_args[0][0]
            assert created_doc["tags"] == expected_tags

    @patch('services.agents.tools.out_docs.repository')
    def test_save_out_doc_exception(self, mock_repository, sample_context, sample_document_data):
        """Test document save with exception."""
        # Arrange
        mock_repository.mongo.out_document.create.side_effect = Exception("Database error")

        # Act
        save_out_doc_func = save_out_doc(sample_context)
        result = save_out_doc_func(**sample_document_data)

        # Assert
        assert result is None

    @patch('services.agents.tools.out_docs.repository')
    def test_save_out_doc_context_values(self, mock_repository):
        """Test document save with different context values."""
        # Arrange
        context = {
            "org_id": 999,
            "agent_name": "CustomAgent",
            "workflow": "custom_workflow"
        }
        mock_doc = Mock()
        mock_doc.id = "doc_id_custom"
        mock_repository.mongo.out_document.create.return_value = mock_doc

        # Act
        save_out_doc_func = save_out_doc(context)
        save_out_doc_func("Custom content", publish=True, tags="custom,test")

        # Assert
        created_doc = mock_repository.mongo.out_document.create.call_args[0][0]
        assert created_doc["organizationId"] == 999
        assert created_doc["agent"] == "CustomAgent"
        assert created_doc["workflow"] == "custom_workflow"
        assert created_doc["publish"] is True
        assert created_doc["tags"] == ["custom", "test"]
