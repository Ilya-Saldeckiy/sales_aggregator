import httpx
import time
from fastapi import HTTPException
from config import settings

class CurrencyService:
    def __init__(self):
        self.cache = None
        self.last_update = 0
        self.url = settings.currency_api_url

    async def get_usd_rate(self):
        if self.cache and (time.time() - self.last_update < 3600):
            return self.cache
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url)
                if response.status_code != 200:
                    raise HTTPException(status_code=503, detail="API ЦБ РФ недоступен")
                data = response.json()
                rate = data["Valute"]["USD"]["Value"]
                self.cache = rate
                self.last_update = time.time()
                return rate
        except Exception:
            raise HTTPException(status_code=503, detail="Ошибка при получении курса валют")

currency_service = CurrencyService()