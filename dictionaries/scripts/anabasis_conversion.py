#!/usr/bin/env python

"""
Work-in-progress script to convert Mather's Anabasis lexicon to JSONL for Scaife ATLAS.

Note this treats each `div1` as a blob of plain text with no attempt (yet)
to retain formatting, extract senses or citations.
This will all come later (see LSJ).
"""

import json

from pathlib import Path
from lxml import etree
import unicodedata

ANABASIS_REPO = Path("../../../anabasis-mather")
DESTO_DIR = Path("../../test-data/dictionaries/anabasis-mather")

URN_PREFIX = "urn:cite2:scaife-viewer:dictionaries.v1:anabasis-mather"

nsmap = {"ns": "http://www.tei-c.org/ns/1.0"}

def to_string(el):
    return etree.tostring(el, with_tail=True, encoding="utf-8", method="text").decode("utf-8")

def latinize(char):
    mappings = {
        'α': 'a',
        'β': 'b',
        'γ': 'g',
        'δ': 'd', 
        'ε': 'e', 
        'ζ': 'z', 
        'η': 'h', 
        'θ': 'q', 
        'ι': 'i', 
        'κ': 'k', 
        'λ': 'l', 
        'μ': 'm', 
        'ν': 'v', 
        'ξ': 'c', 
        'ο': 'o', 
        'π': 'p', 
        'ρ': 'r', 
        'σ': 's',
        'ς': 's',
        'ϲ': 's', 
        'τ': 't', 
        'υ': 'u', 
        'φ': 'f', 
        'χ': 'x', 
        'ψ': 'y',
        'ω': 'w',
        chr(787): ')', # smooth breathing
        chr(788): '(', # rough breathing 
        chr(769): '/', # acute accent 
        chr(768): '\\', # grave accent
        chr(834): '=', # circumflex accent
        chr(837): '|' # iota subscript
    }
    return mappings.get(char, '')

def generate_key(greek_lemma):
    key = []
    for char in greek_lemma:
        for element in unicodedata.normalize("NFD", char.lower()):
            key.append(latinize(element))
    return "".join(key)

def get_entries(root):
    # first div element has metadata, second div element has introduction
    for i, entry in enumerate(root.xpath("ns:text//ns:div", namespaces=nsmap)):
        if entry.attrib["type"] == "edition":
            continue
        if entry.attrib["subtype"] != "entry": # skips the introduction
            continue

        entry_orig_id = i

        urn = f"{URN_PREFIX}-{entry_orig_id}"

        head = to_string(
            entry.xpath("ns:head", namespaces=nsmap)[0]
        ).split(",")[0].strip()
        entry_key = generate_key(head)
        contents = to_string(entry).strip()

        yield {
            "headword": head,
            "data": {
                "content": contents,
                "key": entry_key,
            },
            "urn": urn
        }

def check_urns(jsonl_filepath, urns = {}):
    with open(jsonl_filepath, "r") as f:
        for i, line in enumerate(f): 
            new_urn = json.loads(line)["urn"]
            if new_urn in set(urns.keys()):
                raise ValueError(
                    f"There is a duplicated URN in line {i} of file {jsonl_filepath}. \
                    The same urn was read in at line {urns[new_urn][1]} of file {urns[new_urn][0]}."
                )
            urns[new_urn] = (jsonl_filepath, i)
    return urns

def make_metadata(label, kind, desto_path, urn = None):
    if urn is None:
        try: 
            urn = URN_PREFIX
        except:
            print("No URN provided, so no metafile has been generated.")
            return None

    entry_list = []
    for filename in sorted(desto_path.glob("*.jsonl")):
        entry_list.append(str(filename).split('/')[-1])

    metadata = {
        "label": label,
        "urn": urn,
        "kind": kind, 
        "entries": entry_list
    }

    with open(f"{desto_path}/metadata.json", "w") as f:
        json.dump(metadata, f)
    
    print("metadata.json file written")

urns = {}
for filename in sorted(ANABASIS_REPO.glob("*.xml")):
    tree = etree.parse(filename)
    root = tree.getroot()

    num = filename.stem[-2:]

    with open(f"{DESTO_DIR}/entries_001.jsonl", "w") as f:
        for entry in get_entries(root):
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")

    urns = check_urns(f"{DESTO_DIR}/entries_001.jsonl", urns)

make_metadata("Anabasis Mather", "Dictionary", DESTO_DIR)


