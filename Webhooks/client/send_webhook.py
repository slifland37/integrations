# Useful for understanding why module imports don't get resolved
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# for p in sys.path:
#     print(p)

import requests
from models.payload import WebhookPayload

URL = "http://localhost:8000/webhook"
def send_webhook_request():

    payload = WebhookPayload(event="test_event", data={'message': 'hello from script'})
    response = requests.post(
        url=URL,
        json=payload.model_dump()
    )
    response_payload = response.json()
    print("status: ", response.status_code)
    print("data: ", response_payload['data'])

if __name__ == "__main__":
    send_webhook_request()