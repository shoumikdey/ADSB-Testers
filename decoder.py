import json
import argparse
import glob
import os
from modules.identifiers import *
from modules.transformers import *

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

def const_frame():

    json_frame = {
        "meta":{
            "gs_lat":"",
            "gs_long":"",
            "gs_alt":"",
        },
        "data":{
            "id":None,
            "ADSB_raw"
            "ADSB_msg":None,
            "Timestamp":None,
            "SamplePos":None,
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
            "cprLong":None,
            #Airborne velocity Subtype 1data
            "Subtype":None,
            "IC":None,
            "RESV_A":None,
            "NAC":None,
            "S_ew":None,
            "V_ew":None,
            "S_ns":None,
            "V_ns":None,
            "VrSrc":None,
            "S_vr":None,
            "Vr":None,
            "RESV_B":None,
            "S_Dif":None,
            "Dif":None,
            #Subtype 3
            "S_hdg":None,
            "Hdg":None,
            "AS_t":None,
            "AS":None,
            #Operation status
            "stype_code":None,
            "sccc":None,
            "lw_codes":None,
            "op_mc":None,
            "ver":None,
            "NIC":None,
            "NACp":None,
            "SIL":None,
            "HRD":None,
            #version 2 Needs more understanding
            #Enhanced MODE-S
            "bds_1":None,
            "bds_2":None,
            "mcp_alt":None,
            "fms_alt":None,
            "baro_set":None,
            "VNAV_state":None,
            "Alt_hold_state":None,
            "Apr_state":None,
            "tgt_alt_source":None,
            "prev_lat":None,
            "prev_long":None,
            "isLocalUni":None #If the location is calculated is locally unambiguous (1 frame method)

        }
    }
    return json_frame

def decode(file_obj, fileOut_obj, fileName):
    # pos_data = list()
    data = json.load(file_obj)
    #json_frame['meta'] = data['meta']
    #json_frame['meta'].update(data['meta'])
    for frames in data["data"]:
        if identifier1(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer1(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))
            continue
        if identifier2(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer2(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))
            continue
        if identifier3(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer3(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))
            continue
        if identifier4(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer4(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))
            continue
        if identifier5(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer5(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))
            continue
        if identifier6(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer6(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))
            continue
        if identifier7(df(frames['ADSB_message']), getTC(frames['ADSB_message'])):
            transformer7(frames['ADSB_message'], const_frame(), df(frames['ADSB_message']), getTC(frames['ADSB_message']))

        #pos_data.append(each_pos)
    # json_data = {
    # "meta":"",
    # "data":pos_data
    # }
    #s=json.dumps(json_data, indent=2, separators=(',',':'))
    #fileOut_obj.write(s)

def main(inp_file):
    if "." not in inp_file and (inp_file.rindex(os.sep)+1 == len(inp_file)):
        inp_file += "*"
    files = glob.glob(inp_file)
    if len(files) != 0:
        print(files)
        for fname in files:
            fhandle = open(fname)
            if (output_path.rindex(os.sep) + 1) == len(output_path):
                fullPath = os.path.join(output_path+fname[fname.rindex(os.sep)+1:])
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
