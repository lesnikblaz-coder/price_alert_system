import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from app.auth import decode_token
from app.websockets.manager import manager
from app.logging_config import logger


router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    # verify token before accepting
    try:
        user_id = str(decode_token(token))
    except Exception:
        await websocket.close(code=4001)
        return

    # accept and register
    await manager.connect(
        user_id=user_id,
        websocket=websocket
    )

    # get async redis from app.state
    async_redis: Redis = websocket.app.state.async_redis

    try:
        # subscribe to this user's personal channel
        pubsub: PubSub = async_redis.pubsub()
        await pubsub.subscribe(f"alert:user:{user_id}")

        # listen until connection closes
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = json.loads(message["data"])
            await websocket.send_json(data)
            logger.info("Alert sent | user_id=%s", user_id)

    except WebSocketDisconnect:
        pass # normal - user closed their browser tab

    except Exception as exc:
        logger.error(
            "WebSocket error | user_id=%s error=%s",
            user_id,
            exc
        )

    finally:
        # always clean up
        manager.disconnect(user_id)

        await pubsub.unsubscribe(f"alert:user:{user_id}")
        await pubsub.aclose()