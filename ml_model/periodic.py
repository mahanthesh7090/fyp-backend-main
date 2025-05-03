from tweet.models import City, Tweet
from snscrape.modules.twitter import TwitterSearchScraper
from snscrape.modules.twitter import Photo, Video, Gif
import pickle
import re
import pandas as pd
from nltk.corpus import stopwords
import nltk
import spacy
nlp = spacy.load('en_core_web_sm')
import tweepy

nltk.download('stopwords')


def is_spam(tweet):
    
    with open('ml_model/models_pkl/model_spam.pkl', 'rb') as f:
        model_spam = pickle.load(f)

    with open('ml_model/models_pkl/vectorizer_spam.pkl', 'rb') as f:
        vectorizer_spam = pickle.load(f)
    tweet = re.sub('[^a-zA-Z0-9\s]', '', tweet)
    tweet = tweet.lower()
    # nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    tweet = ' '.join([word for word in tweet.split() if word not in stop_words])
    X = vectorizer_spam.transform([tweet])
    y = model_spam.predict(X)
    if y == 1:
        return True
    else:
        return False

def classify_tweet(tweet):
    with open('ml_model/models_pkl/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('ml_model/models_pkl/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    tweet = re.sub('[^a-zA-Z0-9\s]', '', tweet)
    tweet = tweet.lower()
    # nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    tweet = ' '.join([word for word in tweet.split() if word not in stop_words])
    X = vectorizer.transform([tweet])
    y = model.predict(X)
    return y[0]

def extract_tweet_data(tweet, username, media_dict=None):
    metrics = tweet.public_metrics
    media_url = None

    if (
        media_dict
        and hasattr(tweet, "attachments")
        and tweet.attachments is not None
        and "media_keys" in tweet.attachments
    ):
        for key in tweet.attachments["media_keys"]:
            media = media_dict.get(key)
            if media and media.type == "photo":
                media_url = media.url
                break

    return {
        "id": tweet.id,
        "tweet": tweet.text,
        "username": username,
        "likes": metrics.get("like_count", 0),
        "retweets": metrics.get("retweet_count", 0),
        "quotes": metrics.get("quote_count", 0),
        "media": media_url
    }
def data_store(data):
    problem_type=""
    city = City.objects.get(name="Mysuru") 
    problem_type = classify_tweet(data['tweet'])
    print(problem_type)
    if problem_type == 'unproblematic':
        return  # do not store   
        
    locations = extract_locations(data['tweet'])
    storedTweet = Tweet.objects.create(
            id=data['id'],
            tweet=data['tweet'],
            username=data['username'],
            likes=data["likes"],
            retweets=data["retweets"],
            quotes=data["quotes"],
            media=data['media'],
            source='Twitter',
            city=city,
            problem_type=problem_type
        )
    for location in locations:
        storedTweet.location_set.create(location=location)
    storedTweet.save()

def extract_tweets_and_classify(username,client):
    
    user = client.get_user(username=username)
    user_id = user.data.id

    response = client.get_users_tweets(
    id=user_id,
    max_results=6,
    tweet_fields=["created_at", "public_metrics"],
    expansions=["attachments.media_keys"],
    media_fields=["url", "type"]
    
    )
    print(response.data)
    media_dict = {}
    if response.includes and "media" in response.includes:
        media_dict = {m["media_key"]: m for m in response.includes["media"] if m["type"] == "photo"}

    if response.data:
        for tweet in response.data:
            tweet_data = extract_tweet_data(tweet, username, media_dict)
            if not is_spam(tweet_data['tweet']):
            # Check & save
                if not Tweet.objects.filter(id=tweet_data["id"]).exists():
                    data_store(tweet_data)
    
    



    

# python -m spacy download en_core_web_sm
def extract_locations(tweet):
    doc = nlp(tweet)
    locations = [e.text
                 for e in doc.ents if e.label_ in ('FAC', 'LOC', 'EVENT', 'GPE', 'ORG')]
    return locations


def update_database():
    pass


def periodic():
    # extract tweets from every city (city table) and classify the tweets
    print("Periodic process started")
    
    
    username = "Twitter account user name" # add the particular user name where you want to extract tweets
    bearer_token = "" # add your token (twitter api developer account )
    client = tweepy.Client(bearer_token=bearer_token)
    extract_tweets_and_classify(username,client)
    

