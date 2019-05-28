import json
import glob
import os
from time import gmtime, strftime
import time
import argparse

file_name = ""
input_path = "recordings"+os.sep

def data(fhandle, fh, fname):
    if ".json" not in fname:
        meta = {"inputFile":fname+".json",
                "execTime":strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                "dataFormat":""}
    else:
        meta = {"inputFile":fname,
                "execTime":strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                "dataFormat":""}
    flag = False
    id = 0
    lst = list()
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):
            meta["dataFormat"] = "avr"
            flag = True
            data = dict()
            data = {
            "id":id,
            "ADSB_raw":line,
            "Timestamp":line[1:13],
            "ADSB_message":line[13:len(line)-1]
            }
            lst.append(data)
            id += 1

    json_comp = {
        "meta":meta,
        "data":lst
    }

    s=json.dumps(json_comp, indent=2, separators=(',',':'))
    fh.write(s)

    if not flag:
        print("No dump1090 mlat format frame found")

def main(filepath, output_path):
    if "." not in filepath:
        filepath += "*"
    files = glob.glob(filepath)
    if len(files) != 0:
        for fname in files:
            fhandle = open(fname)
            #if output_name == None:
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
            data(fhandle, fh, fileName)
            fh.close()
    else:
        print("No input file found in the specified input folder")

def getArgs():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', type=str, help="Path to input file", default=input_path+"*")
    args.add_argument('-o', '--output', type=str, help="Path to output file", default = "output_json"+os.sep)
    return args.parse_args()

if __name__ == '__main__':
    time1 = time.time()
    args = getArgs()
    main(args.file, args.output)
    print(time.time()-time1)
