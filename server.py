import hashlib
import hmac
import os

import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

WEBHOOK_SECRET_SPLITTER = os.getenv('WEBHOOK_SECRET_SPLITTER')
WEBHOOK_SECRETS = os.getenv('WEBHOOK_SECRETS').split(WEBHOOK_SECRET_SPLITTER)
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

DISCORD_PURCHASE_WEBHOOK_CONTENT = os.getenv('DISCORD_PURCHASE_WEBHOOK_CONTENT')
DISCORD_REFUND_WEBHOOK_CONTENT = os.getenv('DISCORD_REFUND_WEBHOOK_CONTENT')

BASE_API_URL = "https://api.polymart.org/v1/"

app = Flask(__name__)


def verify_signature(secret, data, signature):
    computed_signature = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, signature)


def get_user_name(user_id):
    api_url = BASE_API_URL + "getAccountInfo"
    params = {'user_id': user_id}
    response = requests.post(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['response']['user']['username']
    else:
        print(f"Failed to get user info: {response.status_code}, {response.text}")
        return None


def get_resource_info(resource_id):
    api_url = BASE_API_URL + "getResourceInfo"
    params = {'resource_id': resource_id}
    response = requests.post(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['response']['resource']
    else:
        print(f"Failed to get resource info: {response.status_code}, {response.text}")
        return None


def send_discord_webhook(webhook_content, payload):
    try:
        user_id = payload['user']['id']
        user_name = get_user_name(user_id)

        resource_id = payload['product']['id']
        resource_info = get_resource_info(resource_id)

        resource_title = resource_info['title']
        resource_currency = resource_info['currency']
        resource_price = resource_info['price']
        resource_thumbnail_url = resource_info['thumbnailURL']

        webhook_content = (webhook_content
                           .replace("{USER_ID}", str(user_id))
                           .replace("{USER_NAME}", user_name)
                           .replace("{RESOURCE_ID}", str(resource_id))
                           .replace("{RESOURCE_TITLE}", resource_title)
                           .replace("{RESOURCE_CURRENCY}", resource_currency)
                           .replace("{RESOURCE_PRICE}", str(resource_price))
                           .replace("{RESOURCE_THUMBNAIL_URL}", resource_thumbnail_url))

        headers = {'Content-Type': 'application/json'}

        response = requests.post(DISCORD_WEBHOOK_URL, data=webhook_content, headers=headers)
        if response.status_code != 204:
            print(f"Failed to send webhook to Discord: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to send webhook to Discord: {e}")


@app.route('/', methods=['POST'])
def server():
    signature = request.headers.get('X-Polymart-Signature')
    data = request.get_data()

    for secret in WEBHOOK_SECRETS:
        if verify_signature(secret, data, signature):
            content = request.json

            event = content['event']
            payload = content['payload']

            if event == 'ping':
                print("Received ping event")

            if event == 'product.user.purchase':
                send_discord_webhook(DISCORD_PURCHASE_WEBHOOK_CONTENT, payload)

            if event == 'product.user.refund':
                send_discord_webhook(DISCORD_REFUND_WEBHOOK_CONTENT, payload)

            return jsonify({'message': 'Webhook received and verified'}), 200

    return jsonify({'message': 'Invalid signature'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
