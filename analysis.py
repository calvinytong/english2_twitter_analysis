import pickle as pkl
import numpy as np
import json

def main():
    f = open('/Users/calvin/Documents/Lehigh/English/Research/data/cap1.pkl', 'rb')
    unpickler = pkl.Unpickler(f)
    data_array = []
    count = 0

    #pull out the first 10000 tweets, note this is easy to change, but speed and space
    #concerns make this limited. I think that doing a random sample would be better
    for x in range(0,10000):
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
            data_array.append(dd)

                #todo make it average the bounding box
                # x1 =
                # x2 =
                # y1 =
                # y2 =

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
