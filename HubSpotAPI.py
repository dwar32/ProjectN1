import requests
import logging

BASE_URL = 'https://api.hubapi.com'

def get_access_token(refresh_token, client_id, client_secret):
    url = f'{BASE_URL}/oauth/v1/token'
    rtoken = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=rtoken)

    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        logging.error(f"Error: {response.status_code}, {response.text}")
        return None

class HubSpotAPI:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_contact(self, contact_data):
        url = f'{BASE_URL}/crm/v3/objects/contacts'
        headers = self.get_headers()
        response = requests.post(url, headers=headers, json=contact_data)
        logging.info(f"Creating contact request: {response.status_code}, {response.text}")

        if response.status_code == 201:
            return response.json()
        elif response.status_code == 409:
            logging.info("Contact already exists")
            return "Contact already exists"
        else:
            logging.error(f"Error: {response.status_code}, {response.text}")
            return None

    def search_contact(self, filters):
        url = f'{BASE_URL}/crm/v3/objects/contacts/search'
        headers = self.get_headers()

        response = requests.post(url, headers=headers, json=filters)
        logging.info(f"Search request: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error: {response.status_code}, {response.text}")
            return {"error": response.status_code, "message": response.text}

    def get_deal(self, deal_id):
        url = f'{BASE_URL}/crm/v3/objects/deals/{deal_id}'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        logging.info(f"Запрос на получение сделки: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Ошибка получения сделки: {response.status_code}, {response.text}")
            return None

    def get_contact(self):
        url = f'{BASE_URL}/crm/v3/objects/contacts'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        logging.info(f"Contact list request: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error contact list: {response.status_code}, {response.text}")
            return None