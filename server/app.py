from flask import Flask, jsonify
from flask_cors import CORS
import requests

URL_BASE = 'https://inf551-b0e88.firebaseio.com/'
app = Flask(__name__)
CORS(app)

@app.route('/Daily', methods=['GET'])
def daily_release():
    url = URL_BASE + 'daily_situation.json'
    response = requests.get(url)
    json_data = response.json()
    data_array = []
    for k in json_data:
        item = json_data[k]
        item['uuid'] = k
        data_array.append(item)
    return jsonify({
        'status': 'success',
        'data': data_array,
    })


if __name__ == "__main__":
    app.run(debug=True)