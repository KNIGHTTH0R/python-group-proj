# Simon Aizpurua
# saa13b

from __future__ import print_function
from instagram.client import InstagramAPI

access_token = "236134297.fcf2484.292104bb363a4134a900584856ea376f"
client_secret = "086878ff36a148f4aca782c5bc145f99"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="sharcee", count=10)
for media in recent_media:
   print(media.caption.text)
