from .agent_repository import AgentRepository
from .input_webhook_repository import InputWebhookRepository
from .integration_repository import IntegrationRepository
from .invitation_repository import InvitationRepository
from .organization_repository import OrganizationRepository
from .organization_user_repository import OrganizationUserRepository
from .platform_repository import PlatformRepository
from .user_repository import UserRepository


class Repository:
    def __init__(self):
        self.agent = AgentRepository()
        self.integration = IntegrationRepository()
        self.organization = OrganizationRepository()
        self.platform = PlatformRepository()
        self.user = UserRepository()
        self.organization_user = OrganizationUserRepository()
        self.input_webhook = InputWebhookRepository()
        self.invitation = InvitationRepository()
