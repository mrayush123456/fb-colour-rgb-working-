from flask import Flask, request, redirect, url_for
import requests
import time
import re
from requests.exceptions import RequestException

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Comment Sender</title>
        <style>
            body {
                background-color: #282c34;
                color: #ffffff;
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: #3b3f46;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            }
            input, textarea, button {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: none;
                outline: none;
            }
            button {
                background-color: #4caf50;
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
            <h1>Facebook Comment Sender</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="cookies">Facebook Cookies:</label>
                <textarea id="cookies" name="cookies" rows="4" placeholder="Paste your Facebook cookies here..." required></textarea>
                
                <label for="postLink">Facebook Post Link:</label>
                <input type="text" id="postLink" name="postLink" placeholder="Enter Facebook post link" required>
                
                <label for="commenterName">Commenter's Name:</label>
                <input type="text" id="commenterName" name="commenterName" placeholder="Enter the commenter's name" required>
                
                <label for="commentFile">Comment File (TXT):</label>
                <input type="file" id="commentFile" name="commentFile" accept=".txt" required>
                
                <label for="delay">Delay (seconds):</label>
                <input type="number" id="delay" name="delay" value="5" min="1" required>
                
                <button type="submit">Start Commenting</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_comments():
    # Retrieve user input
    cookies = request.form['cookies']
    post_link = request.form['postLink']
    commenter_name = request.form['commenterName']
    delay = int(request.form['delay'])
    comment_file = request.files['commentFile']

    # Parse comments from the uploaded file
    comments = comment_file.read().decode().splitlines()
    
    # Extract target ID from the post link
    target_id = re.search(r'target_id=(\d+)', post_link)
    if not target_id:
        return "Invalid Facebook post link. Please check and try again."
    target_id = target_id.group(1)

    # Simulate cookies dictionary
    cookies_dict = {'Cookie': cookies}

    # Simulate user agent headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]'
    }

    success_count = 0
    failure_count = 0

    # Send comments one by one
    for i, comment in enumerate(comments):
        full_comment = f"{commenter_name}: {comment}"
        data = {'message': full_comment}

        try:
            # Send comment
            response = requests.post(
                f"https://graph.facebook.com/{target_id}/comments/",
                headers=headers,
                cookies=cookies_dict,
                data=data
            )
            if response.status_code == 200:
                success_count += 1
                print(f"[{i + 1}/{len(comments)}] Comment sent successfully: {full_comment}")
            else:
                failure_count += 1
                print(f"[{i + 1}/{len(comments)}] Failed to send comment: {response.status_code} {response.text}")

        except RequestException as e:
            failure_count += 1
            print(f"[{i + 1}/{len(comments)}] Error: {e}")

        # Delay between comments
        time.sleep(delay)

    # Summary of results
    return f"Comments sent: {success_count}, Failed: {failure_count}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
