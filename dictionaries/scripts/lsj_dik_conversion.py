#!/usr/bin/env python

"""
Work-in-progress script to convert Helma Dik's XML of the LSJ to JSONL for Scaife ATLAS.
"""

import re
import json

from pathlib import Path
from lxml import etree
import unicodedata

LSJ_REPO = Path("../../../LSJ/dik_version")
# LSJ_REPO_DEBUG = Path("../../../LSJ/dik_version/test")
DESTO_DIR = Path("../../test-data/dictionaries/lsj")

URN_PREFIX = "urn:cite2:scaife-viewer:dictionaries.v1:lsj"


# Note: can switch between pulling xml string vs. just text by changing default value of method
# from "text" to "xml".
def to_string(el, method="xml"):
    text = etree.tostring(el, with_tail=True, encoding="utf-8", method=method).decode(
        "utf-8"
    )
    # now remove all xml tags except for italicization
    pattern = re.compile("<.+?>")
    for match in re.findall(pattern, text):
        if match != "<i>" and match != "</i>":
            text = re.sub(re.escape(match), "", text)
    return text


def latinize(char):
    mappings = {
        "α": "a",
        "β": "b",
        "γ": "g",
        "δ": "d",
        "ε": "e",
        "ζ": "z",
        "η": "h",
        "θ": "q",
        "ι": "i",
        "κ": "k",
        "λ": "l",
        "μ": "m",
        "ν": "n",
        "ξ": "c",
        "ο": "o",
        "π": "p",
        "ρ": "r",
        "σ": "s",
        "ς": "s",
        "ϲ": "s",
        "τ": "t",
        "υ": "u",
        "φ": "f",
        "χ": "x",
        "ψ": "y",
        "ω": "w",
        chr(787): ")",  # smooth breathing
        chr(788): "(",  # rough breathing
        chr(769): "/",  # acute accent
        chr(768): "\\",  # grave accent
        chr(834): "=",  # circumflex accent
        chr(837): "|",  # iota subscript
    }
    return mappings.get(char, "")


def generate_key(greek_lemma):
    key = []
    for char in greek_lemma:
        for element in unicodedata.normalize("NFD", char.lower()):
            key.append(latinize(element))
    return "".join(key)


def normalize_whitespace(text):
    if text is not None:
        # Replace multiple spaces with a single space and strip leading/trailing spaces
        return re.sub(r"\s+", " ", text).strip()
    return text


def process_citation_urn(urn: str):
    # these four lines deal with citation urns that have book and line number
    pattern = r"(,\d+:\d+)(:*)(\d*)"
    if len(re.findall(pattern, urn)) > 0 and len(re.findall(pattern, urn)[0][2]) > 0:
        replacement = r"\1.\3"
        urn = re.sub(pattern, replacement, urn)
    urn = re.sub("Perseus:abo", "urn:cts:greekLit", urn)

    # we want to replace the first "," with "" and the second "," with "."
    # we also want to insert tlg after tlg#.
    pattern = r"(.+)(,)(.+)(,)(.+)"
    replacement = r"\1\3.tlg\5"
    urn = re.sub(pattern, replacement, urn)

    # go from urn:cts:greekLit:tlg0012.tlg001:8.409
    # to urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:8.409
    pattern = r"(.+)(\.)(.+)(:)(.+)"
    replacement = r"\1\2\3.perseus-grc2\4\5"
    urn = re.sub(pattern, replacement, urn)

    return urn


def process_citations(child, counter):
    quote_parts = []
    for quote in child.xpath("quote"):
        quote_text = normalize_whitespace(to_string(quote)).strip()
        quote_parts.append(quote_text)

    quote = " ".join(quote_parts)

    bibl_entries = []
    for bibl in child.xpath("bibl"):
        urn = bibl.attrib.get("n", "")
        urn = process_citation_urn(urn)

        bibl_text = normalize_whitespace(to_string(bibl).strip())
        bibl_entries.append((bibl_text, urn))

    counter["citation_count"] += 1
    ref, ref_urn = bibl_entries[0] if len(bibl_entries) > 0 else ("", "")
    return {
        "urn": f"urn:cite2:scaife-viewer:citations.atlas_v1:lsj-{counter['citation_count']}",
        "data": {"quote": quote, "ref": ref, "urn": ref_urn},
    }


