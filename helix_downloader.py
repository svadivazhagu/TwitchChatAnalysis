import re
from datetime import timedelta

import pandas as pd
import twitch, os, requests

twitch_video = 1006516490
twitch_id = os.environ['twitch_id']
twitch_secret = os.environ['twitch_secret']

chat = []

helix = twitch.Helix(client_id=twitch_id,
                     client_secret=twitch_secret,
                     use_cache=True,
                     cache_duration=timedelta(minutes=10))

'''
TODO:
    make request to see if >1 game played during VOD
    if true:
        iterate through response ['data']['video']['moments']['edges'][i] to access the games
        access ['data']['video']['moments']['edges'][i]['node']['details']['game']['displayName'] to find game name
'''
#video_id = str(#######)

# json_data = {
#     "operationName": "VideoPlayer_ChapterSelectButtonVideo",
#     "variables": {
#         "includePrivate": false,
#         "videoID": video_id
#     },
#     "extensions": {
#         "persistedQuery": {
#             "version": 1,
#             "sha256Hash": "8d2793384aac3773beab5e59bd5d6f585aedb923d292800119e03d40cd0f9b41"
#         }
#     }
# }

#headers = {'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
# r = requests.post('https://gql.twitch.tv/gql', data=json_data, headers=headers)

for comment in helix.video(twitch_video).comments:
    '''Need to clean parts of the chat to ensure that bots don't make it through'''
    if  re.match(".*bot", comment.commenter.name):
        continue


    user = comment.commenter.display_name
    msg = comment.message.body
    timestamp = comment.created_at

    chat.append([user, timestamp, msg])

chat_df = pd.DataFrame(columns = ['user', 'timestamp', 'message'], data=chat)
chat_df.to_csv('helix_chat.csv',header=True, index=False)
