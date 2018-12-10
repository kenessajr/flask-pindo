from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
import json


app = Flask(__name__)


class Config:
    BASE_URL = 'http://178.128.165.87'


class Send(Config):
    def __init__(self, token, to, text, sender='Pindo'):
        self.token = token
        self.to = to
        self.text = text 
        self.sender = sender
        self.url = '{}/sms/'.format(Config.BASE_URL)

    def sms(self):
        payload = {
            'to': self.to,
            'text': self.text,
            'sender': self.sender
        }
        r = requests.post(
            self.url,
            auth=HTTPBasicAuth(self.token, ''),
            json=payload
        )
        return r.json()


@app.route('/')
def ping():
    return jsonify(
        {
            'status': 200,
            'message': 'success',
            'payload': 'ping'
        }
    )

# new
from . import Send
@app.route('/send', methods=['POST'])
def sms():
    data = request.get_json()
    send = Send(data['token'], data['to'], data['text'], data['sender']).sms()
    return jsonify(send)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

