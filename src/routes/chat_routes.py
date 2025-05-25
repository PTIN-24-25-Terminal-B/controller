from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from handlers.web import web_actions
from socket_manager import get_manager
import json

router = APIRouter(prefix="/chat", tags=["Chat"])

manager = get_manager()

class ChatRequest(BaseModel):
    client_id: str
    origin: tuple[int, int]
    destination: tuple[int, int]

    def __str__(self):
        return json.dumps(self.model_dump(mode="json"), indent=2)

@router.post("/")
async def request_car(request: ChatRequest):

    params: dict[str, str] = {
        "origin": request.origin,
        "destination": request.destination
    }

    print(request)

    web_socket: WebSocket = manager["web"][request.client_id]

    if (not isinstance(web_socket, WebSocket)):
        raise "user not connected"

    return web_actions[request_car](request.client_id, web_socket, params, manager)