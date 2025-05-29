#!/usr/bin/env python

import json
import pathlib

from lxml import etree

from convert_ot_cit import get_glossae, extract_citations


AUTHOR_ID = "viaf2603144"

AUTHOR_DIR = (
    pathlib.Path(__file__).parents[3] / "canonical_pdlrefwk" / "data" / AUTHOR_ID
)
TEST_DATA_DIR = pathlib.Path(__file__).parents[2] / "test-data" / "commentaries"


for path in sorted(AUTHOR_DIR.iterdir()):
    if path.is_dir() and path.name[-1].isdigit():
        for subpath in sorted(path.iterdir()):
            if subpath.name == "__cts__.xml":
                pass  # skip
            else:
                SRC_FILE = subpath
                URN_PREFIX = f"urn:cts:greekLit:{subpath.stem}"
                root = etree.parse(SRC_FILE).getroot()
                LABEL = " ".join(
                    [
                        root.xpath(
                            "//tei:titleStmt/tei:title",
                            namespaces={"tei": "http://www.tei-c.org/ns/1.0"},
                        )[0].text,
                        "by",
                        root.xpath(
                            "//tei:titleStmt/tei:author",
                            namespaces={"tei": "http://www.tei-c.org/ns/1.0"},
                        )[0].text,
                    ]
                )
                corresp = root.xpath(
                    "//*[@corresp]", namespaces={"tei": "http://www.tei-c.org/ns/1.0"}
                )
                if corresp:
                    TEXTURN = (
                        ":".join(corresp[0].attrib["corresp"].split(":")[:-1]) + ":"
                    )
                DESTO_DIR = TEST_DATA_DIR / subpath.stem

                if not DESTO_DIR.exists():
                    DESTO_DIR.mkdir(parents=True)

                with open(DESTO_DIR / "glossae_001.jsonl", "w") as f:
                    idx = 0
                    cit_counter = {"count": 0}
                    for corresp, content in get_glossae(SRC_FILE, TEXTURN):
                        idx += 1
                        citations = extract_citations(
                            content,
                            idx,
                            cit_counter,
                            urn_prefix=f"{URN_PREFIX}.perseus-eng1",
                            filename=str(subpath),
                        )
                        entry = {
                            "urn": f"{URN_PREFIX}:{idx}",
                            "corresp": corresp,
                            "content": content,
                            "citations": extract_citations(
                                content,
                                idx,
                                cit_counter,
                                urn_prefix=f"{URN_PREFIX}.perseus-eng1",
                                filename=str(subpath),
                            ),
                        }
                        print(json.dumps(entry, ensure_ascii=False), file=f)

                metadata = {
                    "label": LABEL,
                    "urn": URN_PREFIX,
                    "kind": "Commentary",
                    "entries": ["glossae_001.jsonl"],
                }

                with open(DESTO_DIR / "metadata.json", "w") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
