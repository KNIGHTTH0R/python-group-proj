# Simon Aizpurua
# saa13b
import os
import time
from __future__ import print_function
from instagram.client import InstagramAPI

ig_credentials = {
    'client_id': "fcf2484c92244827b3bcc23d39a61b16",
    'client_secret': "086878ff36a148f4aca782c5bc145f99",
    'redirect_uri': "http://localhost:5000/instagram_callback"
}
api = InstagramAPI(**ig_credentials)


recent_media, next_ = api.user_recent_media(user_id="sharcee", count=10)
for media in recent_media:
   print(media.caption.text)
