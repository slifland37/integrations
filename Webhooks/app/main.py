from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from models.payload import WebhookPayload

app = FastAPI()


@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    print("Payload: ", payload.model_dump())

    return JSONResponse(
        content={"status": "ok", "data": "received request"},
        status_code=status.HTTP_200_OK,
    )
