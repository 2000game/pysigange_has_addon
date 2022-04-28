from __future__ import annotations

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "pysignage"
DEFAULT_PORT: Final = 3000

LOGGER: Final[logging.Logger] = logging.getLogger(__package__)
CONF_CONNECTIONS: Final = "connections"
CONF_COORDINATOR: Final = "coordinator"

PLATFORMS: Final[list[Platform]] = [Platform.SWITCH, Platform.BUTTON]
