import axios
from config import PAYPAL_API_BASE, CLIENT_ID, CLIENT_SECRET

async def get_access_token():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8").decode("base64")

    response = await axios.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data="grant_type=client_credentials"
    )

    return response.data

