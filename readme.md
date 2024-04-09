# Photobooth Lite

This is a fork of Xander Beberman's amazing Flask/gphoto2 [photobooth](https://github.com/xanwich/photobooth). I edited the code to use the front-facing camera on my Macbook Pro instead of interfacing with a fancy DSLR. Although the photos are less beautiful, the code ends up being simpler because it's much easier to save photos taken with the front-facing camera. The original documentation is below!

[Here](https://onlinetexttools.com/convert-text-to-image) is a good website for making the text overlays.

# Original Photobooth documentation

![Printed pictures from the photo booth](/docs/img/pics.webp)

This is the code component of a physical photo booth I built for my birthday/housewarming party in 2022. Much like any other photo booth, it takes four photos of you, adds some fun text, prints out the photos, and uploads them to instagram at [@xandersphotobooth](https://www.instagram.com/xandersphotobooth/).

![The booth set up](/docs/img/booth.webp)

In its complete form, it is made mostly out of

- PVC pipe
- Cardboard
- My bedsheet
- My laptop
- My roommate's DSLR
- An inkjet printer
- An iPad
- A softbox I found on the street one day

The software component of the photobooth is a bit hacky, since the camera I had access to is not officially compatible with GPhoto2, and the code has been slightly modified for other parties I and my friends have thrown, but it's a fun project that others may be able to use in some way.

![Example photbooth image from fondue party](/docs/img/booth-fondue.webp)

## Vague Description of How it All Works

![Diagram of app activity](/docs/img/pb-diagram.png)

1. Flask app starts
1. App "initializes" tethered camera by taking 1 photo with [GPhoto2](https://github.com/gphoto/gphoto2) to find current file number and folder in camera filesystem
1. App logs in to instagram via [Instagrapi](https://subzeroid.github.io/instagrapi/)
1. App serves HTML UI to ipad over local network
1. Ipad regularly queries `/status` app endpoint to get display text for UI page
1. User presses "Start"
1. App triggers capture of four images from camera
1. App downloads four most recent images from camera filesystem and saves to a folder named after current time `images/<YYYYMMDDTHHMMSS>`
1. App resizes saved images and composites two sets of four onto one sheet with [Pillow](https://github.com/python-pillow/Pillow)
1. App sends composited sheet to printer with LPR
1. App resizes saved images into squares and uploads to instagram with Instagrapi
1. App is ready again and sends status text to UI including link to start booth

## Installation

1. [Install conda](https://docs.anaconda.com/free/miniconda/miniconda-install/)
1. Create conda environment with `conda create --name photobooth --file environment.txt`
1. Rename `ig_credentials.example.py` to `ig_credentials.py` and add your instagram credentials

## Configuration

### Image overlay

Image.py adds text or an image on top of the four composited photos, referred to as `BOOTH_TEXT` in the code. This image can come from a static source, e.g. `static/cheese.png`, or be dynamically created in `banner.py`. To specify a static image, load an image at the top of `image.py` with

```python
BOOTH_TEXT = Image.open("path/to/image.png")
```

Or for a dynamic image, at the top of `image.py` import the overlay function:

```python
from .banner import make_booth_text
```

And later in `Booth.assemble`, create the overlay:

```python
def assemble(self):
    BOOTH_TEXT = make_booth_text()
    ...
```

#### Previewing Dynamic Overlay with `banner.py`

To get a preview of your dynamically overlay without running the full application, run `python banner.py` and an overlay will be generated and shown to you.

### UI

The HTML page served by the app can be found in `templates/index.html`, and the associated CSS in `static/style.css`. Change them around until you like them! Just make sure to leave the `<div id="pb-body">` element and script tag in `index.html`.

Much of the UI is also sent by the Flask app in the form of raw HTML bound to the global variable `current_text` and served through the app's `/status` endpoint. Change the text in `app.py`, but leave the links to `/capture` in order to start or restart the photobooth.

### Printing

In `image.py`, the `print` function of the `Booth` class sends a command to a printer using `lpr`. To change paper size, paper type, load tray, etc., edit this command. [LPR man page](https://www.man7.org/linux/man-pages/man1/lpr.1.html).

To disable printing, remove this command, or comment out the `self.print(self.full_path)` call in `Booth.run`.

### Instagram

To turn on/off instagram, set the `IG` flag in `ig.py` to `True`/`False`. When `True`, the app will log into instagram every time you start it, so leaving it `False` until you want it to start posting is recommended.

Set the caption for instagram posts in `upload` in `ig.py`.

## Warnings/Troubleshooting

While building this it was quite tricky to get all the different components to play nicely together. Here are some places you might have to debug if you are to implement this yourself:

- Camera troubles were bountiful:
  - The camera I used (Panasonic Lumix DMC-GH4) is not officially compatible with GPhoto, which recognized it as a different panasonic camera. Because of that, not all of the features were working well or as expected. Image capture was very slow and saving photos was either even slower or fully nonfunctional, which is why these workarounds are here.
  - The code currently pulls images from the camera's filesystem manually, not with GPhoto's "capture and download" function—your camera may not organize files the same way so you may have to change `Camera.strip_filename` or `Camera.create_filename` in `camera.py`.
  - GPhoto was picky about the USB port my camera was plugged into. There was only a certain configuration of ports between my macbook's USB-C ports and my USB-A dongle's ports that worked.
  - This is setup to work well with the image sizes output by the Lumix GH4. You may have to adjust the size and format on your camera, or adjust the image sizing in `image.py` for everything to look good.
- Instagrapi is very unofficial and there's no guarantee that posting to instagram with it will continue to work or that instagram won't think you are abot and freeze your account. It seemed to work fine for me most of the time, but towards the end of the last time the photobooth was setup, the posts stopped making it to instagram and I'm not sure why. I also had to approve most app logins with my phone.
- The printer I used was quite finicky—if the LPR settings didn't _exactly_ match the printer's settings, it would not print. The png I send to the printer is also not exactly what gets printed by the printer—the bleed was always off in a very confusing way. You may need to play around with sizing until you get a result you like. I used cheap photo paper, but this bad boy guzzles ink like nobody's business.
- I have only tried this on my macbook, I have no idea what issues would pop up on linux or windows.

Overall, getting this project up and running to a point you are happy with will probably take a substantial amount of debugging, hacking, and trial and error.

## Usage

1. Plug in camera and printer, if using. Make sure they are both on and camera is set to appropriate tether mode.
2. Set `ig.py` `IG` flag if desired.
3. In a terminal,

```bash
cd <path/to/photobooth>
conda activate photobooth
```

4. Run Flask app with the following command, changing ports if desired:

```bash
FLASK_APP=app FLASK_ENV=production flask run --host=0.0.0.0 --port=5002
```

5. Wait for camera to initialize, and for Instagram to log in. Authorize IG login request if necessary.
6. Find the IP address of the device running your flask app, e.g. `192.168.4.123`. On mac you can do this quickly by Option-clicking the wifi icon in the menu bar and recording "IP Address".
7. Navigate to `<device IP>:<port>` on tablet or other device used to serve UI. Using the example IP in the previous step and the default port 5002, you'd type `192.168.4.123:5002` into your browser.
8. Make sure you see the UI you expect!! Do a test run!! Say "cheese!!" Does the camera take photos? Does the instagram post show up? Does the printer print? If so, have fun!
