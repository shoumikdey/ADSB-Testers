import json
import glob
import sys

def data(fhandle):
    count = 0
    for line in fhandle:
        line = line.rstrip()
        if line.startswith('@') and line.endswith(';') and (len(line) == 42 or len(line) == 28):

            count += 1
            print(json.dumps({'ADSB in mlat':line, 'Timestamp':line[1:13], 'ADSB message':line[13:len(line)-1]}, indent=4, separators=(',',':')))#encode('utf-8'))
    if count == 0:
        print("No dump1090 mlat format frame found")

def main():
    if "--file" not in sys.argv:
        path = "recordings/*.dat"
        files = glob.glob(path)
        for fname in files:
            fhandle = open(fname)
            data(fhandle)
    else:
        path = sys.argv[sys.argv.index("--file")+1]
        data(open(path))


if __name__ == '__main__':
    main()
