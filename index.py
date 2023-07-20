import os
import express
from pathlib import Path
import axios
from dotenv import load_dotenv
import webbrowser

from oauth import get_access_token
from config import PAYPAL_API_BASE

app = express()
load_dotenv()

port = int(os.environ.get("PORT", 8080))

app.use(express.static(Path(__file__).resolve().parent.parent / "client"))
app.use(express.json())

@app.get("/")
def home(req, res):
    res.sendFile(Path(__file__).resolve().parent.parent / "client" / "index.html")

@app.post("/capture/<string:orderId>")
async def capture_order(req, res, orderId):
    access_token = await get_access_token()

    response = await axios.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders/{orderId}/capture",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )

    print("💰 Payment captured!")
    res.json(response.data)

@app.post("/webhook")
async def webhook(req, res):
    access_token = await get_access_token()

    event_type = req.body.get("event_type")
    resource = req.body.get("resource")
    orderId = resource["id"]

    print("🪝 Received Webhook Event")

    # verify the webhook signature
    try:
        response = await axios.post(
            f"{PAYPAL_API_BASE}/v1/notifications/verify-webhook-signature",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            data={
                "transmission_id": req.headers["paypal-transmission-id"],
                "transmission_time": req.headers["paypal-transmission-time"],
                "cert_url": req.headers["paypal-cert-url"],
                "auth_algo": req.headers["paypal-auth-algo"],
                "transmission_sig": req.headers["paypal-transmission-sig"],
                "webhook_id": WEBHOOK_ID,
                "webhook_event": req.body
            }
        )

        verification_status = response.data["verification_status"]

        if verification_status != "SUCCESS":
            print("⚠️  Webhook signature verification failed.")
            return res.sendStatus(400)
    except Exception as err:
        print("⚠️  Webhook signature verification failed.")
        return res.sendStatus(400)

    # capture the order
    if event_type == "CHECKOUT.ORDER.APPROVED":
        try:
            response = await axios.post(
                f"{PAYPAL_API_BASE}/v2/checkout/orders/{orderId}/capture",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
            )

            print("💰 Payment captured!")
        except Exception as err:
            print("❌ Payment failed.")
            return res.sendStatus(400)

    res.sendStatus(200)

app.listen(port, async () => {
    webbrowser.open(f"http://localhost:{port}")
    print(f"Example app listening at http://localhost:{port}")
})
