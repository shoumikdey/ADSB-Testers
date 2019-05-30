import json
import argparse
import glob
import os

input_path = "output_json"+os.sep
output_path = "decoder_json"+os.sep
long_msg_bits = 112
short_msg_bits = 56

def getMsgLength(df):
    if df > 16:
        return long_msg_bits
    else:
        return short_msg_bits

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
    if getMsgLength(df(frame)) == 112:
        return int(bin[0:5],2)
    else:
        return None

def capability(frame):
    bin_frame = hexToDec(frame)
    return int(bin_frame[5:8], 2)

def icao(frame):
    return frame[2:8]

def parity(frame):
    return frame[22:]

def surveillance_status(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[32:37]

def NICsb(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[39]

def Altitude(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[40:52]

def Time(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[52]

def CPR(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[53]

def cprLat(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[54:71]

def cprLong(frame):
    bin_frame = hexToDec(frame)
    return bin_frame[71:88]


def decode(file_obj, fileOut_obj, fileName):
    pos_data = list()
    data = json.load(file_obj)
    for frames in data["data"]:
        each_pos = dict()
        frames['Timestamp'] = int(frames['Timestamp'], 16) * 6
        frames['Samplepos'] = frames.pop('Timestamp')
        if df(frames['ADSB_message']) == 17:
            each_pos = {
                "id":frames['id'],
                "ADSB":frames['ADSB_message'],
                "SamplePos":frames['Samplepos'],
                "df":df(frames['ADSB_message']),
                "tc":getTC(frames['ADSB_message']),
                "capability":capability(frames['ADSB_message']),
                "icao":icao(frames['ADSB_message']),
                "parity":parity(frames['ADSB_message']),
                "surv_stat":surveillance_status(frames['ADSB_message']),
                "NICsb":NICsb(frames['ADSB_message']),
                "alt": Altitude(frames['ADSB_message']),
                "Time":Time(frames['ADSB_message']),
                "cpr_flag":CPR(frames['ADSB_message']),
                "cprLat":cprLat(frames['ADSB_message']),
                "cprLong":cprLong(frames['ADSB_message'])
            }
        else:
            each_pos = {
                "id":frames['id'],
                "ADSB":frames['ADSB_message'],
                "SamplePos":frames['Samplepos'],
                "df":None,
                "tc":None,
                "capability":None,
                "icao":None,
                "parity":None,
                "surv_stat":None,
                "NICsb":None,
                "alt": None,
                "Time":None,
                "cpr_flag":None,
                "cprLat":None,
                "cprLong":None
            }
        pos_data.append(each_pos)
    json_data = {
    "meta":"",
    "data":pos_data
    }
    s=json.dumps(json_data, indent=2, separators=(',',':'))
    fileOut_obj.write(s)

def main(inp_file):
    if "." not in inp_file and (inp_file.rindex(os.sep)+1 == len(inp_file)):
        inp_file += "*"
    files = glob.glob(inp_file)
    if len(files) != 0:
        print(files)
        for fname in files:
            fhandle = open(fname)
            if (output_path.rindex(os.sep) + 1) == len(output_path):
                fullPath = os.path.join(output_path+fname[fname.rindex(os.sep)+1:]+".json")
            else:
                fullPath = os.path.join(output_path+".json")
            try:
                fh = open(fullPath, "w")
            except FileNotFoundError as file_error:
                print("New folder created")
                os.mkdir(output_path[:output_path.rindex(os.sep)])
                fh = open(fullPath, "w")
                #break;
            #sch = open(schema_path, "w")
            if (output_path.rindex(os.sep)+1) == len(output_path):
                fileName = fname[fname.rindex(os.sep)+1:]
            else:
                fileName = output_path[output_path.rindex(os.sep)+1:]
            #data(fhandle, fh, fileName)
            decode(fhandle, fh, fileName)


def getArgs():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', type=str, help="Path to the json file", default=input_path)
    return args.parse_args()

if __name__ == "__main__":
    args = getArgs()
    main(args.file)
