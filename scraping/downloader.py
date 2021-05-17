import json
import sys
import requests
import twitch
import os


def get_vod(vod: int, client: twitch.Helix):
    """
    Given a twitch Vod ID and Twitch API Client, return that video object and throw error if given an incorrect Vod iD
    :param vod: Twitch video ID , Twitch-Python Helix client
    :return: video: Twitch Helix API video object - twitch.helix.Video
    """

    # check if the video exists and is legitimate based on id
    try:
        video = client.video(video_id=vod)
    except requests.exceptions.HTTPError:
        sys.exit('Invalid VoD ID entered.')

    choice = input((f"Is '{video.title}' by {video.user_name} of duration {video.duration} created on {video.created_at} your requested VoD? (y/n)"))
    if choice.lower() == "y":
        return video
    else:
        sys.exit("Operation cancelled by user.")


def get_vod_metadata(video: twitch.helix.Video, twitch_gql_id=os.environ['twitch_gql_id']):
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

    gql_post_headers = {'Client-Id': twitch_gql_id}

    # put together request and send it

    r = requests.post('https://gql.twitch.tv/gql', json=gql_post_json_data, headers=gql_post_headers)

    gql_json_response = json.loads(r.content)

    games_played = []
    for i, game in enumerate(gql_json_response['data']['video']['moments']['edges']):
        game_name = game['node']['details']['game']['displayName']
        time_started = game['node']['positionMilliseconds']
        games_played.append({'game_name': game_name, 'time_started': time_started})
    return {'video_metadata': video.data,
            'games_played': games_played}


