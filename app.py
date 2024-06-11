import webview
import subprocess
import time
import requests
from flask import Flask, render_template, request, jsonify
from urllib.request import urlopen
import re

app = Flask(__name__)

def transform_link(link):
    if "ask_previews" in link:
        link = link.replace("ask_previews", "ask_video")
    elif "previews" in link:
        link = link.replace("previews", "encoded")
    if "gif" in link:
        link = link.replace("gif", "mp4")
    elif "_large.jpg" in link:
        link = link.replace("_large.jpg", ".mp4")
    return link

def find_img_src(url, img_class):
    try:
        with urlopen(url) as response:
            html_content = response.read().decode('utf-8')
            img_srcs = [line.split('src=')[1].split('"')[1] for line in html_content.splitlines() 
                        if f'class="{img_class}"' in line and 'src=' in line]
            return [transform_link(src) for src in img_srcs]
    except Exception as e:
        return []

def validate_url(url):
    regex = re.compile(r'^(?:http|ftp)s?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    url = request.json.get('url')
    if not validate_url(url):
        return jsonify({"error": "Invalid URL"}), 400

    img_class = "background-gif"
    transformed_srcs = find_img_src(url, img_class)
    
    if transformed_srcs:
        return jsonify({"links": transformed_srcs}), 200
    else:
        return jsonify({"error": "No links found"}), 404

if __name__ == '__main__':
    port = 5000  # Port on which Flask app is running
    url = f"http://127.0.0.1:{port}/"

    # Start Flask server in a separate process
    flask_process = subprocess.Popen(["python", "-m", "flask", "run", "--port", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for Flask server to start
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            continue

    # Open Flask app in a standalone window
    webview.create_window("Your App Name", url)
    webview.start(debug=True)
