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
        <title>Facebook Commenter</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(120deg, #f6d365, #fda085);
                color: #333;
            }
            .container { 
                max-width: 90%; 
                margin: 5% auto; 
                background: white; 
                padding: 20px; 
                border-radius: 8px; 
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); 
                animation: fadeIn 1.5s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            input, button, textarea { 
                width: 100%; 
                margin-bottom: 15px; 
                padding: 15px; 
                border: 1px solid #ccc; 
                border-radius: 8px; 
                box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.1);
            }
            textarea {
                height: 400px; /* Large height for textarea */
                background: rgba(245, 245, 245, 0.9);
                font-size: 16px;
                color: #333;
                resize: none; /* Disable resizing */
                transition: background 0.5s ease;
            }
            textarea:focus {
                background: rgba(255, 255, 255, 1);
                border-color: #4CAF50;
                outline: none;
                box-shadow: 0 0 8px rgba(76, 175, 80, 0.8);
            }
            button { 
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                cursor: pointer; 
                transition: background-color 0.3s ease;
            }
            button:hover { 
                background-color: #45a049; 
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
                
                <label for="largeText">Large Text Area:</label>
                <textarea placeholder="Enter additional details or comments"></textarea>
                
                <button type="submit">Start Commenting</button>
            </form>
        </div>
    </body>
    </html>
    '''

# Keep the rest of your app code as it is

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
