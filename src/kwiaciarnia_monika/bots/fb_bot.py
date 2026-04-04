from this import d
import fastapi
from fastapi import Query
from fastapi.responses import Response
import os
from dotenv import load_dotenv

load_dotenv()

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/webhook")
def webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge"),
):
    if mode == "subscribe" and token == os.getenv("FB_VERIFY_TOKEN"):
        print(f"DEBUG - Od FB: '{token}', Z pliku ENV: '{os.getenv('FB_TOKEN')}'")
        return Response(content=challenge, status_code=200)
    return Response(content="Invalid verification", status_code=403)


@app.post("/webhook")
def webhook_post(sender_info: dict):
    print(sender_info)
    return Response(content="OK", status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
