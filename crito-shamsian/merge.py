#!/usr/bin/env python


from collections import defaultdict


GREEK_TOKENS = {}

for line in open("greek_tokens.tsv"):
    sentence_num, token_num, token = line.strip().split("\t")
    GREEK_TOKENS[(int(sentence_num), int(token_num))] = token


def process(sentence_num, lines):
    print()
    print(f"# sent_id = {sentence_num}")
    mappings = defaultdict(list)
    pers = {}
    for line in lines:
        sentence_num, token_num, pers_token_nums, pers_tokens = line
        pers_token_nums = " ".join(pers_token_nums)
        pers_tokens = " ".join(pers_tokens)
        pers[pers_token_nums] = pers_tokens
        mappings[pers_token_nums].append(token_num)
        # print(f"{token_num}\t{pers_token_nums}\t{GREEK_TOKENS[(sentence_num, token_num)]}\t{pers_tokens}")
    for k, vs in mappings.items():
        print(" ".join(str(v) for v in vs), k, " ".join(GREEK_TOKENS[sentence_num, v] for v in vs), pers[k], sep="\t")



lines = []
for line in open("persian_token_numbering_corrected.txt"):
    if line.startswith("#"):
        if lines:
            process(sentence_num, lines)
            lines = []
        sentence_num = int(line.strip().split()[1])
    elif line.strip() == "":
        pass
    elif line.startswith("\t"):
        token_num, rest = line.strip().split(maxsplit=1)
        pers_token_nums = []
        pers_tokens = []
        for part in rest.split():
            if part.startswith("{"):
                pers_token_nums.append(part[1:-1])
            else:
                pers_tokens.append(part)
        token_num = int(token_num)
        lines.append((sentence_num, token_num, pers_token_nums, pers_tokens))
    else:
        pass
process(sentence_num, lines)