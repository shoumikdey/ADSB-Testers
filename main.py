import json
import glob
import sys
import os
import time

cli_args = sys.argv[1:]
file_name = ""
input_path = "recordings"+os.sep
output_path = "output_json"+os.sep

def data(fhandle, fh):
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
            data = {"id":id, "type" : "ADSB_in_mlat", "ADSB_mlat":line, "data":data}
            #print(json.dumps(data, indent=4, separators=(',',':')))#encode('utf-8'))
            lst.append(data.copy())
    #print(lst)
    s=json.dumps(lst, indent=4, separators=(',',':'))
    fh.write(s)
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
            fh = open(fullPath, "a")
            data(fhandle, fh)
            fh.close()
    else:                                                        #arguments block
        file_name = sys.argv[sys.argv.index("--file")+1]
        if "." not in file_name:
            path = str(file_name)+"*"
            files = glob.glob(path)
            for fname in files:
                fhandle = open(fname)
                fullPath = os.path.join(output_path+fname[fname.index(os.sep)+1:]+".json")
                fh = open(fullPath, "a")
                data(fhandle, fh)
                fh.close()
        else:
            fullPath = os.path.join(output_path+file_name[file_name.index(os.sep)+1:]+".json")
            fh = open(fullPath, "a")
            data(open(file_name), fh)
            fh.close()


if __name__ == '__main__':
    time1 = time.time()
    main()
    print(time.time()-time1)
