from flask import Flask, request, redirect, url_for
import os
import time
import re
import requests
from requests.exceptions import RequestException

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
    <html>
    <head>
        <title>Facebook Comment Automation</title>
        <style>
    body{
      background-color: red;
    }
    .container{
      max-width: 1000px;
      background-color: bisque;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 0 10px rgba(red,green,blue,alpha);
      margin: 0 auto;
      margin-top: 20px;
    }
    .header{
      text-align: center;
      padding-bottom: 20px;
    }
    .btn-submit{
      width: 100%;
      margin-top: 10px;
    }
    .footer{
      text-align: center;
      margin-top: 20px;
      color: brown;
    }
  </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Comment Automation</h2>
            <form method="POST" action="/" enctype="multipart/form-data">
                <label for="cookiesFile">Cookies File (TXT):</label>
                <input type="file" name="cookiesFile" required>
                
                <label for="commentsFile">Comments File (TXT):</label>
                <input type="file" name="commentsFile" required>
                
                <label for="commenterName">Commenter's Name:</label>
                <input type="text" name="commenterName" placeholder="Enter commenter name" required>
                
                <label for="postId">Post ID:</label>
                <input type="text" name="postId" placeholder="Enter Facebook post ID" required>
                
                <label for="delay">Delay (seconds):</label>
                <input type="number" name="delay" value="5" min="1" required>
                
                <button type="submit">Start Commenting</button>
            </form>
            <h3>Powered by Flask & Facebook</h3>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_comments():
    try:
        cookies_file = request.files['cookiesFile']
        comments_file = request.files['commentsFile']
        commenter_name = request.form['commenterName']
        post_id = request.form['postId']
        delay = int(request.form['delay'])

        cookies_data = cookies_file.read().decode().splitlines()
        comments = comments_file.read().decode().splitlines()

        # Validate cookies and get EAAG tokens
        valid_cookies = get_valid_cookies(cookies_data)
        if not valid_cookies:
            return 'No valid cookies found. Please check the cookies file.'

        x, cookie_index = 0, 0

        while True:
            time.sleep(delay)
            comment = comments[x].strip()
            current_cookie, token_eaag = valid_cookies[cookie_index]

            response = post_comment(post_id, commenter_name, comment, current_cookie, token_eaag)
            if response and response.status_code == 200:
                print(f'Successfully sent comment: {commenter_name}: {comment}')
                x = (x + 1) % len(comments)
                cookie_index = (cookie_index + 1) % len(valid_cookies)
            else:
                print(f'Failed to send comment: {commenter_name}: {comment}')
                cookie_index = (cookie_index + 1) % len(valid_cookies)

    except Exception as e:
        print(f'[!] An unexpected error occurred: {e}')
        return f"Error: {str(e)}"
    
    return redirect(url_for('index'))

def get_valid_cookies(cookies_data):
    valid_cookies = []
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 '
            'Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]'
        )
    }

    for cookie in cookies_data:
        response = make_request('https://business.facebook.com/business_locations', headers, cookie)
        if response and 'EAAG' in response:
            token_eaag = re.search(r'(EAAG\w+)', response)
            if token_eaag:
                valid_cookies.append((cookie, token_eaag.group(1)))
    return valid_cookies

def make_request(url, headers, cookie):
    try:
        response = requests.get(url, headers=headers, cookies={'Cookie': cookie})
        return response.text
    except RequestException as e:
        print(f'[!] Error making request: {e}')
        return None

def post_comment(post_id, commenter_name, comment, cookie, token_eaag):
    data = {'message': f'{commenter_name}: {comment}', 'access_token': token_eaag}
    try:
        response = requests.post(
            f'https://graph.facebook.com/{post_id}/comments/',
            data=data,
            cookies={'Cookie': cookie}
        )
        return response
    except RequestException as e:
        print(f'[!] Error posting comment: {e}')
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
