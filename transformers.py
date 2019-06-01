def hexToBin(hexdec):
    dec = int(hexdec, 16)
    return bin(dec)[2:].zfill(56)

def transformer1(msg, json_frame, df, tc):
    #Aircraft identification
    print("Aircraft identifier")

def transformer2(msg, json_frame, df, tc):
    #surface position
    print("Surface Position")

def transformer3(msg, json_frame, df, tc):
    #Airborne Position
    print("Airborne Position")

def transformer4(msg, json_frame, df, tc):
    #Airborne velocity
    print("Airborne Velocity")

def transformer5(msg, json_frame, df, tc):
    #Enhanced ADS-B with BDS
    print("Enhanced ADS-B with BDS")
    msg_bin = hexToBin(msg[8:22])
    print("BDS:", int(msg_bin[:4],2),int(msg_bin[4:8], 2))
