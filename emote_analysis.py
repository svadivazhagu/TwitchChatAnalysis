import requests
import pandas as pd, re
#scrape the information from bttv website to identify popular emotes
chat = pd.read_csv("chat_timestamp.csv")


popular_emotes = (chat['message'].value_counts()[:100]).to_frame().reset_index()

emote_sent_grouped = []

for emote in popular_emotes.iterrows():
    emote_name = emote[1]['index']
    emote_popularity = emote[1]['message']
    answer = input('what is the sentiment of ' + emote_name + ' , used ' + str(emote_popularity) + ' times.')
    if answer == 'y':
        emote_sentiment = 'Positive'
    elif answer == 'n':
        emote_sentiment = 'Negative'
    elif answer == 'idk':
        emote_sentiment = 'Unknown'
    emote_sentiment

    emote_sent_grouped.append([emote_name, emote_popularity, emote_sentiment])

