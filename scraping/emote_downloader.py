import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import yaml
import os
import glob

#ingests the fp of a VOD and creates a csv of that streamer's emotes and the top 50 ffz/bttv emotes.
def downloader(fp):
    os.chdir(fp)
    #read in the yaml file
    file_name = glob.glob("*.yaml")[0]
    cwd = os.getcwd()
    file = open(cwd+"\\"+file_name, 'r')
    parsed = yaml.load(file, Loader=yaml.Loader)
    user_id = parsed["video_metadata"]["user_id"]
    user_name = parsed["video_metadata"]["user_name"]
    #request to ffz and the streamer's twitch emotes
    streamer_r = requests.get(f'https://twitchemotes.com/channels/{user_id}')
    ffz_r = requests.get('https://www.frankerfacez.com/emoticons/?sort=count-desc')
    #handle the response, traverse through the response html to find all the emote names
    streamer_soup = BeautifulSoup(streamer_r.content, 'html.parser')
    streamer_emotes = streamer_soup.find_all('div', {'class':'card-body'})[0].text.split('\n')
    last_index = streamer_emotes.index(' View Similar Emotes')
    filtered_streamer_emotes = streamer_emotes[:last_index]
    #remove the tier items in the list ex: $9.99 Tier and the empty spaces from the emote names
    regex = re.compile(r'\$\d+\.\d+\sTier.*')
    cleaned_streamer_emotes = [i.replace(" ",'') for i in filtered_streamer_emotes if i != '' and not regex.match(i)]

    ffz_soup = BeautifulSoup(ffz_r.content, 'html.parser')
    ffz_emotes = ffz_soup.find_all("td", {"class":"emote-name text-left"})
    cleaned_ffz_emotes = []
    for tag in ffz_emotes:
        split = tag.text.split('\n')
        #remove empty strings
        split.remove('')
        emote = split[0]
        cleaned_ffz_emotes.append(emote)

    #make a series with emote_name attribute

    emote_df = pd.DataFrame(data=cleaned_ffz_emotes + cleaned_streamer_emotes, columns=['emote_name'])
    #save series to csv
    emote_df.to_csv(f'{cwd}\emote_dictionary.csv', index=False)
