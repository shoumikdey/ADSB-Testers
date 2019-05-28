import json
import glob
import os
from time import gmtime, strftime
import time
import argparse

file_name = ""
input_path = "recordings"+os.sep
#output_path = "output_json"+os.sep
#inFile = os.getcwd()+os.sep+output_path


def data(fhandle, fh, fname):
    meta = {"inputFile":fname,
            "execTime":strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "dataFormat":""}
    flag = False
    id = 0
    lst = list()
    # execTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
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
            # data = {"id":id,"inFile":inFile, "execTime":execTime, "type" : "ADSB_in_mlat", "ADSB_mlat":line, "data":data}
            # #print(json.dumps(data, indent=4, separators=(',',':')))#encode('utf-8'))
            # lst.append(data.copy())

    #print(lst)
    s=json.dumps(json_comp, indent=2, separators=(',',':'))
    fh.write(s)

    #jsonSchema = list()
    #sonSchema.append(schema)
    #sch_json.write(json.dumps(jsonSchema, indent=4, separators=(',',':')))
            #fh.write('\n')
    if not flag:
        print("No dump1090 mlat format frame found")

def main(filepath, output_path):
    if "." not in filepath:
        filepath += "*"
    files = glob.glob(filepath)
    if len(files) != 0:
        for fname in files:
            fhandle = open(fname)
            fullPath = os.path.join(output_path+fname[fname.rindex(os.sep)+1:]+".json")
            print(fullPath)
            #schema_path = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".schema.json")
            try:
                fh = open(fullPath, "w")
            except FileNotFoundError as file_error:
                print("Destination folder not found")
                break;
            #sch = open(schema_path, "w")
            data(fhandle, fh, fname[fname.index(os.sep)+1:])
            fh.close()
    else:
        while len(files) == 0:
            print("No input file found in the input folder")
            filepath = input("Enter the file path: ")
            if "." not in filepath:
                filepath += "*"
            files = glob.glob(filepath)
        #print(files)
        if len(files) != 0:
            for fname in files:
                fhandle = open(fname)
                fullPath = os.path.join(output_path+fname[fname.rindex(os.sep)+1:]+".json")

                #schema_path = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".schema.json")
                try:
                    fh = open(fullPath, "w")
                except FileNotFoundError as file_error:
                    print("Destination folder not found")
                    break;
                #sch = open(schema_path, "w")
                data(fhandle, fh, fname[fname.index(os.sep)+1:])
                fh.close()


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
