from flask import Flask, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cookie to Access Token Converter</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input, button, label {
                    width: 100%;
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Convert Cookie to Access Token</h2>
                <form action="/" method="post">
                    <label for="cookie">Paste Your Facebook Cookie:</label>
                    <input type="text" id="cookie" name="cookie" placeholder="Paste your Facebook session cookie here" required>
                    <button type="submit">Get Access Token</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def convert_cookie():
    # Get the cookie from the form
    fb_cookie = request.form.get('cookie')

    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': fb_cookie
    }

    # Vinthool API endpoint for cookie to access token conversion
    url = "https://business.facebook.com/business_locations"

    try:
        # Make a POST request to get the access token
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            # Extract the access token from the response
            data = response.json()
            if 'accessToken' in data:
                access_token = data['accessToken']
                return jsonify({'access_token': access_token})
            else:
                return jsonify({'error': 'Access token not found. Check your cookie.'}), 400
        else:
            return jsonify({'error': f'Failed to get access token. Status code: {response.status_code}'}), 400

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
