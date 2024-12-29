from flask import Flask, request, redirect, url_for, render_template_string
import requests
import time

app = Flask(__name__)

# Flask route for the main page
@app.route('/')
def index():
    return '''
        <html>
        <head>
            <title>Facebook Group Manager</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    color: #333;
                    text-align: center;
                    margin-top: 50px;
                }
                .container {
                    max-width: 500px;
                    margin: 0 auto;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                }
                input, select, button {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                button {
                    background-color: #007bff;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Facebook Group Manager</h2>
                <form action="/process" method="post">
                    <label for="token">Facebook Access Token</label>
                    <input type="text" id="token" name="token" placeholder="Enter your token" required>
                    
                    <label for="group_id">Group Chat ID</label>
                    <input type="text" id="group_id" name="group_id" placeholder="Enter the group chat ID" required>
                    
                    <label for="nickname">New Nickname for Members</label>
                    <input type="text" id="nickname" name="nickname" placeholder="Enter the new nickname" required>
                    
                    <label for="lock">Lock Changes?</label>
                    <select id="lock" name="lock">
                        <option value="yes">Yes</option>
                        <option value="no">No</option>
                    </select>
                    
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    '''

# Process the input and make API calls
@app.route('/process', methods=['POST'])
def process():
    token = request.form.get('token')
    group_id = request.form.get('group_id')
    nickname = request.form.get('nickname')
    lock = request.form.get('lock')

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Custom User Agent for Automation",
    }

    try:
        # Step 1: Fetch group members
        members_url = f"https://graph.facebook.com/{group_id}/members"
        response = requests.get(members_url, headers=headers)
        response_data = response.json()

        if 'error' in response_data:
            return f"Error: {response_data['error']['message']}"

        members = response_data.get('data', [])

        # Step 2: Change nicknames
        for member in members:
            member_id = member['id']
            change_url = f"https://graph.facebook.com/{group_id}/nicknames"
            payload = {
                "nickname": nickname,
                "member_id": member_id,
                "lock": lock == 'yes'
            }
            nickname_response = requests.post(change_url, headers=headers, json=payload)
            if nickname_response.ok:
                print(f"Nickname changed for {member['name']}")
            else:
                print(f"Failed to change nickname for {member['name']}")

        return "Process completed successfully!"

    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
