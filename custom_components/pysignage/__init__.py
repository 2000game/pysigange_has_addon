"""The Pysignage component"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_PORT,
)
from homeassistant.core import Event, HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.entity_registry import RegistryEntry, async_migrate_entries
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_CONNECTIONS, CONF_COORDINATOR, DOMAIN, LOGGER, PLATFORMS
from .coordinator import PySignageDataUpdateCoordinator

from pysignageserver.pysignageserver import PySignageServer

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Pysignage component."""
    pysignage = PySignageServer(
        host=entry.data[CONF_HOST],
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        port=entry.data[CONF_PORT],
    )

    try:
        await hass.async_add_executor_job(pysignage.refresh)
    except Exception as ex:
        raise ConfigEntryAuthFailed from ex

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_CONNECTIONS: pysignage,
    }

    coordinator = PySignageDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id][CONF_COORDINATOR] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

class PySignageEntity(CoordinatorEntity[PySignageDataUpdateCoordinator]):
    """Basis PySignage Entity"""

    def __init__(
        self,
        coordinator: PySignageDataUpdateCoordinator,
        name: str,
        entity_description: EntityDescription | None = None,

    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = name

    @property
    def device(self) -> bool:
        if self.unique_id in self.coordinator.data["Switches"]:
            return self.coordinator.data["Switches"][self.unique_id]
        else:
            return self.coordinator.data["Buttons"][self.unique_id]

