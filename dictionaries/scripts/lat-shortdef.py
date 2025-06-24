URN_PREFIX = "urn:cite2:scaife-viewer:dictionaries.v1:lat-short-def"


import json

i = 0
for line in open("../shortdefs/LogeionLatinshortdefs.txt"):
    headword, definition = line.strip().split("\t")
    i += 1
    entry = {
        "headword": headword,
        "definition": definition,
        "urn": f"{URN_PREFIX}-{i}"
    }
    print(json.dumps(entry, ensure_ascii=False))
