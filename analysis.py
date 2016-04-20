import pickle as pkl
import numpy as np
# import matplotlib.pyplot as plt
import json

f = open('/Users/calvin/Documents/Lehigh/English/Research/data/cap1.pkl', 'rb')
unpickler = pkl.Unpickler(f)
data_array = []
count = 0
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
        if dd['coordinates'] == None:
            dd['coordinates'] = dd['place']['bounding_box']['coordinates'][0][0]
        data_array.append(dd)

            #todo make it average the bounding box
            # x1 =
            # x2 =
            # y1 =
            # y2 =
            # print(dd)
            # count += 1
print(data_array[0])

geo_data = {
    "type": "FeatureCollection",
    "features": []
}
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

with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))
