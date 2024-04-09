import logging
from .ig_credentials import ig_username, ig_password
from instagrapi import Client

IG = True

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
            caption="I had the Besst time at Bess's Birthday Bonanza! Bessitos!",
        )
        print("uploaded", images)
    except:
        print("could not upload", images)
