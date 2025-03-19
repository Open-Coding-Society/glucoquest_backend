from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Endpoint to save search queries
@app.route('/saveSearch', methods=['POST'])
def save_search():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'message': 'Query is required'}), 400

    # Append query to searches.txt
    try:
        with open('searches.txt', 'a') as file:
            log_entry = f"{datetime.now().isoformat()} - {query}\n"
            file.write(log_entry)
            print("entry:",log_entry)
        return jsonify({'message': 'Search query saved successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error saving search query', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4887, debug=True)
