import jsonlines
from pathlib import Path
from tqdm import tqdm

dir = Path.cwd()
n_files = len([file for file in dir.glob("*.jsonl")])
files = dir.glob("*.jsonl")

seen_urns = set([])


def read_cit_urns(urn_list, citations):
    for cit in citations:
        urn_list.append(cit["urn"])


def read_from_senses(urn_list, sense):
    if sense.get("citations"):
        for cit in sense["citations"]:
            urn_list.append(cit["urn"])
    for child in sense["children"]:
        read_from_senses(urn_list, child)


urn_to_file = {}
for file in tqdm(files, total=n_files):
    with jsonlines.open(file) as reader:
        for line in reader:
            buffer_list = [line["urn"]]
            read_cit_urns(buffer_list, line["citations"])
            for sense in line["senses"]:
                read_from_senses(buffer_list, sense)
            for urn in buffer_list:
                if urn in seen_urns:
                    print(f"Matching urn is {urn}")
                    print(f"urns for entry are {buffer_list}")
                    print(f"file of current urn is {file}")
                    print(f"file of previous match is {urn_to_file[urn]}")
                    break
                else:
                    seen_urns.add(urn)
                    urn_to_file[urn] = file
