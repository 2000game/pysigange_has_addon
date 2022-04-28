from __future__ import annotations
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PySignageEntity
from .const import CONF_COORDINATOR, DOMAIN as PYSIGNAGE_DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Pysignage component."""
    coordinator = hass.data[PYSIGNAGE_DOMAIN][entry.entry_id][CONF_COORDINATOR]
    async_add_entities(
        [
            PySignageSwitch(coordinator, name)
            for name in coordinator.data["Switches"].keys()
        ]
    )

class PySignageSwitch(PySignageEntity, SwitchEntity):
    """THe switch class for PySignage"""

    @property
    def is_on(self) -> bool:
        """Return true if the entity is on."""
        return self.device["state"]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.hass.async_add_executor_job(self.device["pysignage"].play_playlist_on_all_devices, self.unique_id)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.hass.async_add_executor_job(self.device["pysignage"].return_to_scheduled_content)
        await self.coordinator.async_refresh()