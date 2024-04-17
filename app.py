from flask import (
    Flask,
    render_template,
    send_from_directory,
    Response,
    redirect,
    url_for,
    make_response,
    jsonify,
)
import os
import sys
from datetime import datetime
from time import sleep
import glob
from threading import Thread


from .image import Booth
from .camera import Camera

app = Flask(__name__)

os.makedirs("images", exist_ok=True)
cam = Camera()
current_text = "init"
capture_in_progress = False


@app.route("/")
def index():
    global current_text
    current_text = '<h1><a href="/capture">start</a></h1>'
    return render_template("index.html")


@app.route("/capture")
def capture():
    if not capture_in_progress:
        th = Thread(target=run_capture, args=())
        th.start()
    return render_template("index.html")


@app.route("/status")
def status():
    global current_text
    print(current_text)
    return current_text


@app.route("/print")
def show_print_screen():
    global current_text
    current_text = '<h1>printing!!!</h1><h1><a href="/capture">restart</a></h1>'
    return render_template("index.html")

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

def run_capture():
    global current_text
    global capture_in_progress
    capture_in_progress = True
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    image_dir = os.path.join("images", timestamp, "raw")
    os.makedirs(image_dir)
    cam.reset_counter()
    current_text = "<h1>get ready!</h1>"
    sleep(3)
    for _ in range(4):
        for i in range(3, 0, -1):
            current_text = f"<h1>{str(i)}...</h1>"
            sleep(1)
        current_text = "<h1>smile!!!</h1>"
        cam.capture(image_dir)
        sleep(1)
    upload_and_print()
    capture_in_progress = False


def upload_and_print():
    global current_text
    image_dir = max(glob.glob("images/*T*"))
    b = Booth(image_dir)
    current_text = "posting..."
    b.run()
    current_text = "done"
    image_path = os.path.join(image_dir, "booth.png")
    relative_image_path = os.path.relpath(image_path, start='images')
    current_text = f'<img src="/images/{relative_image_path}" width=750><h1>done!!! <a href="/capture">restart</a></h1>'

if __name__ == "__main__":
    app.run(debug=True)
