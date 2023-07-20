import requests
from config import PAYPAL_API_BASE, CLIENT_ID, CLIENT_SECRET

def get_access_token():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    credentials = credentials.encode("utf-8").decode("base64")

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = "grant_type=client_credentials"

    response = requests.post(f"{PAYPAL_API_BASE}/v1/oauth2/token", headers=headers, data=payload)
    return response.json()