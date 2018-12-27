import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    items = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(items[0], items[1])
    auth.set_access_token(items[2], items[3])
    api = tweepy.API(auth)
    return api

def tweet_dict(status):
    """
    :param status:
    :return: a dictionary of each tweet with the following keys:
       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()
    """
    dict = {}
    dict['id'] = status.id
    dict['created'] = status.created_at.date()
    dict['retweeted'] = status.retweet_count
    dict['text'] = status.text
    dict['hashtages'] = status.entities['hashtags']
    dict['urls'] = status.entities['urls']
    dict['mentions'] = status.entities['user_mentions']
    dict['score'] = SentimentIntensityAnalyzer().polarity_scores(status.text)['compound']
    return dict

def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    statuses = tweepy.Cursor(api.user_timeline, screen_name=name).items(100)
    list_of_dict = []
    while True:
        try:
            status = next(statuses)
            list_of_dict.append(tweet_dict(status))
        except tweepy.TweepError:
            time.sleep(60)
            status = next(statuses)
            list_of_dict.append(tweet_dict(status))
        except StopIteration:
            break

    user = api.get_user(screen_name = name)
    dict_of_user = {}
    dict_of_user['user'] = user.screen_name
    dict_of_user['count'] = user.statuses_count
    dict_of_user['tweets'] = list_of_dict

    return dict_of_user

def following_user_dict(user):
    """
    :param user:
    :return: a dictionary containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image
    """
    dict = {}
    dict['name'] = user.name
    dict['screen_name'] = user.screen_name
    dict['followers'] = user.followers_count
    dict['created'] = user.created_at.date()
    dict['image'] = user.profile_image_url_https
    return dict

def fetch_following(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    users = tweepy.Cursor(api.friends, screen_name=name).items()
    list_of_dict = []
    while True:
        try:
            user = next(users)
            list_of_dict.append(following_user_dict(user))
        except tweepy.TweepError:
            time.sleep(60)
            user = next(users)
            list_of_dict.append(following_user_dict(user))
        except StopIteration:
            break

    return sorted(list_of_dict, key= lambda k: k['followers'], reverse=True)