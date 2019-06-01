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
    print(msg, "Airborne Position", df, tc)
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
