import pandas as pd
from collections import Counter

'''
name: emote_extractor
purpose: remove repeat strings and irrelevant words from a Twitch video chatlog
'''

def emote_extraction(df: pd.DataFrame):
    #for each message, we need to find
    #the most common word in that message
    #extract it and save it as the new message (that's the intent)
    #if there is no most common word (ie each word is only used once) then discard the message? (not indicative of sentiment)
    print(1)
