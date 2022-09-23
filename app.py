from flask import Flask, render_template, Response, redirect, url_for, flash
import cv2
import os
from datetime import datetime
from time import sleep
import glob


from .image import Booth
from .camera import Camera

app = Flask(__name__)

os.makedirs('images', exist_ok=True)
cam = Camera()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/capture')
def capture():
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    image_dir = os.path.join('images', timestamp, 'raw')
    os.makedirs(image_dir)
    for i in range(3):
        cam.capture()
    cam.capture()
    cam.download_n_most_recent_images(image_dir)
    return redirect(url_for('print'))


@app.route('/print')
def print():
    image_dir = max(glob.glob('images/*T*'))
    b = Booth(image_dir)
    b.run()
    return render_template('print.html')


if __name__ == '__main__':
    app.run(debug=True)