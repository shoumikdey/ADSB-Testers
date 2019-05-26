import json
import glob
import sys
import os


def data(fhandle, filename):
    count = 0
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):

            count += 1
            data = {'ADSB in mlat':line, 'Timestamp':line[1:13], 'ADSB message':line[13:len(line)-1]}
            print(json.dumps(data, indent=4, separators=(',',':')))#encode('utf-8'))
            fullPath = os.path.join("output_json/", filename+".json")
            fh = open(fullPath, "a")
            json.dump(data, fh)
            fh.write('\n')
    if count == 0:
        print("No dump1090 mlat format frame found")

def main():
    if "--file" not in sys.argv:
        path = "recordings/*"
        files = glob.glob(path)
        for fname in files:
            fhandle = open(fname)
            data(fhandle, fname[fname.index('/')+1:])
    else:
        if "." not in sys.argv[sys.argv.index("--file")+1]:
            path = str(sys.argv[sys.argv.index("--file")+1])+"*"
            files = glob.glob(path)
            for fname in files:
                fhandle = open(fname)
                data(fhandle, fname[fname.index('/')+1:])
        else:
            path=sys.argv[sys.argv.index("--file")+1]
            data(open(path), path[path.index('/')+1:])


if __name__ == '__main__':
    main()
