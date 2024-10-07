import requests
import logging

BASE_URL = 'https://api.hubapi.com'

class HubSpotAPI:
    def __init__(self, refresh_token, client_id, client_secret, api_key=None):
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        self.token = None
        self.session = requests.Session()

        if self.api_key:
            self.session.headers.update({
                "X-API-KEY": self.api_key
            })

    def get_access_token(self):
        url = f'{BASE_URL}/oauth/v1/token'
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get("access_token")
            self.update_session_headers()
            logging.info("Access token successfully obtained.")
            return self.token
        else:
            logging.error(f"Error obtaining access token: {response.status_code}, {response.text}")
            raise Exception(f"Failed to get access token: {response.status_code}")

    def update_session_headers(self):
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })

    def make_request(self, method, url, **kwargs):
        #if token is expired, we get 401, we refresh it
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:
            logging.info("Token expired or unauthorized, refreshing token...")
            self.get_access_token()
            response = self.session.request(method, url, **kwargs)  # repeating request with new token

        return response

    def handle_errors(self, response):

        if response.status_code >= 400:
            error_message = response.json().get('message', 'Unknown error occurred')
            logging.error(f"Error {response.status_code}: {error_message}")
            return {"error": response.status_code, "message": error_message}
        return response.json()

    def create_contact(self, contact_data):
        url = f'{BASE_URL}/crm/v3/objects/contacts'
        response = self.make_request('POST', url, json=contact_data)
        return self.handle_errors(response)

    def get_contact(self, contact_id):
        url = f'{BASE_URL}/crm/v3/objects/contacts/{contact_id}'
        response = self.make_request('GET', url)
        return self.handle_errors(response)

    def update_contact(self, contact_id, contact_data):
        url = f'{BASE_URL}/crm/v3/objects/contacts/{contact_id}'
        response = self.make_request('PATCH', url, json=contact_data)
        return self.handle_errors(response)

    def delete_contact(self, contact_id):
        url = f'{BASE_URL}/crm/v3/objects/contacts/{contact_id}'
        response = self.make_request('DELETE', url)
        return self.handle_errors(response)

    def search_contact(self, filters):
        url = f'{BASE_URL}/crm/v3/objects/contacts/search'
        response = self.make_request('POST', url, json=filters)
        return self.handle_errors(response)

