"""雷池集成"""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置 Safeline 集成的入口点。"""
    hass.data.setdefault(DOMAIN, {})

    # 正确的方式是使用 async_forward_entry_setups
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    _LOGGER.info("Safeline 集成已成功加载")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载 Safeline 集成的入口点。"""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])

