import math
def hexToDec(hexdec):
    dec = int(hexdec, 16)
    return bin(dec)[2:].zfill(56)

def lat_index(lat_cpr_even, lat_cpr_odd):
    return math.floor((59 * lat_cpr_even) - (60*lat_cpr_odd) + 0.5)

def NL(lat):
    try:
        nz = 15
        a = 1 - math.cos(math.pi / (2 * nz))
        b = math.cos(math.pi / 180.0 * abs(lat)) ** 2
        nl = 2 * math.pi / (math.acos(1 - a/b))
        nl = int(nl)
        return nl
    except:
        return 1

def latitude(lat_even, lat_odd, t_even, t_odd):
    dlatEven = 6;
    dlatOdd = 360/59;
    cprEven = int(lat_even, 2)/131072
    cprOdd = int(lat_odd, 2)/131072
    j = lat_index(cprEven, cprOdd)
    latEven = dlatEven * (j % 60 + cprEven)
    latOdd = dlatOdd * (j % 59 + cprOdd)
    if latEven >= 270:
        latEven -= 360
    if latOdd >= 270:
        latOdd -= 360
    if(NL(latEven) != NL(latOdd)):
        #exit("The positions are in different latitude zones")
        return 0
        #exit()
    if(t_even >= t_odd):
        return latEven
    else:
        return latOdd



def longitude(lat_even1, lat_odd1, long_even, long_odd, t_even, t_odd, nl_lat):
    #if(NL(int(lat_even1, 2)) != NL(int(lat_odd1, 2))):
    #print(NL(10.2157745361328), NL(10.2162144547802))
    if(t_even > t_odd):
        ni = max(NL(nl_lat),1)
        dLon = 360 / ni
        cprEven1 = int(long_even, 2)/131072
        cprOdd1 = int(long_odd, 2)/131072
        m = math.floor(cprEven1 * (NL(nl_lat) - 1) - cprOdd1 * NL(nl_lat) + 0.5)
        lon =  dLon*(m % ni + cprEven1)
    elif(t_odd > t_even):
        ni = max(NL(nl_lat)-1,1)
        dLon = 360 / ni
        cprEven1 = int(long_even, 2)/131072
        cprOdd1 = int(long_odd, 2)/131072
        m = math.floor(cprEven1 * (NL(nl_lat) - 1) - cprOdd1 * NL(nl_lat) + 0.5)
        lon = dLon*(m%ni + cprOdd1)
    if(lon >= 180):
        return lon - 360
    else:
        return lon
#print(latitude("10110011110111111", "10101100101000001", 0, 1))
#print(longitude("10110011110111111", "10101100101000001", "01001101110100110", "11110101101111010", 0, 1))

def altitude(bin_altitude):
    qBit = bin_altitude[7]
    alt=bin_altitude[0:7]+bin_altitude[8:]
    altitude = int(alt, 2)
    if(int(qBit) == 1):
        return altitude * 25 - 1000
    else:
        return altitude * 100 - 1000

def main_pos(frame1, frame2):
    # frame1 = input("Enter frame 1: ")
    # frame2 = input("Enter frame 2: ")
    hex_pos1 = frame1[8:22]
    hex_pos2 = frame2[8:22]
    bin_frame1 = hexToDec(hex_pos1)
    bin_frame2 = hexToDec(hex_pos2)
    cpr_frame1 = bin_frame1[21]
    cpr_frame2 = bin_frame2[21]

    bin_lat1 = bin_frame1[22:39]
    bin_lat2 = bin_frame2[22:39]
    bin_long1 = bin_frame1[39:]
    bin_long2 = bin_frame2[39:]
    #print(int(cpr_frame1), int(cpr_frame2), "hiealeidjalidjalsdijalsdij", hexToDec(frame1)[53], hexToDec(frame2)[53])
    if(int(cpr_frame1) == 0 and int(cpr_frame2) == 1):
        bin_lat_even = bin_lat1
        bin_long_even = bin_long1
        bin_lat_odd = bin_lat2
        bin_long_odd = bin_long2
    elif(int(cpr_frame1) == 1 and int(cpr_frame2) == 0):
        bin_lat_even = bin_lat2
        bin_long_even = bin_long2
        bin_lat_odd = bin_lat1
        bin_long_odd = bin_long1

    bin_alt = bin_frame2[8:20]

    if(bin_lat_even == bin_lat2):
        # print("latitude:", latitude(bin_lat_even, bin_lat_odd, 0, 1))
        # print("longitude:", longitude(bin_lat_even, bin_lat_odd, bin_long_even, bin_long_odd, 0, 1, latitude(bin_lat_even, bin_lat_odd, 0, 1)))
        return latitude(bin_lat_even, bin_lat_odd, 0, 1), longitude(bin_lat_even, bin_lat_odd, bin_long_even, bin_long_odd, 0, 1, latitude(bin_lat_even, bin_lat_odd, 0, 1)), altitude(bin_alt)
    else:
        # print("latitude:", latitude(bin_lat_even, bin_lat_odd, 1, 0))
        # print("longitude:", longitude(bin_lat_even, bin_lat_odd, bin_long_even, bin_long_odd, 1, 0, latitude(bin_lat_even, bin_lat_odd, 1, 0)))
        return latitude(bin_lat_even, bin_lat_odd, 0, 1), longitude(bin_lat_even, bin_lat_odd, bin_long_even, bin_long_odd, 0, 1, latitude(bin_lat_even, bin_lat_odd, 0, 1)), altitude(bin_alt)

    print("Altitude:",altitude(bin_alt),"ft OR", (altitude(bin_alt)*0.3048),"m")

# if __name__=="__main__":
#     main()
