"""雷池集成配置流程"""
import voluptuous as vol
from homeassistant import config_entries
import aiohttp
from .const import DOMAIN, TEST_API
from .data_fetcher import SafelineAPI

class SafelineConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    '''雷池实例的配置流对象'''
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input["host"].rstrip("/")
            api_token = user_input["api_token"]

            try:
                # 格式校验
                if not host.startswith(("http://", "https://")):
                    raise vol.Invalid("invalid_host_format")
                # 连接测试
                if await self._test_connection(host, api_token):
                    # 唯一性检查
                    await self.async_set_unique_id(f"safeline_plug_{host.split('//')[1]}")
                    self._abort_if_unique_id_configured()
                    # 创建配置项
                    return self.async_create_entry(
                        title=f"雷池 ({host})",
                        data={"host": host, "api_token": api_token}
                    )
            except aiohttp.ClientResponseError as err:
                if err.status == 401:
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "api_error"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except vol.Invalid:
                errors["base"] = "invalid_host"

        # 带默认值的 Schema
        data_schema = vol.Schema({
            vol.Required("host", default="https://"): str,
            vol.Required("api_token"): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "docs_url": "https://github.com/nkdns/safeline_plug/"
            }
        )

    async def _test_connection(self, host, token):
        safelineapi = SafelineAPI(host, token)
        return await safelineapi.get_data(TEST_API)
