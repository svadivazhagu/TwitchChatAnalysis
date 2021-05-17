import requests
import pandas as pd, re
#scrape the information from bttv website to identify popular emotes

def emote_sentiment_input(chat_file):

    chat = pd.read_csv(chat_file)


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
        elif answer == 'i':
            emote_sentiment = 'Unknown'
        emote_sentiment

        emote_sent_grouped.append([emote_name, emote_popularity, emote_sentiment])

chat = pd.read_csv(r'/data/chat_with_datetime.csv')

omegaluls = []
for msg in chat.iterrows():
    if type(msg[1]['message']) == str and 'omegalul' in msg[1]['message'].lower():
        omegaluls.append(msg)
    continue

df = pd.DataFrame(data=omegaluls)

print(1)
