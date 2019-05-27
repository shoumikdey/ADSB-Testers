import json
import glob
import sys
import os
from time import gmtime, strftime
import time

cli_args = sys.argv[1:]
file_name = ""
input_path = "recordings"+os.sep
output_path = "output_json"+os.sep
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
    lst = list()
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):
            id += 1
            flag = True
            data = dict()
            data = {
            "Timestamp":line[1:13],
            "ADSB_message":line[13:len(line)-1]
            }
            data = {"id":id,"inFile":output_path, "execTime":strftime("%Y-%m-%d %H:%M:%S", gmtime()), "type" : "ADSB_in_mlat", "ADSB_mlat":line, "data":data}
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

def main():                                                   #no arguments
    if "--file" not in cli_args:
        path = input_path+"*"
        files = glob.glob(path)
        for fname in files:
            fhandle = open(fname)
            fullPath = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".json")
            schema_path=os.path.join(output_path+fname[fname.index(os.sep)+1:]+".schema.json")
            fh = open(fullPath, "a")
            sch = open(schema_path, "w")
            data(fhandle, fh, sch)
            fh.close()
    else:                                                        #arguments block
        file_name = sys.argv[sys.argv.index("--file")+1]
        if "." not in file_name:
            path = str(file_name)+"*"
            files = glob.glob(path)
            for fname in files:
                fhandle = open(fname)
                fullPath = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".json")
                schema_path = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".schema.json")
                fh = open(fullPath, "a")
                sch = open(schema_path, "w")
                data(fhandle, fh, sch)
                fh.close()
        else:
            fullPath = os.path.join(output_path+file_name[file_name.index(os.sep)+1:]+".json")
            schema_path = os.path.join(output_path+file_name[file_name.index(os.sep)+1:]+".schema.json")
            fh = open(fullPath, "a")
            sch = open(schema_path, "w")
            data(open(file_name), fh, sch)
            fh.close()


if __name__ == '__main__':
    time1 = time.time()
    main()
    print(time.time()-time1)
