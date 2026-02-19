import logging
from typing import Dict, Any
import aiohttp
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APITrafficMonitor:
    def __init__(self, endpoint: str, interval: int = 60):
        self.endpoint = endpoint
        self.interval = interval
        self.session = aiohttp.ClientSession()
        
    async def monitor_traffic(self) -> Dict[str, Any]:
        try:
            logger.info("Starting API traffic monitoring...")
            while True:
                await self._capture_request()
                await asyncio.sleep(self.interval)
        except Exception as e:
            logger.error(f"Monitoring failed: {str(e)}")
            raise

    async def _capture_request(self) -> None:
        try:
            async with self.session.get(self.endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Traffic captured: {data}")
                else:
                    logger.warning(f"API responded with status {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Connection error: {str(e)}")