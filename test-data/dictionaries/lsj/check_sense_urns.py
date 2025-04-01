import jsonlines
from pathlib import Path
from tqdm import tqdm

dir = Path.cwd()
files = dir.glob("*.jsonl")

seen_urns = []


def read_sense_urns(urn_list, sense):
    urn_list.append(sense["urn"])
    for s in sense["children"]:
        read_sense_urns(urn_list, s)


urn_to_file = {}
for file in tqdm(files):
    with jsonlines.open(file) as reader:
        for line in reader:
            buffer_list = [line["urn"]]
            for sense in line["senses"]:
                read_sense_urns(buffer_list, sense)
            for urn in buffer_list:
                if urn in set(seen_urns):
                    print(f"Matching urn is {urn}")
                    print(f"urns for entry are {buffer_list}")
                    print(f"file of current urn is {file}")
                    print(f"file of previous match is {urn_to_file[urn]}")
                    break
                else:
                    seen_urns.append(urn)
                    urn_to_file[urn] = file
