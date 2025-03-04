#!/usr/bin/env python

"""
Work-in-progress script to convert Lewis and Short elementary Latin dictionary to JSONL for Scaife ATLAS.

Note this treats each `div1` as a blob of plain text with no attempt (yet)
to retain formatting or citations.
This will all come later (see LSJ).
"""

import json

from pathlib import Path
from lxml import etree
import unicodedata

ELEM_LATIN_REPO = Path("../../../elementary-latin")
DESTO_DIR = Path("../../test-data/dictionaries/elementary-latin")

if not DESTO_DIR.exists():
    DESTO_DIR.mkdir()

URN_PREFIX = "urn:cite2:scaife-viewer:dictionaries.v1:elementary-latin"


def to_string(el):
    return etree.tostring(el, with_tail=True, encoding="utf-8", method="text").decode(
        "utf-8"
    )


def get_senses(entry, urn):
    parent_senses = []
    for sense in entry.xpath("sense"):
        sense_orig_id = sense.attrib["id"]
        contents = to_string(sense).strip() if sense.text else ""

        if sense.attrib["level"] == "0":
            sense_urn = f"{urn}-{sense_orig_id}"
            parent_senses.append(
                {
                    "label": sense.attrib.get("n"),
                    "definition": contents,
                    "urn": sense_urn,
                    "children": [],
                }
            )

        elif sense.attrib["level"] == "1":
            if len(parent_senses) == 0:
                parent_senses.append(
                    {
                        "definition": "",
                        "urn": f"{urn}-0",
                        "children": [],
                    }
                )
            parent_urn = parent_senses[-1]["urn"]
            sense_urn = f"{parent_urn}-{sense_orig_id}"
            parent_senses[-1]["children"].append(
                {
                    "label": sense.attrib.get("n"),
                    "definition": contents,
                    "urn": sense_urn,
                    "children": [],
                }
            )

        elif sense.attrib["level"] == "2":
            if len(parent_senses) == 0:
                parent_senses.append(
                    {
                        "definition": "",
                        "urn": f"{urn}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"]) == 0:
                parent_senses[-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['urn']}-0",
                        "children": [],
                    }
                )

            parent_urn = parent_senses[-1]["children"][-1]["urn"]
            sense_urn = f"{parent_urn}-{sense_orig_id}"

            parent_senses[-1]["children"][-1]["children"].append(
                {
                    "label": sense.attrib.get("n"),
                    "definition": contents,
                    "urn": sense_urn,
                    "children": [],
                }
            )

        elif sense.attrib["level"] == "3":
            if len(parent_senses) == 0:
                parent_senses.append(
                    {
                        "definition": "",
                        "urn": f"{urn}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"]) == 0:
                parent_senses[-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['urn']}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"][-1]["children"]) == 0:
                parent_senses[-1]["children"][-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['children'][-1]['urn']}-0",
                        "children": [],
                    }
                )

            parent_urn = parent_senses[-1]["children"][-1]["children"][-1]["urn"]
            sense_urn = f"{parent_urn}-{sense_orig_id}"
            parent_senses[-1]["children"][-1]["children"][-1]["children"].append(
                {
                    "label": sense.attrib.get("n"),
                    "definition": contents,
                    "urn": sense_urn,
                    "children": [],
                }
            )

        elif sense.attrib["level"] == "4":
            if len(parent_senses) == 0:
                parent_senses.append(
                    {
                        "definition": "",
                        "urn": f"{urn}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"]) == 0:
                parent_senses[-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['urn']}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"][-1]["children"]) == 0:
                parent_senses[-1]["children"][-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['children'][-1]['urn']}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"][-1]["children"][-1]["children"]) == 0:
                parent_senses[-1]["children"][-1]["children"][-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['children'][-1]['children'][-1]['urn']}-0",
                        "children": [],
                    }
                )

            parent_urn = parent_senses[-1]["children"][-1]["children"][-1]["children"][
                -1
            ]["urn"]
            sense_urn = f"{parent_urn}-{sense_orig_id}"

            parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
                "children"
            ].append(
                {
                    "label": sense.attrib.get("n"),
                    "definition": contents,
                    "urn": sense_urn,
                    "children": [],
                }
            )

        elif sense.attrib["level"] == "5":
            if len(parent_senses) == 0:
                parent_senses.append(
                    {
                        "definition": "",
                        "urn": f"{urn}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"]) == 0:
                parent_senses[-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['urn']}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"][-1]["children"]) == 0:
                parent_senses[-1]["children"][-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['children'][-1]['urn']}-0",
                        "children": [],
                    }
                )

            if len(parent_senses[-1]["children"][-1]["children"][-1]["children"]) == 0:
                parent_senses[-1]["children"][-1]["children"][-1]["children"].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['children'][-1]['children'][-1]['urn']}-0",
                        "children": [],
                    }
                )

            if (
                len(
                    parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
                        "children"
                    ]
                )
                == 0
            ):
                parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
                    "children"
                ].append(
                    {
                        "definition": "",
                        "urn": f"{parent_senses[-1]['children'][-1]['children'][-1]['children'][-1]['urn']}-0",
                        "children": [],
                    }
                )

            parent_urn = parent_senses[-1]["children"][-1]["children"][-1]["children"][
                -1
            ]["children"][-1]["urn"]
            sense_urn = f"{parent_urn}-{sense_orig_id}"

            parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
                "children"
            ][-1]["children"].append(
                {
                    "label": sense.attrib.get("n"),
                    "definition": contents,
                    "urn": sense_urn,
                    "children": [],
                }
            )

    return parent_senses


def get_entries(root):
    # first div element has metadata, second div element has introduction
    for entry in root.xpath("text//entry"):
        entry_orig_id = entry.attrib["id"]
        entry_key = entry.attrib["key"]

        urn = f"{URN_PREFIX}-{entry_orig_id}"

        head = entry.attrib["key"]
        entry_type = entry.attrib["type"]

        contents = []
        for child in entry.iterchildren():
            if child.tag != "sense":
                text = child.xpath("normalize-space()")
                if text:
                    contents.append(to_string(child))
        contents = "".join(contents).strip()

        senses = get_senses(entry, urn)

        yield {
            "headword": head,
            "urn": urn,
            "definition": contents,
            "key": entry_key,
            "senses": senses,
            "type": entry_type,
        }


def check_urns(jsonl_filepath, urns={}):
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


def make_metadata(label, kind, desto_path, urn=None):
    if urn is None:
        try:
            urn = URN_PREFIX
        except TypeError:
            print("No URN provided, so no metafile has been generated.")
            return None

    entry_list = []
    for filename in sorted(desto_path.glob("*.jsonl")):
        entry_list.append(str(filename).split("/")[-1])

    metadata = {"label": label, "urn": urn, "kind": kind, "entries": entry_list}

    with open(f"{desto_path}/metadata.json", "w") as f:
        json.dump(metadata, f)

    print("metadata.json file written")


urns = {}
for filename in sorted(ELEM_LATIN_REPO.glob("*.xml")):
    tree = etree.parse(filename)
    root = tree.getroot()

    with open(f"{DESTO_DIR}/entries_001.jsonl", "w") as f:
        for entry in get_entries(root):
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")

    urns = check_urns(f"{DESTO_DIR}/entries_001.jsonl", urns)

make_metadata("Elementary Latin", "Dictionary", DESTO_DIR)
