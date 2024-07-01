"""
This is just a sample script to take a TSV file of headwords and definitions
and convert it to a JSONL file that can be used to bulk import data into
Scaife ATLAS.
"""


URN_PREFIX = "urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:my-defs"


import json

i = 0
for line in open("defs.tsv"):
    headword, definition = line.strip().split("\t")
    i += 1
    entry = {
        "headword": headword,
        "data": {
            "content": definition
        },
        "urn": f"{URN_PREFIX}-{i}"
    }
    print(json.dumps(entry, ensure_ascii=False))
