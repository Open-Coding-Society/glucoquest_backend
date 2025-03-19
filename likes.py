from talk import receive_data

print(receive_data())
from flask import Flask, request, jsonify

app = Flask(__name__)

# Route to handle likes data
@app.route('/api/likes-data', methods=['POST'])
def receive_likes_data():
    # Get JSON data from the request
    likes_data = request.get_json()

    # Validate the received data
    if not likes_data or not isinstance(likes_data, dict):
        return jsonify(success=False, message="Invalid likes data"), 400

    # Log the received data for debugging
    print("Received Likes Data:", likes_data)

    # Respond with success
    return jsonify(success=True, message="Likes data received successfully"), 200

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

# Route to handle likes data
@app.route('/api/likes-data', methods=['POST'])
def receive_likes_data():
    # Get JSON data from the request
    likes_data = request.get_json()

    # Validate the received data
    if not likes_data or not isinstance(likes_data, dict):
        return jsonify(success=False, message="Invalid likes data"), 400

    # Log the received data for debugging
    print("Received Likes Data:", likes_data)

    # Respond with success
    return jsonify(success=True, message="Likes data received successfully"), 200

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
