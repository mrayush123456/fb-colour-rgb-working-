from flask import Flask, request, redirect, url_for
import requests

app = Flask(__name__)

# Headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Group Management</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center">Group Chat Nickname Manager</h1>
            <form action="/" method="post">
                <div class="mb-3">
                    <label for="accessToken" class="form-label">Access Token:</label>
                    <input type="text" class="form-control" id="accessToken" name="accessToken" placeholder="Paste your Facebook token" required>
                </div>
                <div class="mb-3">
                    <label for="groupId" class="form-label">Group Chat ID:</label>
                    <input type="text" class="form-control" id="groupId" name="groupId" placeholder="Enter Group Chat ID" required>
                </div>
                <div class="mb-3">
                    <label for="nicknamePrefix" class="form-label">Nickname Prefix:</label>
                    <input type="text" class="form-control" id="nicknamePrefix" name="nicknamePrefix" placeholder="Enter Nickname Prefix" required>
                </div>
                <div class="mb-3">
                    <label for="lock" class="form-label">Lock Nicknames?</label>
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
def manage_group():
    # Get form inputs
    access_token = request.form.get('accessToken')
    group_id = request.form.get('groupId')
    nickname_prefix = request.form.get('nicknamePrefix')
    lock = request.form.get('lock')

    # Facebook Graph API URL for group members
    members_url = f"https://graph.facebook.com/v15.0/{group_id}/members"
    params = {'access_token': access_token}

    try:
        # Fetch group members
        response = requests.get(members_url, params=params, headers=headers)
        response_data = response.json()
        if 'data' not in response_data:
            return f"Error: Unable to fetch group members. {response_data.get('error', 'Unknown error')}"

        members = response_data['data']
        print(f"Total members found: {len(members)}")

        # Update nicknames for each member
        for idx, member in enumerate(members):
            member_id = member['id']
            nickname = f"{nickname_prefix}_{idx + 1}"

            nickname_url = f"https://graph.facebook.com/v15.0/{group_id}/members/{member_id}/nicknames"
            nickname_data = {'access_token': access_token, 'nickname': nickname}

            nickname_response = requests.post(nickname_url, json=nickname_data, headers=headers)
            if nickname_response.status_code == 200:
                print(f"[SUCCESS] Updated nickname for Member ID: {member_id} -> {nickname}")
            else:
                print(f"[ERROR] Failed to update nickname for Member ID: {member_id} -> {nickname}")
                print(nickname_response.json())

        # Lock nicknames if specified
        if lock.lower() == "yes":
            lock_url = f"https://graph.facebook.com/v15.0/{group_id}/lock"
            lock_response = requests.post(lock_url, params={'access_token': access_token}, headers=headers)
            if lock_response.status_code == 200:
                print("[LOCKED] Nicknames have been locked successfully.")
            else:
                print("[ERROR] Failed to lock nicknames.")
                print(lock_response.json())

        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
