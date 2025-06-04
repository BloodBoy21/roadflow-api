from .changelog_repository import ChangelogRepository
from .knowledge_repository import KnowledgeRepository
from .logs_repository import LogsRepository
from .out_repository import OutDocumentRepository
from .platform_repository import PlatformRepository
from .repository_repository import RepositoryRepository
from .workflow_repository import WorkflowRepository


class Repository:
    def __init__(self):
        self.changelog = ChangelogRepository()
        self.knowledge = KnowledgeRepository()
        self.logs = LogsRepository()
        self.out_document = OutDocumentRepository()
        self.platform = PlatformRepository()
        self.repository = RepositoryRepository()
        self.workflow = WorkflowRepository()
