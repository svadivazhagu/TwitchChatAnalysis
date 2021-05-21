import pandas as pd
from collections import Counter
import re

'''
name: emote_extractor
purpose: remove repeat strings and irrelevant words from a Twitch video chatlog
'''

def emote_extraction(chatlog : pd.DataFrame):
    #for each message, we need to find
    #the most common word in that message
    #extract it and save it as the new message (that's the intent)
    #if there is no most common word (ie each word is only used once) then discard the message? (not indicative of sentiment)
    msg_counter = Counter(chatlog.split(" "))


df = pd.read_csv(r"C:\Users\SV\PycharmProjects\TwitchChatAnalysis\downloads\xQcOW\2021-04-30\2021-04-30.csv")
df['message'] = df['message'].astype('str')
mode_df = pd.DataFrame({"mode" : df["message"].str.split(' ').apply(lambda x: [k for k, v in Counter(x).most_common(1)])})
mode_df['mode'] = [','.join(map(str, l)) for l in mode_df['mode']]

mode_df.to_csv('most_common_words.csv', index=False, header=True)