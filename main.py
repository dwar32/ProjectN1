from flask import Flask, request, jsonify, session
import logging
from HubSpotAPI import HubSpotAPI

app = Flask(__name__)
app.secret_key = '10102002'
logging.basicConfig(filename='app.log', level=logging.INFO)


hubspot_api = HubSpotAPI(
    refresh_token="f24f7c51-0f0c-4d2f-babc-7d98f24a0774",
    client_id="c481c770-d8f4-42b5-955d-a8dbf332e5e2",
    client_secret="d763e8c5-71d6-436e-8fbd-0bb4dbbd04d3",
    api_key="your_api_key_here"
)

def ensure_token():

    if 'access_token' not in session:
        try:
            session['access_token'] = hubspot_api.get_access_token()
        except Exception as e:
            logging.error(f"Failed to get access token: {str(e)}")
            return None
    return session['access_token']

@app.route('/search_contacts', methods=['POST'])
def search_contacts():
    if not ensure_token():
        return jsonify({"error": "Token could not be retrieved"}), 401

    filters = request.get_json()
    result = hubspot_api.search_contact(filters)
    return jsonify(result), 200

@app.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if not ensure_token():
        return jsonify({"error": "Token could not be retrieved"}), 401

    if request.method == 'GET':
        filters = request.args.to_dict()
        result = hubspot_api.search_contact(filters)
        return jsonify(result), 200

    elif request.method == 'POST':
        contact_data = request.get_json()
        result = hubspot_api.create_contact(contact_data)
        if "error" in result:
            return jsonify(result), result['error']
        return jsonify(result), 201

@app.route('/contacts/<contact_id>', methods=['GET', 'PATCH', 'DELETE'])
def manage_contact(contact_id):
    if not ensure_token():
        return jsonify({"error": "Token could not be retrieved"}), 401

    if request.method == 'GET':
        result = hubspot_api.get_contact(contact_id)
        return jsonify(result), 200

    elif request.method == 'PATCH':
        contact_data = request.get_json()
        result = hubspot_api.update_contact(contact_id, contact_data)
        if "error" in result:
            return jsonify(result), result['error']
        return jsonify(result), 200

    elif request.method == 'DELETE':
        result = hubspot_api.delete_contact(contact_id)
        if "error" in result:
            return jsonify(result), result['error']
        return jsonify(result), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

