"""Config flow for Golemio integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_TOKEN

DOMAIN = "golemio"
CONF_CONTAINERID = "container_id"


class GolemioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Golemio."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_TOKEN): str,
                    vol.Required(CONF_CONTAINERID): str,
                }
            )
            return self.async_show_form(step_id="user", data_schema=data_schema)

        # Create entry with provided data
        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    @staticmethod
    def async_get_options_flow(entry: config_entries.ConfigEntry):
        return GolemioOptionsFlowHandler(entry)


class GolemioOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is None:
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_NAME, default=self.entry.data.get(CONF_NAME)): str,
                    vol.Required(CONF_TOKEN, default=self.entry.data.get(CONF_TOKEN)): str,
                    vol.Required(CONF_CONTAINERID, default=self.entry.data.get(CONF_CONTAINERID)): str,
                }
            )
            return self.async_show_form(step_id="init", data_schema=data_schema)

        return self.async_create_entry(title=self.entry.title, data=user_input)
