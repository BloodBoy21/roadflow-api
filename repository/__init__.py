from repository.mongo import Repository as MongoRepository
from repository.sql import Repository as SQLRepository


class RepositoryFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_repositories()
        return cls._instance

    def _init_repositories(self):
        self.sql: SQLRepository = SQLRepository()
        self.mongo: MongoRepository = MongoRepository()


repository = RepositoryFactory()
