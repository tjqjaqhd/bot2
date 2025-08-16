"""웹소켓 클라이언트 스텁"""
import asyncio
from typing import AsyncIterator, List


class WSClient:
    def __init__(self, messages: List[str]):
        self.messages = messages

    async def __aiter__(self) -> AsyncIterator[str]:
        for msg in self.messages:
            await asyncio.sleep(0)
            yield msg
