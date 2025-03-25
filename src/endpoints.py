from flask import Flask
from flask import request
from flask import jsonify
import kapo

app = Flask(__name__)


@app.route('/messages', methods=['POST'])
def send_message():
    """
    Send a message to the database
    """

    # Get the message data from the request
    data = request.get_json()
    webmaster_id = data['webmaster_id']
    sender_id = data['sender_id']
    sender_name = data['sender_name']
    recipient_id = data['recipient_id']
    recipient_name = data['recipient_name']
    message = data['message']
    timestamp = data['timestamp']

    # Post the message to the database
    kapo.post_private_message(webmaster_id, sender_id, sender_name, recipient_id, recipient_name, message, timestamp)

    return jsonify({'status': 'success'})


@app.route('/dms', methods=['GET'])
def get_dms():
    """
    Get all direct messages for a given pair of users
    """
    
    sender_id = request.args.get('sender_id')
    recipient_id = request.args.get('recipient_id')
    last_message_id = request.args.get('last_message_id')

    messages = kapo.get_dms(sender_id, recipient_id, last_message_id)

    return jsonify(messages)


def register_endpoints(app):
    app.add_url_rule('/messages', 'send_message', send_message, methods=['POST', 'GET'])
    app.add_url_rule('/dms', 'get_dms', get_dms, methods=['GET'])