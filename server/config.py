import os

NODE_ENV = os.getenv("NODE_ENV")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

is_prod = NODE_ENV == "production"

PAYPAL_API_BASE = "https://api.paypal.com" if is_prod else "https://api.sandbox.paypal.com"
