#!/usr/bin/env python3

import collections
import json
import pathlib
import sys

import jsonlines

sense_urns = set()
citation_urns = set()


def process_senses(senses, error_counts):
    for sense in senses:

        if "urn" not in sense:
            error_counts["Missing sense urn"] += 1
        if "definition" not in sense:
            error_counts["Missing sense definition"] += 1

        for key in sense.keys():
            if key not in [
                "label",
                "urn",
                "definition",
                "children",
                "citations",
            ]:
                error_counts[f"Unexpected sense property '{key}'"] += 1

        if sense["urn"] in sense_urns:
            error_counts[f"Duplicate sense urn '{sense['urn']}'"] += 1
        sense_urns.add(sense["urn"])

        if "citations" in sense:
            process_citations(sense["citations"], error_counts)
        if "children" in sense:
            process_senses(sense["children"], error_counts)


def process_citations(citations, error_counts):
    for citation in citations:

        if "urn" not in citation:
            error_counts["Missing citation urn"] += 1
        if "ref" not in citation:
            error_counts["Missing citation ref"] += 1

        for key in citation.keys():
            if key not in [
                "urn",
                "ref",
                "quote",
                "target",
            ]:
                error_counts[f"Unexpected sense property '{key}'"] += 1

        if citation["urn"] in citation_urns:
            error_counts[f"Duplicate citation urn '{citation['urn']}'"] += 1
        citation_urns.add(citation["urn"])


dictionaries_path = pathlib.Path(sys.argv[1])

for dictionary_dir in dictionaries_path.iterdir():
    if not dictionary_dir.is_dir():
        continue

    print()
    print(dictionary_dir)

    metadata = json.load((dictionary_dir / "metadata.json").open())

    assert metadata.keys() == {"label", "urn", "kind", "entries"}

    assert metadata["kind"] == "Dictionary"

    for entries_filename in metadata["entries"]:

        error_counts = collections.Counter()

        try:
            entries = jsonlines.open(dictionary_dir / entries_filename)
        except FileNotFoundError:
            print(f"  Missing entries file: {entries_filename}")
            continue

        for entry in entries:
            if "urn" not in entry:
                error_counts["Missing urn"] += 1
            if "headword" not in entry:
                error_counts["Missing headword"] += 1
            if "definition" not in entry:
                error_counts["Missing definition"] += 1
            if "senses" in entry:
                process_senses(entry["senses"], error_counts)
            if "citations" in entry:
                process_citations(entry["citations"], error_counts)
            for key in entry.keys():
                if key not in [
                    "urn",
                    "headword",
                    "definition",
                    "senses",
                    "citations",
                    "key",
                    "headword_display",
                ]:
                    error_counts[f"Unexpected entry property '{key}'"] += 1

        if error_counts:
            print(f"  Errors in {entries_filename}:")
        for error, count in error_counts.items():
            print(f"    {error}: {count}")