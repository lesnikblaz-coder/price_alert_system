from fastapi import WebSocket

from app.logging_config import logger


class ConnectionManager:
    def __init__(self):
        # user_id -> WebSocket - keep track of who's currently connected
        self._connected: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connected[user_id] = websocket
        logger.info("WebSocket connected | user_id=%s", user_id)

    def disconnect(self, user_id: str) -> None:
        self._connected.pop(user_id, None)
        logger.info("WebSocket disconnected | user_id=%s", user_id)

    def is_connected(self, user_id: str) -> bool:
        return user_id in self._connected

# single shared instance
manager = ConnectionManager()