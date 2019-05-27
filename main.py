import json
import glob
import os
from time import gmtime, strftime
import time
import argparse

file_name = ""
input_path = "recordings"+os.sep
output_path = "output_json"+os.sep
inFile = os.getcwd()+os.sep+output_path
schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    },
    "inFile": {
      "type": "string"
    },
    "execTime": {
      "type": "string"
    },
    "type": {
      "type": "string"
    },
    "ADSB_mlat": {
      "type": "string"
    },
    "data": {
      "type": "object",
      "properties": {
        "Timestamp": {
          "type": "string"
        },
        "ADSB_message": {
          "type": "string"
        }
      },
      "required": [
        "Timestamp",
        "ADSB_message"
      ]
    }
  },
  "required": [
    "id",
    "inFile",
    "execTime",
    "type",
    "ADSB_mlat",
    "data"
  ]
}

def data(fhandle, fh, sch_json):
    flag = False
    id = 0
    lst = []
    execTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):
            id += 1
            flag = True
            #data = dict()
            data = {
            "Timestamp":line[1:13],
            "ADSB_message":line[13:len(line)-1]
            }
            data = {"id":id,"inFile":inFile, "execTime":execTime, "type" : "ADSB_in_mlat", "ADSB_mlat":line, "data":data}
            #print(json.dumps(data, indent=4, separators=(',',':')))#encode('utf-8'))
            lst.append(data.copy())
    #print(lst)
    s=json.dumps(lst, indent=4, separators=(',',':'))
    fh.write(s)
    jsonSchema = list()
    jsonSchema.append(schema)
    sch_json.write(json.dumps(jsonSchema, indent=4, separators=(',',':')))
            #fh.write('\n')
    if not flag:
        print("No dump1090 mlat format frame found")

def main(filepath):
    if "." not in filepath:
        filepath += "*"
    files = glob.glob(filepath)
    for fname in files:
        fhandle = open(fname)
        fullPath = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".json")
        schema_path = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".schema.json")
        fh = open(fullPath, "a")
        sch = open(schema_path, "w")
        data(fhandle, fh, sch)
        fh.close()

def getArgs():
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', type=str, help="Path to input file", default=input_path+"*")
    return args.parse_args()

if __name__ == '__main__':
    time1 = time.time()
    args = getArgs()
    main(args.file)
    print(time.time()-time1)
