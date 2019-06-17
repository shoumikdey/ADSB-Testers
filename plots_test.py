import glob
import json
import matplotlib.pyplot as plt

def icao(frame):
    return frame[2:8]

locx = dict()
locy = dict()
files = glob.glob("decoder_json/*")
x = list()
y = list()
z = list()
for file in files:
    fh = open(file)
    data = json.load(fh)
    for frames in data['data']:
        if frames['latitude'] != None:
            if icao(frames['ADSB_message']) not in locx:
                locx[icao(frames['ADSB_message'])] = list()
                locx[icao(frames['ADSB_message'])].append(frames['latitude'])
            else:
                locx[icao(frames['ADSB_message'])].append(frames['latitude'])
        if frames['longitude'] != None:
            if icao(frames['ADSB_message']) not in locy:
                locy[icao(frames['ADSB_message'])] = list()
                locy[icao(frames['ADSB_message'])].append(frames['longitude'])
            else:
                locy[icao(frames['ADSB_message'])].append(frames['longitude'])

for i in locx:
    fig = plt.figure()
    plt.scatter(locy[i], locx[i])
    plt.xlabel(i)
    #
    print(locy[i], i, "\n")
    print(locx[i], i,"\n")
    fig.savefig("plots/"+i+".png")

    #plt.show()
