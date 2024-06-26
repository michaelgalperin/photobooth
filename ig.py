import logging
from .ig_credentials import ig_username, ig_password
from instagrapi import Client

IG = False

if IG:
    print("IG LOGGING IN")
    try:
        cl = Client()
        cl.login(ig_username, ig_password)
        print("DONE")
    except:
        print("COULD NOT LOG IN")


def upload(images):
    if not IG:
        print("IG OFF, NOT UPLOADING")
        return
    try:
        media = cl.album_upload(
            images,
            caption="I had fun at Jenna and Dave's Wedding! Life's a beach!",
        )
        print("uploaded", images)
    except:
        print("could not upload", images)
