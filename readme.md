# [twitch](twitch.tv) chat sentiment analysis

## hypothesis
if a a chat has a high similarity in Emotes and is experiencing higher frequency of messages at a given timestamp,
there is something 'exciting' happening on stream.

## ideation
in a popular stream, if something **engaging** happens -- chat tends to fill with a particular set of emotes/messages, in a rapid time.
<img src="https://i.redd.it/52xqyo1i37k01.png" alt="Twitch chat when streamer Forsen has made a big mistake.">


## todo
- create a better measure of chatter engagement
  - instead of normalizing by mean, can use the overall *min* value (if using binned approach)
- identify most popular emotes for a given timestamp
  - because of *user spam* (spamming multiple emotes per message, can lead to inflation of sentiment)
  - to overcome this, associate an Emote-using chatter with one emote per message, and rank most popular emotes per time stamp to identify the most popular emote per X time unit.


## potential use cases
- if we can determine 'exciting' moments on stream (positive or negative), can calculate times with which to generate clips from - automatic clip generator?
- can we measure the quality of a stream by the engagements from chat? think of a "quality of streamer content"
- emote analysis. 
  - ~~Use BS4 to scrape [bttv.com](https://betterttv.com/emotes/top) and identify popular emotes, or just extract it from the chat.~~ 
  **Realized that this wasn't needed due to being able to choose what the most popular emotes were for a given stream, from the chatlog itself (3/24/21)**.
    - beyond this, identify sentiment associated with emotes. positive (KomodoHype, PogU, PagMan) and negative (FeelsBadMan, OMEGALUL)

## resources
[Emote-Controlled: Obtaining Implicit Viewer Feedback Through Emote-Based Sentiment Analysis on Comments of Popular Twitch.tv Channels](https://dl.acm.org/doi/abs/10.1145/3365523)

