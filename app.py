from flask import Flask, request, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

# Headers for requests
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Management Tool</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">Facebook Management Tool</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="tokenType" class="form-label">Token Type:</label>
                    <select class="form-control" id="tokenType" name="tokenType" required>
                        <option value="single">Single Token</option>
                        <option value="multi">Multi Token</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="accessToken" class="form-label">Access Token:</label>
                    <input type="text" class="form-control" id="accessToken" name="accessToken" required>
                </div>
                <div class="mb-3">
                    <label for="threadId" class="form-label">Conversation ID:</label>
                    <input type="text" class="form-control" id="threadId" name="threadId" required>
                </div>
                <div class="mb-3">
                    <label for="kidx" class="form-label">Enter Nickname Prefix:</label>
                    <input type="text" class="form-control" id="kidx" name="kidx" required>
                </div>
                <div class="mb-3">
                    <label for="txtFile" class="form-label">Message File (TXT):</label>
                    <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
                </div>
                <div class="mb-3" id="multiTokenFile" style="display: none;">
                    <label for="tokenFile" class="form-label">Token File (for Multi-Token):</label>
                    <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
                </div>
                <div class="mb-3">
                    <label for="time" class="form-label">Delay Between Messages (Seconds):</label>
                    <input type="number" class="form-control" id="time" name="time" min="1" required>
                </div>
                <div class="mb-3">
                    <label for="lock" class="form-label">Lock Messages?</label>
                    <select class="form-control" id="lock" name="lock">
                        <option value="no">No</option>
                        <option value="yes">Yes</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def process_form():
    # Extract form data
    token_type = request.form.get('tokenType')
    access_token = request.form.get('accessToken')
    thread_id = request.form.get('threadId')
    nickname_prefix = request.form.get('kidx')
    time_interval = int(request.form.get('time'))
    lock = request.form.get('lock')

    # Handle file uploads
    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()

    tokens = []
    if token_type == 'multi':
        token_file = request.files.get('tokenFile')
        if token_file:
            tokens = token_file.read().decode().splitlines()

    # Folder to save data
    folder_name = f"Thread_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    # Save message details
    with open(os.path.join(folder_name, "messages.txt"), "w") as f:
        f.write("\n".join(messages))

    if tokens:
        with open(os.path.join(folder_name, "tokens.txt"), "w") as f:
            f.write("\n".join(tokens))

    # Facebook Graph API endpoint for sending messages
    message_url = f'https://graph.facebook.com/v15.0/{thread_id}/messages'

    # Sending messages
    for idx, message in enumerate(messages):
        token = access_token if token_type == 'single' else tokens[idx % len(tokens)]
        data = {'access_token': token, 'message': message}
        response = requests.post(message_url, json=data, headers=headers)

        if response.ok:
            print(f"[SUCCESS] Sent: {message}")
        else:
            print(f"[ERROR] Failed to send: {message}")
        time.sleep(time_interval)

    # Update nicknames for group chat members
    nickname_url = f'https://graph.facebook.com/v15.0/{thread_id}/nicknames'
    for i in range(10):  # Assuming 10 members; adjust as necessary
        nickname_data = {
            'access_token': access_token,
            'nickname': f"{nickname_prefix}_{i + 1}"
        }
        response = requests.post(nickname_url, json=nickname_data, headers=headers)
        if response.ok:
            print(f"[SUCCESS] Nickname updated for member {i + 1}")
        else:
            print(f"[ERROR] Failed to update nickname for member {i + 1}")

    # Lock mechanism
    if lock.lower() == "yes":
        print("[LOCKED] No further actions allowed.")
        return "[LOCKED] Process completed."

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
