from datetime import timedelta
import twitch
import os

'''
name: client_setup.py
purpose: handle information from user to connect to Twitch API and create a Helix object of a video.
contains:
    - parse_chatlog(chatlog)
        Given a Comments iterable parse the data and extract relevant fields out to a dataframe

    - save_chatlog(metadata, df_chatlog)
        Once the video's comments have been parsed, gather the metadata associated with the video and then save it in
        /chatlogs/ folder.

TODO:
    - figure out how to extract the number of comments in a Comments object
    - implement easier-to-customize functionality with saving the information
    - the time printing.
'''

#default twitch ID and client secret is the environment variable, but can be specified in CLI
def create_client(twitch_id=os.environ['twitch_id'], twitch_secret=os.environ['twitch_secret']):
    client = twitch.Helix(client_id=twitch_id,
                         client_secret=twitch_secret,
                         use_cache=True,
                         cache_duration=timedelta(minutes=30))
    return client
