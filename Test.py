import snscrape.modules.twitter as sntwitter

query = "#AI since:2024-03-01 until:2024-03-05"
tweets = []

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) > 10:
        break
    tweets.append(tweet.content)

print(tweets)
