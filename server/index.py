import os
import json
import requests
from flask import Flask, request, send_from_directory
from dotenv import load_dotenv
import webbrowser

from oauth import get_access_token
from config import PAYPAL_API_BASE

app = Flask(__name__, static_folder='staticfiles')

port = int(os.getenv("PORT", 8082))

@app.route("/")
def index():
    return send_from_directory("../client/", "index.html")

@app.route("/capture/<order_id>", methods=["POST"])
def capture(order_id):
    access_token = get_access_token()["access_token"]
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    url = f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture"
    
    response = requests.post(url, headers=headers)
    data = response.json()

    print("💰 Payment captured!")
    return json.dumps(data)

@app.route("/webhook", methods=["POST"])
def webhook():
    access_token = get_access_token()["access_token"]
    
    event_type = request.json["event_type"]
    resource = request.json["resource"]
    order_id = resource["id"]
    
    print("🪝 Received Webhook Event")
    
    # Verify the webhook signature
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        payload = {
            "transmission_id": request.headers["paypal-transmission-id"],
            "transmission_time": request.headers["paypal-transmission-time"],
            "cert_url": request.headers["paypal-cert-url"],
            "auth_algo": request.headers["paypal-auth-algo"],
            "transmission_sig": request.headers["paypal-transmission-sig"],
            "webhook_id": WEBHOOK_ID,
            "webhook_event": request.json
        }
        
        url = f"{PAYPAL_API_BASE}/v1/notifications/verify-webhook-signature"
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        
        verification_status = data["verification_status"]
        
        if verification_status != "SUCCESS":
            print("⚠️  Webhook signature verification failed.")
            return "", 400
    except Exception as err:
        print("⚠️  Webhook signature verification failed.")
        return "", 400
    
    # Capture the order
    if event_type == "CHECKOUT.ORDER.APPROVED":
        try:
            url = f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture"
            
            response = requests.post(url, headers=headers)
            
            print("💰 Payment captured!")
        except Exception as err:
            print("❌ Payment failed.")
            return "", 400
    
    return "", 200

if __name__ == "__main__":
    load_dotenv()
    webbrowser.open_new_tab(f"http://localhost:{port}")
    app.run(port=port)