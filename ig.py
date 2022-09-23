import logging
from .ig_credentials import ig_username, ig_password
from instagrapi import Client

print("IG LOGGING IN")
try:
    cl = Client()
    cl.login(ig_username, ig_password)
    print("DONE")
except:
    print("COULD NOT LOG IN")


def upload(images):
    try:
        media = cl.album_upload(
            images,
            caption="",
        )
        print("uploaded", images)
    except:
        print("could not upload", images)
