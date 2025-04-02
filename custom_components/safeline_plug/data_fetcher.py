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

    def get_data(self):
        '''返回所有数据'''
        #TODO返回数据与相关函数开发
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
