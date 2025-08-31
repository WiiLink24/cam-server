import requests

class PhotoboxClient:
    def __init__(self, client_id, client_secret):
        self.base_url = "https://api.photobox.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self._get_access_token()

    def _get_access_token(self):
        """Get OAuth2 access token"""
        auth_url = f"{self.base_url}/oauth/token"
        response = requests.post(
            auth_url,
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"}
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def upload_image(self, image_data):
        """Upload image to Photobox"""
        endpoint = f"{self.base_url}/v1/media"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            endpoint,
            files={"file": image_data},
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    def create_order(self, product_id, image_id, quantity=1):
        """Create print order with Photobox"""
        endpoint = f"{self.base_url}/v1/orders"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "items": [{
                "productId": product_id,
                "imageId": image_id,
                "quantity": quantity
            }]
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
