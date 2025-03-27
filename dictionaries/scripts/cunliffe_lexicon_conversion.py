#!/usr/bin/env python

"""
Work-in-progress script to convert XML of the cunliffe lexicon to JSONL for Scaife ATLAS.
"""

import re
import json

from pathlib import Path
from lxml import etree
import unicodedata

CUNLIFFE_REPO = Path("../../../cunliffe-lexentries")
# CUNLIFFE_REPO_DEBUG = Path("../../../cunliffe_lex/dik_version/test")
DESTO_DIR = Path("../../test-data/dictionaries/cunliffe-1-lex")

URN_PREFIX = "urn:cite2:scaife-viewer:dictionaries.v1:cunliffe_lex"

nsmap = {"ns": "http://www.tei-c.org/ns/1.0"}


def to_string(el, method="xml", to_remove=[], with_tail=True):
    text = (
        etree.tostring(el, with_tail=with_tail, encoding="utf-8", method=method)
        .decode("utf-8")
        .strip()
    )
    if method != "xml":
        return text
    # remove unwanted elements
    for tag in to_remove:
        pattern = re.compile(f"<{tag}.+?{tag}>")
        text = re.sub(pattern, "", text)
    # now remove all xml tags except for italicization
    pattern = re.compile("<.+?>")
    for matched in re.findall(pattern, text):
        if matched != "<i>" and matched != "</i>":
            if not re.match(r"<.*?corr.*?>", matched):
                text = text.replace(matched, "")
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
    # get eveything between <bibl ...> and </bibl> in ref property.
    # Ignore <ref> elements.
    # Currently, this does not yield any "quote" property.
    quote_parts = []
    ref = None
    ref_urn = None
    for quote in child.xpath(".//ns:quote", namespaces=nsmap):
        quote_text = normalize_whitespace(to_string(quote))
        quote_parts.append(quote_text)

    quote = " ".join(quote_parts)

    for bibl in child.xpath(".//ns:bibl", namespaces=nsmap):
        ref_urn = process_citation_urn(bibl.attrib["n"])

        # to get format work_urn:cited_book.cited_line
        # so from Helma's format
        # Perseus:abo:tlg,0012,001:8:409
        # we want urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:8.409

        ref = normalize_whitespace(to_string(bibl))

    citation = (
        {
            "urn": f"urn:cite2:scaife-viewer:citations.atlas_v1:cunliffe_lex-{counter['citation_count']}",
            "data": {"quote": quote, "ref": ref, "urn": ref_urn},
        }
        if ref and ref_urn
        else None
    )
    if ref and ref_urn:
        counter["citation_count"] += 1

    return citation


def get_entries(root, counter: dict):
    # div1 element has all entries, div has individual entry
    for entry in root.xpath("//ns:body/ns:div", namespaces=nsmap):
        head = (
            to_string(entry.xpath("ns:head", namespaces=nsmap)[0]).split(",")[0].strip()
        )
        head = head.split(" ")[0]
        entry_key = generate_key(head)
        entry_type = (
            entry.attrib.get("type").strip() if entry.attrib.get("type") else None
        )
        entry_urn = f"{URN_PREFIX}-n{counter['entry_count']}"
        counter["entry_count"] += 1
        contents = []
        for child in entry.iterchildren():
            if child.tag != "sense":
                text = normalize_whitespace(to_string(child))
                if text:
                    contents.append(text)
        contents = " ".join(contents).strip()

        citations = []

        for child in entry.iterdescendants():
            if child.tag == f"{{{nsmap['ns']}}}cit":
                citations.append(process_citations(child, counter))

        yield {
            "headword": head,
            "urn": entry_urn,
            "definition": contents,
            "citations": citations,
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


if __name__ == "__main__":
    urns = {}
    counter = {"entry_count": 0, "citation_count": 0}
    # for filename in sorted(CUNLIFFE_REPO_DEBUG.glob("*.xml")):
    for filename in sorted(CUNLIFFE_REPO.glob("*.xml")):
        tree = etree.parse(filename)
        root = tree.getroot()

        num = 1
        prev_ten_urns = []

        with open(f"{DESTO_DIR}/entries_{num:02d}.jsonl", "w") as f:
            num += 1
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
    make_metadata("cunliffe_lex", "Dictionary", DESTO_DIR)
