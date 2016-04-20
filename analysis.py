import pickle as pkl
import numpy as np
import json

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



def main():
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
    x_mean = x_sum / count
    y_mean = y_sum / count

    print(rms(data_array,x_mean,y_mean,count))

    #initialize geo_data json (just a dict here) to feed in to the maps
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }

    #populate the json file
    for d in data_array:
        geo_json_feature = {
                "type": "Feature",
                "geometry": d['coordinates'],
                "properties": {
                    "text": d['text'],
                    "created_at": d['created_at']
                }
            }
        geo_data['features'].append(geo_json_feature)

    #write the json out to a file
    with open('geo_data.json', 'w') as fout:
        fout.write(json.dumps(geo_data, indent=4))


if __name__ == '__main__':
    main()
