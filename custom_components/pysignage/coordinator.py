"""Data update coordinator for pysignage."""
from __future__ import annotations
from datetime import timedelta


from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from pysignageserver.pysignageserver import PySignageServer

from .const import DOMAIN, LOGGER, CONF_CONNECTIONS

class PySignageDataUpdateCoordinator(DataUpdateCoordinator):
    """PySignage Data Update Coordinator"""


    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Intialize"""
        self.entry = entry
        self.pysignage: PySignageServer = hass.data[DOMAIN][self.entry.entry_id][CONF_CONNECTIONS]
        super().__init__(
            hass,
            LOGGER,
            name=entry.entry_id,
            update_interval=timedelta(seconds=30),
        )

    def _update_playlist_switches(self) -> dict[str, dict]:
        """Update playlist switches"""
        try:
            self.pysignage.refresh()
        except Exception as ex:
            raise UpdateFailed from ex
        playlists = self.pysignage.get_playable_playlists()
        data = {"Switches": {}, "Buttons": {}}
        for playlist in playlists:
            state = self.pysignage.get_playlist_state(playlist)
            data["Switches"][playlist] = {"state": state, "pysignage": self.pysignage}
        features = ["End Stream", "Play Stream Only", "Play Countdown Only", "Play Countdown and Stream", "Return to scheduled Content"]
        for feature in features:
            data["Buttons"][feature] = {"pysignage": self.pysignage}
        return data

    async def _async_update_data(self) -> dict[str, bool]:
        """Update data"""
        return await self.hass.async_add_executor_job(self._update_playlist_switches)



