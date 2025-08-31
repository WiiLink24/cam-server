import requests
from requests.auth import HTTPBasicAuth

class ShutterflyClient:
    def __init__(self, api_key, api_secret):
        self.base_url = "https://api.shutterfly.com"
        self.auth = HTTPBasicAuth(api_key, api_secret)

    def upload_photo(self, image_data, product_type="prints"):
        """Upload photo to Shutterfly for printing"""
        endpoint = f"{self.base_url}/media"
        response = requests.post(
            endpoint,
            files={"file": image_data},
            auth=self.auth,
            params={"productType": product_type}
        )
        response.raise_for_status()
        return response.json()

    def create_order(self, items):
        """Create print order with Shutterfly"""
        endpoint = f"{self.base_url}/orders"
        response = requests.post(
            endpoint,
            json={"items": items},
            auth=self.auth
        )
        response.raise_for_status()
        return response.json()
