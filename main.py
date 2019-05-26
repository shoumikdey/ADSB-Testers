import json
import glob
import sys
import os

cli_args = sys.argv[1:]
file_name = ""
input_path = "recordings/"
output_path = "output_json/"

def data(fhandle, filename):
    count = 0
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):

            count += 1
            data = {'ADSB in mlat':line, 'Timestamp':line[1:13], 'ADSB message':line[13:len(line)-1]}
            print(json.dumps(data, indent=4, separators=(',',':')))#encode('utf-8'))
            fullPath = os.path.join(output_path+filename+".json")
            fh = open(fullPath, "a")
            json.dump(data, fh)
            fh.write('\n')
    if count == 0:
        print("No dump1090 mlat format frame found")

def main():                                                   #no arguments
    if "--file" not in cli_args:
        path = input_path+"*"
        files = glob.glob(path)
        for fname in files:
            fhandle = open(fname)
            data(fhandle, fname[fname.index('/')+1:])
    else:                                                        #arguments block
        file_name = sys.argv[sys.argv.index("--file")+1]
        if "." not in file_name:
            path = str(file_name)+"*"
            files = glob.glob(path)
            for fname in files:
                fhandle = open(fname)
                data(fhandle, fname[fname.index('/')+1:])
        else:
            path=file_name
            data(open(path), path[path.index('/')+1:])


if __name__ == '__main__':
    main()
