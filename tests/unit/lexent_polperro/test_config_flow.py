"""Unit tests for Lexent Polperro config flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.data_entry_flow import AbortFlow

from custom_components.lexent_polperro.config_flow import PolperroConfigFlow
from custom_components.lexent_polperro.const import CONF_HOST, CONF_MAC, DOMAIN


class TestConfigFlowUserStep:
    """Tests for the user step."""

    def _make_flow(self) -> PolperroConfigFlow:
        """Create a config flow instance with mocked hass."""
        flow = PolperroConfigFlow()
        flow.hass = MagicMock()
        return flow

    @pytest.mark.asyncio
    async def test_user_step_shows_form(self) -> None:
        """User step shows IP address form."""
        flow = self._make_flow()
        result = await flow.async_step_user()
        assert result["type"] == "form"
        assert result["step_id"] == "user"

    @pytest.mark.asyncio
    async def test_user_step_success(self) -> None:
        """Successful connection creates config entry."""
        flow = self._make_flow()
        flow.async_set_unique_id = AsyncMock()
        flow._abort_if_unique_id_configured = MagicMock()
        flow.async_create_entry = MagicMock(return_value={"type": "create_entry"})

        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.connect = AsyncMock()
        mock_client.get_state = AsyncMock()
        mock_client.disconnect = AsyncMock()

        with patch(
            "custom_components.lexent_polperro.config_flow.PolperroClient",
            return_value=mock_client,
        ):
            result = await flow.async_step_user({CONF_HOST: "192.168.2.8"})

        mock_client.connect.assert_called_once()
        mock_client.get_state.assert_called_once()
        mock_client.disconnect.assert_called_once()
        flow.async_set_unique_id.assert_called_once_with("502cc626e9a5")
        flow.async_create_entry.assert_called_once()

        entry_data = flow.async_create_entry.call_args[1]["data"]
        assert entry_data[CONF_HOST] == "192.168.2.8"
        assert entry_data[CONF_MAC] == "502cc626e9a5"

    @pytest.mark.asyncio
    async def test_user_step_connection_error(self) -> None:
        """Connection failure shows error and allows retry."""
        flow = self._make_flow()

        mock_client = AsyncMock()
        mock_client.connect = AsyncMock(side_effect=Exception("timeout"))

        with patch(
            "custom_components.lexent_polperro.config_flow.PolperroClient",
            return_value=mock_client,
        ):
            result = await flow.async_step_user({CONF_HOST: "192.168.2.99"})

        assert result["type"] == "form"
        assert result["errors"]["base"] == "cannot_connect"

    @pytest.mark.asyncio
    async def test_user_step_duplicate_aborts(self) -> None:
        """Duplicate MAC aborts with already_configured."""
        flow = self._make_flow()
        flow.async_set_unique_id = AsyncMock()
        flow._abort_if_unique_id_configured = MagicMock(
            side_effect=AbortFlow("already_configured")
        )

        mock_client = AsyncMock()
        mock_client.mac = "502cc626e9a5"
        mock_client.connect = AsyncMock()
        mock_client.get_state = AsyncMock()
        mock_client.disconnect = AsyncMock()

        with (
            patch(
                "custom_components.lexent_polperro.config_flow.PolperroClient",
                return_value=mock_client,
            ),
            pytest.raises(AbortFlow, match="already_configured"),
        ):
            await flow.async_step_user({CONF_HOST: "192.168.2.8"})

    @pytest.mark.asyncio
    async def test_user_step_error_recovery(self) -> None:
        """After a connection error, user can retry and succeed."""
        flow = self._make_flow()
        flow.async_set_unique_id = AsyncMock()
        flow._abort_if_unique_id_configured = MagicMock()
        flow.async_create_entry = MagicMock(return_value={"type": "create_entry"})

        # First attempt: fail
        mock_bad = AsyncMock()
        mock_bad.connect = AsyncMock(side_effect=Exception("timeout"))

        with patch(
            "custom_components.lexent_polperro.config_flow.PolperroClient",
            return_value=mock_bad,
        ):
            result = await flow.async_step_user({CONF_HOST: "192.168.2.99"})
        assert result["errors"]["base"] == "cannot_connect"

        # Second attempt: succeed
        mock_good = AsyncMock()
        mock_good.mac = "502cc626e9a5"
        mock_good.connect = AsyncMock()
        mock_good.get_state = AsyncMock()
        mock_good.disconnect = AsyncMock()

        with patch(
            "custom_components.lexent_polperro.config_flow.PolperroClient",
            return_value=mock_good,
        ):
            await flow.async_step_user({CONF_HOST: "192.168.2.8"})
        flow.async_create_entry.assert_called_once()
