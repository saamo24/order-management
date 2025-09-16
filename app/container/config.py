from dependency_injector import containers, providers

from app.core.config import settings


class Config(containers.DeclarativeContainer):

    config = providers.Configuration()

    config.override({
        "mongodb_url": settings.mongodb_url,
        "database_name": settings.database_name,
        "api_title": settings.api_title,
        "api_version": settings.api_version,
        "api_description": settings.api_description,
        "host": settings.host,
        "port": settings.port,
        "debug": settings.debug,
        "secret_key": settings.secret_key,
    })
