import json
fhandle=open("output_json/dump1090_output_1.dat.json")
x = json.load(fhandle)
for j in x:
    print(j)

print(x["data"])
for a in x["data"]:
    print(a["Timestamp"])
