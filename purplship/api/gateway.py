"""Purplship API Gateway modules."""

import attr
import pkgutil
import logging
from typing import Callable, Union
from purplship.core import Settings
from purplship.api.proxy import Proxy
from purplship.api.mapper import Mapper
from purplship.core.errors import PurplShipError
import purplship.mappers as mappers

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class Gateway:
    mapper: Mapper
    proxy: Proxy
    settings: Settings


@attr.s(auto_attribs=True)
class GatewayInitializer:
    initializer: Callable[[Union[Settings, dict]], Gateway]

    def create(self, settings: dict) -> Gateway:
        return self.initializer(settings)


class _ProviderMapper:
    @property
    def providers(self):
        # Register Purplship mappers
        return {
            name: __import__(f"{mappers.__name__}.{name}", fromlist=[name])
            for _, name, _ in pkgutil.iter_modules(mappers.__path__)
        }

    def __getitem__(self, key) -> GatewayInitializer:
        def initializer(settings: Union[Settings, dict]) -> Gateway:
            try:
                provider = self.providers[key]
                settings_value: Settings = (
                    provider.Settings(**settings)
                    if isinstance(settings, dict)
                    else settings
                )
                return Gateway(
                    settings=settings_value,
                    proxy=provider.Proxy(settings_value),
                    mapper=provider.Mapper(settings_value),
                )
            except KeyError as e:
                raise PurplShipError(f"Unknown provider '{key}'") from e
            except Exception as e:
                raise PurplShipError(f"Failed to setup provider '{key}'") from e

        return GatewayInitializer(initializer)


gateway = _ProviderMapper()
logger.info(
    f"""
Purplship default gateway mapper initialized.
Registered providers: {','.join(gateway.providers)}
"""
)