def process_sense_levels(sense, urn: str, parent_senses: list, counter: dict):
    """
    Modifies passed list parent_senses in place, adding dictionaries at top level
    for each parent_senses, with each dict having a "children" field for list of sub_senses.
    Relies on "level" attribute to infer sense hierarchy.
    """
    contents_list = []
    citations = []
    for child in sense.iterchildren():
        if child.tag == "cit":
            citations.append(process_citations(child, counter))
        # handle citations outside of "cit" tag, i.e. without quotation
        if child.tag == "bibl":
            ref = normalize_whitespace(to_string(child).strip())
            ref_urn = child.attrib.get("n", "MISSING")
            ref_urn = process_citation_urn(ref_urn)
            counter["citation_count"] += 1
            citations.append(
                {
                    "urn": f"urn:cite2:scaife-viewer:citations.atlas_v1:lsj-{counter['citation_count']}",
                    "data": {"quote": "", "ref": ref, "urn": ref_urn},
                }
            )
        text = normalize_whitespace(to_string(child))
        if text:
            contents_list.append(text)
    contents = " ".join(contents_list).strip()
    if sense.attrib.get("level") == "0" or sense.attrib.get("level") is None:
        sense_urn = f"{urn}-n{len(parent_senses)}"
        parent_senses.append(
            {
                "label": sense.attrib.get("n"),
                "definition": contents,
                "urn": sense_urn,
                "citations": citations,
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
        parent_num_children = len(parent_senses[-1]["children"])
        sense_urn = f"{parent_urn}-{parent_num_children}"
        parent_senses[-1]["children"].append(
            {
                "label": sense.attrib.get("n"),
                "definition": contents,
                "urn": sense_urn,
                "citations": citations,
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
        parent_num_children = len(parent_senses[-1]["children"][-1]["children"])
        sense_urn = f"{parent_urn}-{parent_num_children}"

        parent_senses[-1]["children"][-1]["children"].append(
            {
                "label": sense.attrib.get("n"),
                "definition": contents,
                "urn": sense_urn,
                "citations": citations,
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
        parent_num_children = len(
            parent_senses[-1]["children"][-1]["children"][-1]["children"]
        )
        sense_urn = f"{parent_urn}-{parent_num_children}"
        parent_senses[-1]["children"][-1]["children"][-1]["children"].append(
            {
                "label": sense.attrib.get("n"),
                "definition": contents,
                "urn": sense_urn,
                "citations": citations,
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

        parent_urn = parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
            "urn"
        ]
        parent_num_children = len(
            parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
                "children"
            ]
        )
        sense_urn = f"{parent_urn}-{parent_num_children}"

        parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
            "children"
        ].append(
            {
                "label": sense.attrib.get("n"),
                "definition": contents,
                "urn": sense_urn,
                "citations": citations,
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

        parent_urn = parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
            "children"
        ][-1]["urn"]
        parent_num_children = len(
            parent_senses[-1]["children"][-1]["children"][-1]["children"][-1][
                "children"
            ][-1]["children"]
        )
        sense_urn = f"{parent_urn}-{parent_num_children}"

        parent_senses[-1]["children"][-1]["children"][-1]["children"][-1]["children"][
            -1
        ]["children"].append(
            {
                "label": sense.attrib.get("n"),
                "definition": contents,
                "urn": sense_urn,
                "citations": citations,
                "children": [],
            }
        )

    return parent_senses


def get_senses(entry, urn, counter: dict):
    parent_senses = []
    for sense in entry.xpath("sense"):
        process_sense_levels(sense, urn, parent_senses, counter)
    return parent_senses


def get_entries(root, counter: dict):
    # div1 element has all entries, div2 has individual entry
    for entry in root.xpath("text//div2"):
        if not entry.attrib.get("key"):
            continue
        head = to_string(entry.xpath("head")[0]).split(",")[0].strip()
        head = head.split(" ")[0]
        entry_key = entry.attrib.get("key").strip()
        entry_type = (
            entry.attrib.get("type").strip() if entry.attrib.get("type") else None
        )
        entry_urn = f"{URN_PREFIX}-{entry.attrib['orig_id'].strip()}"
        contents = []
        citations = []
        for child in entry.iterchildren():
            if child.tag != "sense":
                text = normalize_whitespace(to_string(child))
                if text:
                    contents.append(text)
            if child.tag == "cit":
                citations.append(process_citations(child, counter))
        contents = " ".join(contents).strip()

        senses = get_senses(entry, entry_urn, counter)

        yield {
            "headword": head,
            "urn": entry_urn,
            "definition": contents,
            "citations": citations,
            "senses": senses,
            "key": entry_key,
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
counter = {"citation_count": 0}
# for filename in sorted(LSJ_REPO_DEBUG.glob("*.xml")):
for filename in sorted(LSJ_REPO.glob("*.xml")):
    tree = etree.parse(filename)
    root = tree.getroot()

    num = filename.stem[-2:]
    prev_ten_urns = []

    with open(f"{DESTO_DIR}/entries_{num}.jsonl", "w") as f:
        for entry in get_entries(root, counter):
            if entry["urn"] in set(prev_ten_urns):
                for i, id in enumerate(prev_ten_urns):
                    if entry["urn"] == id:
                        entry["urn"] += f"_{i}"

            if len(prev_ten_urns) == 10:
                del prev_ten_urns[0]
            prev_ten_urns.append(entry["urn"])
            f.write(json.dumps(entry, ensure_ascii=False))
            f.write("\n")
# Note that this does not check for duplicates accross files

for filename in sorted(DESTO_DIR.glob("*.jsonl")):
    urns = check_urns(filename, urns)
make_metadata("LSJ", "Dictionary", DESTO_DIR)
