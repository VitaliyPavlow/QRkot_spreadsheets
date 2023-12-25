from dependency_injector import containers, providers

from app.core.db import AsyncSessionLocal
from app.core.google_client import get_service
from app.models import CharityProject, Donation
from app.repositories import CharityProjectRepository, DonationRepository
from app.services.google_api_servies import GoogleService


class Container(containers.DeclarativeContainer):
    """Dependency Injector Container."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.charity_project",
            "app.api.endpoints.donation",
            "app.api.validators",
            "app.services.investment_processing",
            "app.api.endpoints.google",
        ],
    )

    db_session_factory = providers.Factory(AsyncSessionLocal)

    charity_repository = providers.Factory(
        CharityProjectRepository,
        model=CharityProject,
        session_factory=db_session_factory,
    )

    donation_repository = providers.Factory(
        DonationRepository, model=Donation, session_factory=db_session_factory
    )

    google_client = providers.Resource(get_service)

    google_service = providers.Factory(
        GoogleService, wrapper_service=google_client
    )
