import glob
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def icao(frame):
    return frame[2:8]

locx = dict()
locy = dict()
locz = dict()
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

        if frames['altitude'] != None:
            if icao(frames['ADSB_message']) not in locz:
                locz[icao(frames['ADSB_message'])] = list()
                locz[icao(frames['ADSB_message'])].append(frames['altitude'])
            else:
                locz[icao(frames['ADSB_message'])].append(frames['altitude'])


for i in locx:
    # fig = plt.figure()
    # plt.scatter(locy[i], locx[i])
    # plt.xlabel(i)
    # #
    # print(locx[i], i, "\n")
    # print(locy[i], i,"\n")
    # fig.savefig("plots/"+i+".png")

    #plt.show()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(locx[i], locy[i], locz[i])
    ax.legend()
    ax.can_zoom()
    ax.set_xlabel('latitude')
    ax.set_ylabel('longitude')
    ax.set_zlabel('altitude')
    fig.savefig("plots/3D/"+i+".png")
    #plt.show()
