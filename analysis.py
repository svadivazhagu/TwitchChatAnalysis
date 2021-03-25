import pandas as pd, re, matplotlib, numpy as np
from datetime import datetime

chat = pd.read_csv("chat.csv")
converted_timestamps = []

def rex(stamp):
    return re.findall("(\d\d:\d\d)", stamp)[0]

#chat['timestamp'] = chat['timestamp'].apply(rex)

distribution = chat['timestamp'].value_counts()

for row in chat.iterrows():
    date = row[1]['date']
    timestamp = row[1]['timestamp']
    converted_time = datetime.strptime(date+timestamp, '%m/%d/%y%I:%M:%S %p')
    converted_timestamps.append(converted_time)


#datetime.strptime(chat.loc[0]['timestamp'], '%I:%M:%S %p')

print(1)
