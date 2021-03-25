# twitch chat analysis

## hypothesis:
if a a chat has a high similarity in Emotes and is experiencing higher frequency of messages at a given timestamp,
there is something 'exciting' happening on stream.

## ideation:
in a popular stream, if something 'stupid' happens -- chat tends to fill with a particular set of emotes/messages, in a rapid time. same thing occurs if something 'exciting' happens.

## potential use cases:
- if we can determine 'exciting' moments on stream (positive or negative), can calculate times with which to generate clips from - automatic clip generator?
- can we measure the quality of a stream by the engagements from chat? think of a "quality of streamer content"
- emote analysis. 
  - Use BS4 to scrape [bttv.com](https://betterttv.com/emotes/top) and identify popular emotes, or just extract it from the chat.
    - beyond this, identify sentiment associated with emotes. positive (KomodoHype, PogU, PagMan) and negative (FeelsBadMan, OMEGALUL)
