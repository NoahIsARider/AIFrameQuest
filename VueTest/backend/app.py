from flask import Flask, jsonify
from flask_cors import CORS
from utils.data_utils import get_json_data
import traceback

app = Flask(__name__)
CORS(app)  # 允许所有域名访问

@app.route('/api/get-data', methods=['GET'])
def get_data():
    try:
        print("Attempting to fetch data...")
        data = get_json_data()
        print("Data fetched successfully")
        return jsonify(data)
    except Exception as e:
        error_msg = str(e)
        print(f"Error occurred: {error_msg}")
        print("Full traceback:")
        print(traceback.format_exc())
        return jsonify({
            'error': error_msg,
            'details': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)