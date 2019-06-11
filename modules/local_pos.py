import math
def hexToBin(hexdec):
    dec = int(hexdec, 16)
    return bin(dec)[2:].zfill(56)

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

def main():
    msg = "8D40621D58C382D690C8AC2863A7"
    latRef = 52.258
    lonRef = 3.918
    isEven = False
    msg_bin = hexToBin(msg)
    if msg_bin[53] == "0":
        isEven = True
    if isEven:
        dLat = 360/60
    else:
        dLat = 360/59
    Latcpr = int(msg_bin[54:71], 2)/131072
    j = math.floor(latRef/dLat) + math.floor(((latRef%dLat)/dLat) - Latcpr + 0.5)
    lat = dLat * (j + Latcpr)
    if isEven:
        if (NL(lat)) > 0:
            dLon = 360/NL(lat)
        else:
            dLon = 360
    else:
        if (NL(lat)-1) > 0:
            dLon = 360/(NL(lat)-1)
        else:
            dLon = 360

    Loncpr = int(msg_bin[71:88], 2)/131072
    m = math.floor(lonRef/dLon) + math.floor(((lonRef%dLon)/dLon) - Loncpr + 0.5)
    lon = dLon * (m + Loncpr)


    print(lat, lon)

if __name__ == "__main__":
    main()
