"""雷池集成配置流程"""
import voluptuous as vol
import logging
from homeassistant import config_entries
from .const import DOMAIN, API_TOKEN

class LeichiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return await self.async_step_home()
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(API_TOKEN): str,
                }
            ),
            description_placeholders={
                "apitoken_hint": "雷池API密钥",
            },
            errors=errors,
        )