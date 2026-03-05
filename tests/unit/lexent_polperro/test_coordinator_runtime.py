"""Unit tests for coordinator runtime behaviour (_async_update_data, async_shutdown)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.lexent_polperro.const import CONF_HOST, CONF_MAC
from custom_components.lexent_polperro.coordinator import PolperroCoordinator
from tests.conftest import _make_device_state


def _make_coordinator(
    mock_client: MagicMock | None = None,
) -> PolperroCoordinator:
    hass = MagicMock()
    entry = MagicMock()
    entry.data = {CONF_HOST: "192.168.2.8", CONF_MAC: "502cc626e9a5"}
    entry.unique_id = "502cc626e9a5"

    with patch(
        "custom_components.lexent_polperro.coordinator.PolperroClient",
        return_value=mock_client or MagicMock(),
    ):
        return PolperroCoordinator(hass, entry)


class TestAsyncUpdateData:
    """Tests for _async_update_data."""

    @pytest.mark.asyncio
    async def test_first_call_connects_then_gets_state(self) -> None:
        """First update call connects to device and returns state."""
        state = _make_device_state()
        mock_client = AsyncMock()
        mock_client.connect = AsyncMock()
        mock_client.get_state = AsyncMock(return_value=state)

        coordinator = _make_coordinator(mock_client)
        assert coordinator._connected is False

        result = await coordinator._async_update_data()

        mock_client.connect.assert_called_once()
        mock_client.get_state.assert_called_once()
        assert coordinator._connected is True
        assert result is state

    @pytest.mark.asyncio
    async def test_subsequent_call_skips_connect(self) -> None:
        """When already connected, skip connect and just get state."""
        state = _make_device_state()
        mock_client = AsyncMock()
        mock_client.connect = AsyncMock()
        mock_client.get_state = AsyncMock(return_value=state)

        coordinator = _make_coordinator(mock_client)
        coordinator._connected = True

        result = await coordinator._async_update_data()

        mock_client.connect.assert_not_called()
        mock_client.get_state.assert_called_once()
        assert result is state

    @pytest.mark.asyncio
    async def test_connect_error_raises_update_failed(self) -> None:
        """Connection error disconnects and raises UpdateFailed."""
        mock_client = AsyncMock()
        mock_client.connect = AsyncMock(side_effect=OSError("network down"))
        mock_client.disconnect = AsyncMock()

        coordinator = _make_coordinator(mock_client)

        with pytest.raises(UpdateFailed, match="Error communicating"):
            await coordinator._async_update_data()

        assert coordinator._connected is False
        mock_client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_state_error_raises_update_failed(self) -> None:
        """get_state error disconnects and raises UpdateFailed."""
        mock_client = AsyncMock()
        mock_client.connect = AsyncMock()
        mock_client.get_state = AsyncMock(side_effect=TimeoutError("timeout"))
        mock_client.disconnect = AsyncMock()

        coordinator = _make_coordinator(mock_client)

        with pytest.raises(UpdateFailed, match="Error communicating"):
            await coordinator._async_update_data()

        assert coordinator._connected is False
        mock_client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect_error_during_cleanup_is_suppressed(self) -> None:
        """If disconnect fails during error cleanup, it's silently suppressed."""
        mock_client = AsyncMock()
        mock_client.connect = AsyncMock(side_effect=OSError("fail"))
        mock_client.disconnect = AsyncMock(side_effect=OSError("double fail"))

        coordinator = _make_coordinator(mock_client)

        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()

        assert coordinator._connected is False


class TestAsyncShutdown:
    """Tests for async_shutdown."""

    @pytest.mark.asyncio
    async def test_shutdown_disconnects_when_connected(self) -> None:
        """Shutdown disconnects client when connected."""
        mock_client = AsyncMock()
        mock_client.disconnect = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        coordinator._connected = True

        with patch.object(
            type(coordinator).__bases__[0], "async_shutdown", new_callable=AsyncMock
        ):
            await coordinator.async_shutdown()

        mock_client.disconnect.assert_called_once()
        assert coordinator._connected is False

    @pytest.mark.asyncio
    async def test_shutdown_skips_disconnect_when_not_connected(self) -> None:
        """Shutdown does not disconnect when not connected."""
        mock_client = AsyncMock()
        mock_client.disconnect = AsyncMock()

        coordinator = _make_coordinator(mock_client)
        assert coordinator._connected is False

        with patch.object(
            type(coordinator).__bases__[0], "async_shutdown", new_callable=AsyncMock
        ):
            await coordinator.async_shutdown()

        mock_client.disconnect.assert_not_called()
