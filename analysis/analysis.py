import pandas as pd, re, numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

#


print(chat.head())

distribution = chat['datetime'].value_counts(sort=False, bins=192)

norm_dist = distribution / distribution.mean()


#plot = distribution.plot(kind='line',rot=90, grid=True)

#plot.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
#plot.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))



plt.tight_layout()
plt.figure(dpi=2400)
plt.show()
