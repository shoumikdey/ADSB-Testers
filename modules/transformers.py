import json
icao_last_seen = dict()

def getICAO(frame):
    return frame[2:8]

def hexToBin(hexdec):
    dec = int(hexdec, 16)
    return bin(dec)[2:].zfill(56)

def transformer1(msg, json_frame, df, tc):
    #Aircraft identification
    print(msg, "Aircraft identifier", df, tc)

def transformer2(msg, json_frame, df, tc):
    #surface position
    print(msg, "Surface Position", df, tc)

def transformer3(msg, json_frame, df, tc):
    #Airborne Position
    isEven = False
    print(msg, "Airborne Position", df, tc, hexToBin(msg)[53])
    if hexToBin(msg)[53] == "0":
        isEven = True
        #print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    if getICAO(msg) not in icao_last_seen:
        if isEven:
            icao_last_seen[getICAO(msg)] = ["",msg]
        else:
            icao_last_seen[getICAO(msg)] = [msg, ""]
    elif isEven:
        if icao_last_seen[getICAO(msg)][0] != "":
            print("Msg", msg, "Previous odd msg", icao_last_seen[getICAO(msg)][0])
            icao_last_seen[getICAO(msg)][1] = msg
        else:
            print("No previous odd msg found")
    elif not isEven:
        if icao_last_seen[getICAO(msg)][1] != "":
            print("Msg", msg, "Previous even msg", icao_last_seen[getICAO(msg)][1])
            icao_last_seen[getICAO(msg)][0] = msg
        else:
            print("No previous even msg found")
    #print(json.dumps(icao_last_seen, indent=2))
    #print(json_frame)

def transformer4(msg, json_frame, df, tc):
    #Airborne velocity
    print(msg, "Airborne Velocity")
    msg_bin = hexToBin(msg[8:22])
    print("Subtype:", int(msg_bin[5:8], 2))

def transformer5(msg, json_frame, df, tc):
    print("Airborne position with GNSS altitiude", df, tc)

def transformer6(msg, json_frame, df, tc):
    print("Aircraft operation status", df, tc)


def transformer7(msg, json_frame, df, tc):
    #Enhanced ADS-B with BDS
    print(msg, "Enhanced ADS-B with BDS", df, tc)
    msg_bin = hexToBin(msg[8:22])
    print("BDS:", int(msg_bin[:4],2),int(msg_bin[4:8], 2))
    if int(msg_bin[:4],2) in [2, 4, 5, 6]:
        print("-----------------------------------------------------------------")
