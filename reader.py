import json
import random
def hexToDec(hexdec):
    dec = int(hexdec, 16)
    return bin(dec)[2:].zfill(56)

def df(frame):
    bin_frame = hexToDec(frame)
    df = int(bin_frame[0:5], 2)
    return df

def getTC(frame):
    data = frame[8:22]
    bin = hexToDec(data)
    return int(bin[0:5],2)

def tcContent(tc):
    if tc >= 1 and tc <= 4:
        return "Aircraft Identification"
    elif tc >= 5 and tc <= 8:
        return "Aircraft Identification"
    elif tc >= 9 and tc <= 18:
        return "Airborne Position"
    elif tc == 19:
        return "Airborne velocities"
    elif tc >= 20 and tc <= 22:
        return "Airborne position"
    elif tc >= 23 and tc <= 27:
        return "Reserved"
    elif tc == 28:
        return "Aircraft Status"
    elif tc == 29:
        return "Target state and status operation"
    else:
        return "Aircraft operation status"

def main():
    fhandle = open('dump1090_output.dat')
    count = 0
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):
            if df(line[13:len(line)-1]) == 17:
                count += 1
                # print("ADSB in mlat:", line)
                # print("Timestamp:", line[1:13])
                # print("ADSB message", line[13:len(line)-1])
                # print("Downlink Format:", df(line[13:len(line)-1]))
                # print("Type code:", getTC(line[13:len(line)-1]))
                # print("Typecode Content:", tcContent(getTC(line[13:len(line)-1])), "\n")
                print(json.dumps({'ADSB in mlat':line, 'Timestamp':int(line[1:13],16),
                                'ADSB message':line[13:len(line)-1],
                                'Downlink Format':df(line[13:len(line)-1]),
                                'Type code':getTC(line[13:len(line)-1]),
                                'Content':tcContent(getTC(line[13:len(line)-1])),
                                'Distance from GS to aircraft':'',
                                'Sample Rate':'2MHz'},
                                indent=4, separators=(',',':')))#encode('utf-8'))
    if count == 0:
        print("No dump1090 mlat format frame found")

if __name__ == '__main__':
    main()
