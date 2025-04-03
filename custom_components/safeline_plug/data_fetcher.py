'''数据处理模块'''
import aiohttp
from .const import  API_TIMEOUT

class SafelineData:
    '''雷池数据集'''
    def __init__(self, host, token):
        self.host = host.rstrip("/")
        self.token = token
        self._data = {}
        self._api = SafelineAPI(self.host,self.token)

    async def _get_safeline_qps(self):
        raw_data = await self._api.get_data('/api/stat/qps')
        qpslist = raw_data.get("data", {}).get("nodes", [])
        qps = 0
        if "0.0.0.0:0" in qpslist[-1]:
            qps = qpslist[-1]["0.0.0.0:0"]
        self._data['qps'] = qps

    async def _get_safeline_today_attack(self):
        raw_data = await self._api.get_data('/api/stat/basic/attack')
        attack_data = raw_data.get("data", {})
        self._data['attack_ip'] = attack_data.get('attack_ip',0)
        intercept_data = attack_data.get('intercept',{})
        intercept = 0
        for key in intercept_data:
            intercept += intercept_data.get(key,0)
        self._data['intercept'] = intercept

    async def _get_safeline_today_access(self):
        raw_data = await self._api.get_data('/api/dashboard/user/counts')
        access_data = raw_data.get("data", {})
        self._data['today_pv'] = access_data.get("today_pv",0)
        self._data['today_uv'] = access_data.get("today_uv",0)
        self._data['today_ip'] = access_data.get("today_ip",0)

    async def _get_safeline_today_error_status(self):
        raw_data = await self._api.get_data('/api/stat/basic/error_status_code')
        error_data = raw_data.get("data", {})
        self._data['error_4xx'] = error_data.get("error_4xx",0)
        self._data['error_5xx'] = error_data.get("error_5xx",0)

    async def _get_safeline_24h_attack(self):
        raw_data = await self._api.get_data('/api/stat/advance/attack')
        attack_data = raw_data.get("data", {})
        self._data['attack_ip24'] = attack_data.get('attack_ip24',0)
        intercept_data = attack_data.get('intercept',{})
        intercept24 = 0
        for key in intercept_data:
            intercept24 += intercept_data.get(key,0)
        self._data['intercept24'] = intercept24

    async def _get_safeline_24h_access(self):
        raw_data = await self._api.get_data('/api/stat/advance/access')
        access_data = raw_data.get("data", {})
        self._data['pv24'] = access_data.get("access",0)
        self._data['uv24'] = access_data.get("session",0)
        self._data['ip24'] = access_data.get("ip",0)

    async def _get_safeline_24h_error_status(self):
        raw_data = await self._api.get_data('/api/stat/advance/error_status_code')
        error_data = raw_data.get("data", {})
        self._data['error_4xx24'] = error_data.get("error_4xx",0)
        self._data['error_5xx24'] = error_data.get("error_5xx",0)

    async def get_data(self):
        '''返回所有数据'''
        await self._get_safeline_qps()
        # 今日数据统计
        await self._get_safeline_today_attack()
        await self._get_safeline_today_access()
        await self._get_safeline_today_error_status()
        # 近24h数据统计
        await self._get_safeline_24h_attack()
        await self._get_safeline_24h_access()
        await self._get_safeline_24h_error_status()
        return self._data

    async def get_qps_data(self):
        '''更新qps数据'''
        await self._get_safeline_qps()
        return self._data

    async def get_other_data(self):
        '''更新其他数据'''
        # 今日数据统计
        await self._get_safeline_today_attack()
        await self._get_safeline_today_access()
        await self._get_safeline_today_error_status()
        # 近24h数据统计
        await self._get_safeline_24h_attack()
        await self._get_safeline_24h_access()
        await self._get_safeline_24h_error_status()
        return self._data

class SafelineAPI:
    '''基于雷池认证方式的API请求类'''
    def __init__(self, host, token):
        self.host = host.rstrip("/")
        self.token = token

    async def get_data(self, endpoint):
        '''发送 GET 请求'''
        url = f"{self.host}{endpoint}"
        headers = {"X-SLCE-API-TOKEN": self.token}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=API_TIMEOUT) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def post_data(self, endpoint, data):
        '''发送 POST 请求'''
        url = f"{self.host}{endpoint}"
        headers = {"X-SLCE-API-TOKEN": self.token}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data, timeout=API_TIMEOUT) as resp:
                resp.raise_for_status()
                return await resp.json()
