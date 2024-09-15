from flask import Flask, request, jsonify, session
import logging
from HubSpotAPI import HubSpotAPI, get_access_token

class HubSpotApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = '10102002'
        logging.basicConfig(filename='app.log', level=logging.INFO)  # logging setup
        self.setup_routes()  # routes setup

    # token auto-refreshment method
    def ensure_token(self):
        if 'access_token' not in session:
            refresh_token = "f24f7c51-0f0c-4d2f-babc-7d98f24a0774"
            client_id = "c481c770-d8f4-42b5-955d-a8dbf332e5e2"
            client_secret = "d763e8c5-71d6-436e-8fbd-0bb4dbbd04d3"
            token = get_access_token(refresh_token, client_id, client_secret)
            if token:
                session['access_token'] = token
            else:
                return None
        return session['access_token']

    # routes setup method
    def setup_routes(self):
        @self.app.route('/echo', methods=['POST'])
        def echo():
            data = request.get_json()
            print("data received:", data)
            logging.info(f"Echo request: {data}")
            return jsonify(data), 200

        @self.app.route('/create_contact', methods=['POST'])
        def create_contact_route():
            token = self.ensure_token()  #check and refresh token
            if token is None:
                return jsonify({"error": "Token could not be retrieved"}), 401

            api = HubSpotAPI(token)
            contact_data = request.get_json()  #getting data from body (request)
            result = api.create_contact(contact_data)

            if result:
                return jsonify(result), 201
            else:
                return jsonify({"error": "Contact not created"}), 400

        @self.app.route('/search_contact', methods=['POST'])
        def search_contact_route():
            token = self.ensure_token()  #check for token
            if token is None:
                return jsonify({"error": "Token could not be retrieved"}), 401

            api = HubSpotAPI(token)
            filters = request.get_json()  #getting filters from body

            if not filters:
                return jsonify({"error": "No filters provided"}), 400

            result = api.search_contact(filters)
            return jsonify(result), 200

        @self.app.route('/get_deal/<deal_id>', methods=['GET'])
        def get_deal_route(deal_id):
            token = self.ensure_token()  #token check
            if token is None:
                return jsonify({"error": "Token could not be retrieved"}), 401

            api = HubSpotAPI(token)
            result = api.get_deal(deal_id)
            return jsonify(result), 200

        @self.app.route('/contacts', methods=['GET'])
        def contact_list():
            token = self.ensure_token()
            if token is None:
                return jsonify({'erroe': 'Token could not be retrieved'}), 401

            api = HubSpotAPI(token)
            result = api.get_contact()
            return jsonify(result), 200

    # initializing app method
    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

#initializing app
if __name__ == "__main__":
    app = HubSpotApp()
    app.run()

