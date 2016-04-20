#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import pandas as pd


#Variables that contains the user credentials to access Twitter API
access_token = "3002655854-ZMTmg2RlZH2x92RApVyIMg2fQFgwvEJBCUXmy7X"
access_token_secret = "kS1cODyAf8nfTkMbbrDY1YNhIXGrYl5MsvP2aoJ7lKbzD"
consumer_key = "LnKZ50b6p3EaGZc5fcxdcyNEr"
consumer_secret = "8BKDn8KzLqwFxUb3b7JPCKbZgF8bVMjIGl3Tl0axCt07MZ3oYR"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    print(auth)
    auth.set_access_token(access_token, access_token_secret)
    print(access_token)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['campaign', 'bernie', 'trump', 'election'])
