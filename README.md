# Twitter-Sentiment-Analysis

The goal of this project is to pull twitter data, using the tweepy wrapper around the twitter API, and perform simple sentiment analysis using the `vaderSentiment` library. The tweepy library hides all of the complexity necessary to handshake with Twitter's server for a secure connection.

I also produce a web server running at AWS to display the most recent 100 tweets from a given user and the list of users followed by a given user. In response to any existed user, the web server will respond with a tweet list color-coded by sentiment, using a red to green gradient and a page that displays the list of users followed by the given user.
