"""雷池集成"""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from .data_coordinator import SafelineDataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置 Safeline 集成的入口点。"""
    hass.data.setdefault(DOMAIN, {})
    coordinator = SafelineDataUpdateCoordinator(hass,entry.data)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator
    }
    hass.loop.create_task(coordinator.async_start())
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    _LOGGER.info("Safeline 集成已成功加载")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载 Safeline 集成的入口点。"""
    hass.data[DOMAIN][entry.entry_id]["coordinator"].async_stop()
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
