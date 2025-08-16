"""단순 웹소켓 클라이언트 래퍼."""
from __future__ import annotations
import asyncio
import websockets


class WSClient:
    def __init__(self, url: str):
        self.url = url
        self.ws = None

    async def connect(self):
        self.ws = await websockets.connect(self.url)
        return self

    async def recv(self):
        if self.ws is None:
            raise RuntimeError("not connected")
        return await self.ws.recv()

    async def close(self):
        if self.ws:
            await self.ws.close()
