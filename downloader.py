import subprocess

vod_id = str(956998845)
length = str(10)
cmd = ['twitch-chatlog', vod_id, '--length', length]

request = subprocess.run(cmd, shell=True, capture_output=True)

chatlog = request.stdout.decode('utf-8').split('\n')

print(1)