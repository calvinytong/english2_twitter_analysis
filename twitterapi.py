# Import the necessary methods from "twitter" library
from twython import TwythonStreamer
import pickle as pkl
import os
import time
from time import gmtime, strftime
import datetime
import pytz

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = "3002655854-ZMTmg2RlZH2x92RApVyIMg2fQFgwvEJBCUXmy7X"
ACCESS_SECRET = "kS1cODyAf8nfTkMbbrDY1YNhIXGrYl5MsvP2aoJ7lKbzD"
CONSUMER_KEY = "LnKZ50b6p3EaGZc5fcxdcyNEr"
CONSUMER_SECRET = "8BKDn8KzLqwFxUb3b7JPCKbZgF8bVMjIGl3Tl0axCt07MZ3oYR"

class Streamer(TwythonStreamer):

    def __init__(self, filename, con_key, con_sec, acc_tok, acc_sec):
        path = os.path.join('data',filename + '.pkl')
        self.f = open(path, 'wb')
        self.count = 0
        super(Streamer, self).__init__(con_key, con_sec, acc_tok, acc_sec)

    def on_success(self, data):
        try:
            if data['lang'] == 'en':
                pkl.dump(data, self.f, -1)
                # print(data['text'])
                self.count += 1
                if self.count % 1000 == 0:
                    print('received tweet #', self.count)
        except KeyError:
            pass

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

def main():

    fmt = ' %H:%M:%S_%Y-%m-%d'
    d = datetime.datetime.now(pytz.timezone("America/New_York")).strftime(fmt)
    stream = Streamer(d,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    #this only returns geo tagged tweets in the USA

    while True:  #Endless loop: personalize to suit your own purposes
        try:
            stream.statuses.filter(locations ='-124.88,25.13,-66.09,49.1',replies = 'all')
        except:
            #e = sys.exc_info()[0]  #Get exception info (optional)
            #print 'ERROR:',e  #Print exception info (optional)
            continue

if __name__ == '__main__':
    main()
