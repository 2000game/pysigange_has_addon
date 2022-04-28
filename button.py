from __future__ import annotations
from typing import Any

from homeassistant.components.button import ButtonEntity
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
    entity_list = []
    #eatures = ["End Stream", "Play Stream Only", "Play Countdown Only", "Play Countdown and Stream", "Return to scheduled Content"]
    for feature in coordinator.data["Buttons"].keys():
        if feature == "End Stream":
            entity_list.append(EndStreamButton(coordinator, feature))
        elif feature == "Play Stream Only":
            entity_list.append(PlayStreamOnlyButton(coordinator, feature))
        elif feature == "Play Countdown Only":
            entity_list.append(PlayCountdownOnlyButton(coordinator, feature))
        elif feature == "Play Countdown and Stream":
            entity_list.append(PlayCountdownStreamButton(coordinator, feature))
        elif feature == "Return to scheduled Content":
            entity_list.append(ReturnToScheduledContentButton(coordinator, feature))

    async_add_entities(
        entity_list
    )


class EndStreamButton(PySignageEntity, ButtonEntity):
    """Switch to End the Stream"""

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self.device["pysignage"].end_stream)
        await self.coordinator.async_refresh()

class PlayStreamOnlyButton(PySignageEntity, ButtonEntity):
    """Switch to End the Stream"""

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self.device["pysignage"].play_stream_only)
        await self.coordinator.async_refresh()

class PlayCountdownOnlyButton(PySignageEntity, ButtonEntity):
    """Switch to End the Stream"""

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self.device["pysignage"].play_countdown_only)
        await self.coordinator.async_refresh()

class PlayCountdownStreamButton(PySignageEntity, ButtonEntity):
    """Switch to End the Stream"""

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self.device["pysignage"].play_countdown_stream)
        await self.coordinator.async_refresh()

class ReturnToScheduledContentButton(PySignageEntity, ButtonEntity):
    """Switch to End the Stream"""

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self.device["pysignage"].return_to_scheduled_content)
        await self.coordinator.async_refresh()