from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import requests

app = Flask(__name__)

@app.route('/api/classify')
def classify():

    #Add CORS headers to responses
    def make_response(data, status):
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = status
        return response

    #Define variables and validate
    name = request.args.get('name')
    
    if name is None or name == '':
        return make_response({'status': 'error', 'message': 'Missing or empty name parameter'}, 400)
    
    if not isinstance(name, str):
        return make_response({'status': 'error', 'message': 'Name must be a string'}, 422)
    
    #Genderize API call
    try:
        api_response = requests.get(f'https://api.genderize.io/?name={name}')
        api_response.raise_for_status()
        api_data = api_response.json()
    except Exception as e:
        return make_response({'status': 'error', 'message': str(e)}, 500)
    
    #Handle count = 0 and gender is None
    if api_data.get('count') == 0 and api_data.get('gender') is None:
        return make_response({'status': 'error', 'message': 'No prediction available for the provided name'}, 200)
    
    #Process and return data
    processed_data = {
        'name': api_data.get('name'),
        'gender': api_data.get('gender'),
        'probability': api_data.get('probability'),
        'sample_size': api_data.get('count'),
        'is_confident': api_data.get('probability') >= 0.7 and api_data.get('count') >= 100,
        'processed_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    
    return make_response({'status': 'success', 'data': processed_data}, 200)

if __name__ == '__main__':
    app.run(debug=True)
