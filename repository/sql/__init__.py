from .agent_repository import AgentRepository
from .integration_repository import IntegrationRepository
from .member_repository import MemberRepository
from .organization_repository import OrganizationRepository
from .platform_repository import PlatformRepository
from .user_repository import UserRepository
from .organization_user_repository import OrganizationUserRepository


class Repository:
    def __init__(self):
        self.agent = AgentRepository()
        self.integration = IntegrationRepository()
        self.member = MemberRepository()
        self.organization = OrganizationRepository()
        self.platform = PlatformRepository()
        self.user = UserRepository()
        self.organization_user = OrganizationUserRepository()
