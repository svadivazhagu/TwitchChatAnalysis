import pandas as pd, re, matplotlib, numpy as np
from datetime import datetime
from tqdm import tqdm

chat = pd.read_csv("chat.csv")
#converted_timestamps = []

am_pm = chat['timestamp'].apply(lambda x: x[-2:])

def rex(stamp):
    return re.findall("(\d\d:\d\d)", stamp)[0]

chat['timestamp'] = chat['timestamp'].apply(rex)

chat['timestamp'] = chat['timestamp'] + am_pm

#creating new column called `datetime` to indicate the datetime object of the timestamp of the message - vectorized
chat['datetime'] = pd.to_datetime(chat[['date','timestamp']].astype(str).apply(' '.join, 1),
                                  format='%m/%d/%y %I:%M%p')

distribution = chat['datetime'].value_counts()

print(1)
