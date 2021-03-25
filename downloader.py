import subprocess, pandas as pd, re

vod_id = str(956998845)
length = str(0)
cmd = ['twitch-chatlog', vod_id, '--length', length]

request = subprocess.run(cmd, shell=True, capture_output=True)

chatlog = request.stdout.decode('utf-8').split('\n')

all_rows =[]
for row in chatlog:
    if re.match(".*!.*", row.lower()) or re.match(".*\*\*.*", row.lower()) or re.match(".*\<(.*bot)\>.*", row.lower()):
        #continue if message starts with ! means interacting with a chatbot - not indicative of stream
        #continue of message has ** in it -- means from a chatbot
        continue
    if not row:
        #means we are at the last item, disregard this one
        continue

    try:
        date = re.findall("\d{2}\/\d{2}\/\d{2}", row)[0]
        timestamp = re.findall("\d{2}:\d{2}:\d{2}\s\w\w", row)[0]
        username = re.findall("\<(.*?)\>", row)[0]
        message = re.findall(">\s(.*)", row)[0]

    except IndexError as e:
        print(e)

    all_rows.append([date, timestamp, username, message])
    #print(username, message)

df = pd.DataFrame(all_rows, columns=['date','timestamp','username','message'])

df.to_csv('chat.csv', index=False, header=True)

