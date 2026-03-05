"""Config flow for Lexent Polperro integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from polperro import PolperroClient  # type: ignore[attr-defined]

from .const import CONF_HOST, CONF_MAC, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PolperroConfigFlow(ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """Handle a config flow for Lexent Polperro."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step: enter device IP."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            client = PolperroClient(host=host)

            try:
                await client.connect()
                await client.get_state()
                mac = client.mac
                await client.disconnect()
            except Exception:
                _LOGGER.exception("Failed to connect to Polperro device at %s", host)
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(mac)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Polperro ({host})",
                    data={
                        CONF_HOST: host,
                        CONF_MAC: mac,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
        )
