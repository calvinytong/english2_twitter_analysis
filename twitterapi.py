# Import the necessary methods from "twitter" library
from twython import TwythonStreamer
import pickle as pkl
import os
import time
from time import gmtime, strftime
import datetime
import pytz

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

def load_keys():
    keys = []
    path = os.path.join('.keys')
    f = open(path, 'r')
    for line in f:
        keys.append(str(line))
    return keys


def main():

    fmt = ' %H:%M:%S_%Y-%m-%d'
    d = datetime.datetime.now(pytz.timezone("America/New_York")).strftime(fmt)
    keys = load_keys()
    stream = Streamer(d,keys[0], keys[1], keys[2], keys[3])
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
