import asyncio
import websockets
import structlog

log = structlog.get_logger(__name__)


class WSClient:
    """단순 재접속 웹소켓 클라이언트."""

    def __init__(self, url: str):
        self.url = url
        self._stop = False

    async def connect(self):
        while not self._stop:
            try:
                async with websockets.connect(self.url) as ws:
                    await self.handle(ws)
            except Exception as e:  # pragma: no cover - 단순 로깅
                log.warning("ws reconnect", error=str(e))
                await asyncio.sleep(1)

    async def handle(self, ws):  # pragma: no cover - 외부 구현
        async for msg in ws:
            log.info("ws_message", msg=msg)

    def stop(self):
        self._stop = True
