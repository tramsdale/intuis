"""Config flow for IntuisNetatmo integration."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from intuis_netatmo import IntuisNetatmo

_LOGGER = logging.getLogger(__name__)

DOMAIN = "intuis_netatmo"

class IntuisNetatmoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IntuisNetatmo."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Try to create client and authenticate
                client = IntuisNetatmo(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    client_id=user_input[CONF_CLIENT_ID],
                    client_secret=user_input[CONF_CLIENT_SECRET],
                )
                client.pull_data()

                # If successful, create the config entry
                return self.async_create_entry(
                    title="IntuisNetatmo",
                    data=user_input,
                )
            except Exception as err:
                _LOGGER.error("Error during setup: %s", err)
                errors["base"] = "cannot_connect"

        # Show the form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_CLIENT_SECRET): str,
            }),
            errors=errors,
        ) 