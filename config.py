import os

NODE_ENV = os.environ.get("NODE_ENV")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

isProd = NODE_ENV == "development"

PAYPAL_API_BASE = "https://api.paypal.com" if isProd else "https://api.sandbox.paypal.com"
