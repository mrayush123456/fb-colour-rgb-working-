from flask import Flask, request, render_template_string, redirect, url_for
import requests
import time
import threading

# Flask App
app = Flask(__name__)

# Static Variables
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

STOP_FLAG = False  # Global flag to stop the process

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Automation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            color: #343a40;
            background-image: url('https://i.ibb.co/fFqG2rr/Picsart-24-07-11-17-16-03-306.jpg');
            background-size: cover;
            background-position: center;
        }
        .container {
            margin-top: 50px;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .btn-stop {
            background-color: #dc3545;
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Facebook Group/Inbox Message Sender</h1>
        <form method="POST" action="/" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="accessToken" class="form-label">Access Token:</label>
                <input type="text" class="form-control" id="accessToken" name="accessToken" required>
            </div>
            <div class="mb-3">
                <label for="threadIds" class="form-label">Target Group Chat/Inbox IDs (comma-separated):</label>
                <input type="text" class="form-control" id="threadIds" name="threadIds" required>
            </div>
            <div class="mb-3">
                <label for="kidx" class="form-label">Hater's Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" required>
            </div>
            <div class="mb-3">
                <label for="txtFile" class="form-label">Upload Message File (.txt):</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="time" class="form-label">Delay Between Messages (seconds):</label>
                <input type="number" class="form-control" id="time" name="time" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Start Sending Messages</button>
        </form>
        <form method="POST" action="/stop">
            <button type="submit" class="btn btn-stop w-100 mt-3">Stop</button>
        </form>
    </div>
</body>
</html>
'''

# Route: Home
@app.route("/", methods=["GET", "POST"])
def home():
    global STOP_FLAG
    STOP_FLAG = False  # Reset stop flag for new sessions

    if request.method == "POST":
        # Form Data
        access_token = request.form.get("accessToken")
        thread_ids = request.form.get("threadIds").split(",")
        hater_name = request.form.get("kidx")
        time_interval = int(request.form.get("time"))
        txt_file = request.files["txtFile"]

        # Read Messages from File
        try:
            messages = txt_file.read().decode("utf-8").splitlines()
        except Exception as e:
            return f"<p>Error reading file: {e}</p>"

        # Start a new thread for message sending
        threading.Thread(target=send_messages, args=(access_token, thread_ids, hater_name, messages, time_interval)).start()

        return "<p>Messages are being sent. You can stop the process using the 'Stop' button.</p>"

    return render_template_string(HTML_TEMPLATE)

# Route: Stop
@app.route("/stop", methods=["POST"])
def stop():
    global STOP_FLAG
    STOP_FLAG = True  # Set stop flag to True
    return redirect(url_for("home"))

# Function: Send Messages
def send_messages(access_token, thread_ids, hater_name, messages, time_interval):
    global STOP_FLAG

    for thread_id in thread_ids:
        for message in messages:
            if STOP_FLAG:
                print("[INFO] Message sending stopped by the user.")
                return
            
            try:
                full_message = f"{hater_name}: {message}"
                api_url = f"https://graph.facebook.com/v16.0/{thread_id}/messages"
                response = requests.post(api_url, data={
                    "message": full_message,
                    "access_token": access_token
                }, headers=HEADERS)

                if response.status_code == 200:
                    print(f"[SUCCESS] Message sent to {thread_id}: {full_message}")
                else:
                    print(f"[ERROR] Failed to send to {thread_id}: {response.json()}")

                time.sleep(time_interval)

            except Exception as e:
                print(f"[ERROR] Exception occurred: {e}")
                time.sleep(30)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
                    
