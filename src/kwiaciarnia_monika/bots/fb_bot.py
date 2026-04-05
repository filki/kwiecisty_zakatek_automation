import fastapi
from fastapi import Query
from fastapi.responses import Response, FileResponse
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import httpx

load_dotenv()

META_URL = "https://graph.facebook.com/v25.0/me/messages"
app = fastapi.FastAPI()
httpx_client = httpx.AsyncClient()

# Znajdź folder główny projektu (3 poziomy wyżej od tego pliku)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
app.mount("/static", StaticFiles(directory=PROJECT_ROOT), name="static")


@app.get("/")
def read_root():
    return FileResponse("index.html")


@app.get("/webhook")
def webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge"),
):
    if mode == "subscribe" and token == os.getenv("FB_TOKEN"):
        return Response(content=challenge, status_code=200)
    return Response(content="Invalid verification", status_code=403)


@app.post("/webhook")
async def webhook_post(sender_info: dict):
    message = sender_info["entry"][0]["messaging"][0]["message"].get("text")
    message_clean = "" if message is None else message.lower().strip()
    sender_id = sender_info["entry"][0]["messaging"][0]["sender"]["id"]
    if not message_clean:
        return Response(content="OK", status_code=200)
    if "cześć" in message_clean:
        await _send_message(
            sender_id,
            "Witamy w pracowni florystycznej Kwiecisty Zakątek! Jestem Twoim asystentem, w czym mogę dzisiaj służyć?",
        )
        await _send_options(sender_id)
    else:
        await _send_message(sender_id, "Nie rozumiem")
    return Response(content="OK", status_code=200)


async def _send_message(sender_id: str, message: str):
    response = await httpx_client.post(
        url=META_URL,
        params={"access_token": os.getenv("FB_PAGE_ACCESS_TOKEN")},
        json={"recipient": {"id": sender_id}, "message": {"text": message}},
    )
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.text}")


async def _send_options(sender_id: str):
    response = await httpx_client.post(
        url=META_URL,
        params={"access_token": os.getenv("FB_PAGE_ACCESS_TOKEN")},
        json={
            "recipient": {"id": sender_id},
            "message": {
                "text": "Oto Twoje opcje do wyboru:",
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": "test 1",
                        "payload": "UKRYTA_WARTOSC_1",
                    },
                    {
                        "content_type": "text",
                        "title": "test 2",
                        "payload": "UKRYTA_WARTOSC_2",
                    },
                ],
            },
        },
    )
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.text}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=20846)
