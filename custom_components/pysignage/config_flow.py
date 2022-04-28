"""Config flow for Pysignage"""
from __future__ import annotations
from typing import Any

import voluptuous as vol


from homeassistant.config_entries import ConfigEntry, ConfigFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, DEFAULT_PORT

from typing import Any

from pysignageserver.pysignageserver import PySignageServer
from requests.exceptions import ConnectionError

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,

    }
)

RESULT_SUCCESS = "success"

class PysignageConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Pysignage"""

    VERSION = 1

    def __init__(self) -> None:
        self._entry: ConfigEntry | None = None
        self._host: str | None = None
        self._username: str | None = None
        self._password: str | None = None
        self._port: int | None = None

    def _get_entry(self, name: str) -> FlowResult:
        return self.async_create_entry(
            title=name,
            data={
                CONF_HOST: self._host,
                CONF_USERNAME: self._username,
                CONF_PASSWORD: self._password,
                CONF_PORT: self._port,
            },
        )

    async def _update_entry(self) -> None:
        assert self._entry is not None
        self.hass.config_entries.async_update_entry(
            self._entry,
            data={
                CONF_HOST: self._host,
                CONF_USERNAME: self._username,
                CONF_PASSWORD: self._password,
                CONF_PORT: self._port,
            },
        )
        await self.hass.config_entries.async_reload(self._entry.entry_id)

    def _try_connect(self) -> str:
        try:
            pysignage = PySignageServer(host=self._host, username=self._username, password=self._password, port=self._port).refresh()
            return RESULT_SUCCESS
        except ConnectionError:
            return "already_in_progress"
        except TypeError as err:
            return "invalid_auth"

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})

            self._host = user_input.get(CONF_HOST)
            self._username = user_input.get(CONF_USERNAME)
            self._password = user_input.get(CONF_PASSWORD)
            self._port = user_input.get(CONF_PORT)

            result = await self.hass.async_add_executor_job(self._try_connect)

            if result == RESULT_SUCCESS:
                return self._get_entry(self._host)
            return self.async_abort(reason=result)
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA, errors=errors,
        )
