import time
import re
from pathlib import Path
import pandas as pd
import yaml


'''
name: parse_video.py
purpose: handle a Video object after it's gathered online and downloaded locally
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

def parse_chatlog(chatlog):
    """
    :param chatlog:
    :return: Pandas dataframe containing cleaned data corresponding to the inputted chatlog with columns:
        1. User - Twitch Display name of user of message (str)
        2. Timestamp - YYYY-MM-DDTHH:MM:SS (str)
        3. Message - Text data of message (str)
    """
    chat = []
    start = time.time()
    for comment in chatlog:
        '''Need to clean parts of the chat:
            - prevent bots' messages from showing
            - prevent stream commands from showing (!.*)
            - prevent subscription notifications from coming up '''

        if re.match(".*bot", comment.commenter.name) or re.match("!.*", comment.message.body) or re.match("They've subscribed for \d+ months!", comment.message.body):
            continue

        user = comment.commenter.display_name
        msg = comment.message.body.split(' ')
        timestamp = comment.created_at

        chat.append([user, timestamp, msg])
        print(f"{user}", f"{msg}")

    chat_df = pd.DataFrame(columns=['user', 'timestamp', 'message'], data=chat)
    end = time.time()
    print("----------------------------------\nChat data parsed in {:.2f} seconds\n----------------------------------".format(end-start))
    return chat_df


def save_chatlog(metadata, df_chatlog: pd.DataFrame):
    #create new folder within current directory called chatlog if doesn't exist
    Path(r"downloads/").mkdir(parents=True, exist_ok=True)
    #create subfolder with the name of the streamer
    Path(rf"downloads/{metadata['video_metadata']['user_name']}/").mkdir(parents=True, exist_ok=True)
    #create subfolder with the name of the vod date, to store metadata and chatlog
    Path(rf"downloads/{metadata['video_metadata']['user_name']}/{metadata['video_metadata']['created_at'][:10]}/").mkdir(parents=True, exist_ok=True)
    #save the dataframe within the subfolder
    filepath = Path(f"downloads/{metadata['video_metadata']['user_name']}/{metadata['video_metadata']['created_at'][:10]}/{metadata['video_metadata']['created_at'][:10]}.yaml")
    df_chatlog.to_csv(f"downloads/{metadata['video_metadata']['user_name']}/{metadata['video_metadata']['created_at'][:10]}/{metadata['video_metadata']['created_at'][:10]}.csv", header=True, index=False)
    with open(filepath, 'w') as file:
        yaml.dump(metadata, file)
    return rf"downloads/{metadata['video_metadata']['user_name']}/{metadata['video_metadata']['created_at'][:10]}/"