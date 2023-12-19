from dependency_injector import containers, providers

from app.models import CharityProject, Donation
from app.repositories import CharityProjectRepository, DonationRepository
from app.services.google_api_servies import GoogleServices


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

    charity_repository = providers.Singleton(
        CharityProjectRepository, model=CharityProject
    )
    donation_repository = providers.Singleton(
        DonationRepository, model=Donation
    )
    google_services = providers.Singleton(GoogleServices)
