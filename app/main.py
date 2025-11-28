from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_change_in_production'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for connected users
# Format: { socket_id: { public_key: JWK_Object, joined_at: timestamp } }
users = {}

# Ensure logs directory exists
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'encrypted_chat.json')

def log_encrypted_message(sender_id, encrypted_packages):
    """
    Simulates storing the encrypted blob in a database.
    The server CANNOT read these messages.
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "sender": sender_id,
        "payload": encrypted_packages # This is the ciphertext
    }
    
    # Append to JSON file
    try:
        data = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        
        data.append(entry)
        
        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"🔒 [Server Log] Encrypted message from {sender_id} stored.")
    except Exception as e:
        print(f"Error logging: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]
        # Broadcast updated user list to everyone
        emit('user_list', users, broadcast=True)
    print(f"Client disconnected: {request.sid}")

@socketio.on('join')
def handle_join(data):
    """
    When a user joins, they send their RSA Public Key.
    We store it and broadcast the new list of users so clients can encrypt for each other.
    """
    public_key = data.get('publicKey')
    
    if public_key:
        users[request.sid] = public_key
        # Send the current list of users (and their keys) to EVERYONE
        # This allows Client A to get Client B's public key
        emit('user_list', users, broadcast=True)
        print(f"🔑 Key Exchange: User {request.sid} registered public key.")

@socketio.on('send_message')
def handle_message(data):
    """
    Relay the encrypted message packages to recipients.
    data structure:
    {
        'packages': { 'recipient_socket_id': { 'iv':..., 'content':..., 'encryptedKey':... } },
        'plaintext_preview': '...' (Optional, for sender's UI only, not stored securely)
    }
    """
    sender_id = request.sid
    packages = data.get('packages', {})
    
    # Store the encrypted log
    log_encrypted_message(sender_id, packages)
    
    # Broadcast to all clients. 
    # Clients will check if there is a package meant for them in the data.
    emit('receive_message', {
        'sender_id': sender_id,
        'packages': packages,
        'plaintext_preview': data.get('plaintext_preview') # Only for the sender UX
    }, broadcast=True)

if __name__ == '__main__':
    print("🚀 Starting Secure Chat Server...")
    socketio.run(app, debug=True, port=5000)
4
