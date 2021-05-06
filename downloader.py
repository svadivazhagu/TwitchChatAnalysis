import json
import re
import sys
from datetime import timedelta
import requests
import pandas as pd
import twitch
import os
from pathlib import Path

SAME = 1008313700
DIFF = 1006516490


def get_vod(vod_id: int):
    """
    Given a twitch Vod ID, return that video object and throw error if given an incorrect Vod iD
    :param vod_id: Twitch video ID - Int
    :return: video: Twitch Helix API video object - twitch.helix.Video
    """
    twitch_id = os.environ['twitch_id']
    twitch_secret = os.environ['twitch_secret']

    helix = twitch.Helix(client_id=twitch_id,
                         client_secret=twitch_secret,
                         use_cache=True,
                         cache_duration=timedelta(minutes=10))

    # check if the video exists and is legitimate based on id
    try:
        video = helix.video(video_id=vod_id)
    except requests.exceptions.HTTPError:
        sys.exit('Requested VoD not found.')

    choice = input((f"Is '{video.title}' by {video.user_name} of duration {video.duration} created on {video.created_at} your requested VoD? (y/n)"))
    if choice.lower() == "y":
        return video
    else:
        sys.exit("Operation cancelled by user.")


def get_vod_metadata(video: twitch.helix.Video):
    """
    Given a Video vod, extract the desired metadata from that vod
    :param video: twitch Helix video
    :return:
    """
    created_at = video.created_at
    streamer = video.user.display_name
    duration = video.duration
    video_id = video.id

    # extract the games played during that vod and the timestamps when that game started being played.

    # assemble the JSON body to be sent with request.

    gql_post_json_data = {
        "operationName": "VideoPlayer_ChapterSelectButtonVideo",
        "variables": {
            "includePrivate": False,
            "videoID": video_id
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "8d2793384aac3773beab5e59bd5d6f585aedb923d292800119e03d40cd0f9b41"
            }
        }
    }

    # create the headers for the request containing client ID given in browser !!! may need to update this !!!
    gql_post_headers = {'Client-Id': os.environ['twitch_gql_id']}

    # put together request and send it

    r = requests.post('https://gql.twitch.tv/gql', json=gql_post_json_data, headers=gql_post_headers)

    gql_json_response = json.loads(r.content)

    games_played = []
    for i, game in enumerate(gql_json_response['data']['video']['moments']['edges']):
        game_name = game['node']['details']['game']['displayName']
        time_started = game['node']['positionMilliseconds']

        games_played.append({'game_name': game_name, 'time_started': time_started})

    return {'created_at': created_at, 'streamer': streamer, 'duration': duration, 'video_id': video_id,
            'games_played': games_played}


def parse_chatlog(chatlog):
    """

    :param chatlog:
    :return: Pandas dataframe containing cleaned data corresponding to the inputted chatlog with columns:
        1. User - Twitch Display name of user of message (str)
        2. Timestamp - YYYY-MM-DDTHH:MM:SS (str)
        3. Message - Text data of message (str)
    """
    chat = []
    for comment in chatlog:
        '''Need to clean parts of the chat:
            - prevent bots' messages from showing
            - prevent stream commands from showing (!.*)'''
        if re.match(".*bot", comment.commenter.name) or re.match("!.*", comment.message.body):
            continue

        user = comment.commenter.display_name
        msg = comment.message.body
        timestamp = comment.created_at

        chat.append([user, timestamp, msg])
        print(f"{user}", f"{msg}")

    chat_df = pd.DataFrame(columns=['user', 'timestamp', 'message'], data=chat)
    return chat_df


def save_chatlog(metadata, df_chatlog: pd.DataFrame):
    #create new folder within current directory called chatlog if doesn't exist
    Path(r"chatlogs/").mkdir(parents=True, exist_ok=True)
    #create subfolder with the name of the chatlog file
    Path(f"chatlogs/{metadata['streamer']}/").mkdir(parents=True, exist_ok=True)
    #save the dataframe within the subfolder
    filepath = f"chatlogs/{metadata['streamer']}/{metadata['created_at'][:-4]}"
    df_chatlog.to_csv(f"chatlogs/{metadata['streamer']}/{metadata['created_at'][:10]}.csv", header=True, index=False)

if __name__ == '__main__':
    vod = get_vod('1006728507')
    metadata = get_vod_metadata(vod)
    chat_df = parse_chatlog(vod.comments)
    save_chatlog(metadata, chat_df)
