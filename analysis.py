import pickle as pkl
import numpy as np
import json
from collections import Counter
import csv
import random
import matplotlib.pyplot as plt
# from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile

#vector helpers
#note this code is adapted from Joel Grus's Excellent Data Science from scratch
#https://github.com/joelgrus/data-science-from-scratch

def vector_add(v,w):
    return[v_i + w_i for v_i, w_i in zip(v,w)]

def vector_sum(vectors):
    result = vectors[0]
    for vector in vectors[1:]:
        result = vector_add(result, vector)
    return result

def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v,w)]

def scalar_multiply(c, v):
    return[c * v_i for v_i in v]

def vector_mean(vectors):
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v,w))

def sum_of_squares(v):
    return dot(v,v)

def squared_distance(v,w):
    return sum_of_squares(vector_subtract(v,w))

class KMeans(object):
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k          # number of clusters
        self.means = None   # means of clusters

    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):

        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            # Find new assignments
            new_assignments = list(map(self.classify, inputs))

            # If no assignments have changed, we're done.
            if assignments == new_assignments:
                return

            # Otherwise keep the new assignments,
            assignments = new_assignments

            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a == i]
                # avoid divide-by-zero if i_points is empty
                if i_points:
                    self.means[i] = vector_mean(i_points)


def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = list(map(clusterer.classify, inputs))

    return sum(squared_distance(input,means[cluster])
               for input, cluster in zip(inputs, assignments))

def plot_squared_clustering_errors(inputs):

    ks = range(1, 20)
    errors = [squared_clustering_errors(inputs, k) for k in ks]

    plt.plot(ks, errors)
    plt.xticks(ks)
    plt.xlabel("k")
    plt.ylabel("total squared error")
    plt.show()

def rms(data, x_mean, y_mean, count):
    """
    Calculates the root mean squared error in the data more here
    http://statweb.stanford.edu/~susan/courses/s60/split/node60.html
    For now this is the metric we use to calculate clustering, however
    I think it will have to be improved to take into account how well the points
    cluster around 'hubs'

    data: the data array populated with the datum dicts
    x_mean: the mean of the x coordinates
    y_mean: the mean of the y coordinates
    count: number of samples in the data array

    """
    s = 0
    for d in data:
        x_coor = d['coordinates'][0]
        y_coor = d['coordinates'][1]
        s += (x_coor - x_mean)**2 + (y_coor - y_mean)**2
    return (s / count)**0.5

def get_stop_words():
    stop_word_set = None
    with open('stopwords.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            stop_word_set = set(row)
    if stop_word_set:
        return stop_word_set

def to_json(data_array):
        # #initialize geo_data json (just a dict here) to feed in to the maps
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }

        #populate the json file
        for d in data_array:
            geo_json_feature = {
                    "type": "Feature",
                    "geometry": {"type" : "Point", "coordinates" : d['coordinates']},
                    "properties": {
                        "text": d['text'],
                        "created_at": d['created_at']
                    }
                }
            geo_data['features'].append(geo_json_feature)

        #write the json out to a file
        with open('geo_data.json', 'w') as fout:
            fout.write(json.dumps(geo_data, indent=4))


def main():
    stop_word_set = get_stop_words()
    f = open('/Users/calvin/Documents/Lehigh/English/Research/data/cap1.pkl', 'rb')
    unpickler = pkl.Unpickler(f)
    data_array = []
    count = 0
    x_sum = 0
    y_sum = 0
    #pull out the first 10000 tweets, note this is easy to change, but speed and space
    #concerns make this limited. I think that doing a random sample would be better
    for x in range(0,100000):
        try:
            dd = pkl.load(f)
        except EOFError:
            break
        except Exception:
            print(count)
            count += 1
            unpickler.load()
            continue
        else:
            #right now we just take the first coordinate in the bounding box as the actual
            #we could average to find the middle, but this seems good enough for now
            if dd['coordinates'] == None:
                if dd['place'] == None:
                    continue
                dd['coordinates'] = dd['place']['bounding_box']['coordinates'][0][0]
            else:
                #account for edge case where coordinates are wrapped
                dd['coordinates'] = dd['coordinates']['coordinates']

            #count how many samples we take
            count += 1
            # print(dd.keys())
            # print(dd)

            #sum up the coordinate values
            x_sum += dd['coordinates'][0]
            y_sum += dd['coordinates'][1]

            #append the data point to the data array
            data_array.append(dd)

            #todo make it average the bounding box
            # x1 =
            # x2 =
            # y1 =
            # y2 =

    #take the mean of the x coordinates and y coordinates
    # x_mean = x_sum / count
    # y_mean = y_sum / count
    # text_list = []
    # print(rms(data_array,x_mean,y_mean,count))
    # for d in data_array:
    #     tok = d['text'].split()
    #     for w in tok:
    #         l = w.lower()
    #         if l in stop_word_set:
    #             continue
    #         text_list.append(l)
    #
    #
    # counts = Counter(text_list)
    # print(counts.most_common(15))

    inputs = []
    for d in data_array:
        inputs.append(d['coordinates'])

    plot_squared_clustering_errors(inputs)
    cluster = KMeans(20)
    cluster.train(inputs)
    print(cluster.means)
    #
    # cluster_data = []
    # for d in data_array:
    #     if cluster.classify(d['coordinates']) == 0:
    #         cluster_data.append(d)
    # print(len(cluster_data))
    #
    # to_json(cluster_data)


if __name__ == '__main__':
    main()
