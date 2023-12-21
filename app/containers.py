from dependency_injector import containers, providers

from app.core.db import get_async_session
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
    db_session = providers.Resource(get_async_session)
    charity_repository = providers.Singleton(
        CharityProjectRepository, model=CharityProject, session=db_session
    )
    donation_repository = providers.Singleton(
        DonationRepository, model=Donation, session=db_session
    )
    google_get_service = providers.Resource(get_service)
    google_service = providers.Factory(
        GoogleService, wrapper_services=google_get_service
    )
