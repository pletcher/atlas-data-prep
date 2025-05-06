# values must have no white space
LATIN_AUTH_ABB = {
    "plaut.": "plautus",
    "tac.": "tacitus",
    "verg.": "vergil",
}


# note: multiword titles have spaces replaced with "_"
# # titles with spaces replaced with "_" are automatically added to WORK_URNS
LATIN_WORK_URNS = {
    "plautus": {
        "trinummus": "phi019",
    },
    "tacitus": {
        "agricola": "phi001",
    },
    "vergil": {
        "eclogues": "phi001",
        "georgics": "phi002",
        "aeneid": "phi003",
    },
}

# surely the more general point is that if there is no work name then the ref should resolve to tlg001

LATIN_SINGLE_WORK_AUTHORS = {}

LATIN_AUTH_URNS = {
    "plautus": "urn:cts:latinLit:phi0119",
    "tacitus": "urn:cts:latinLit:phi1351",
    "vergil": "urn:cts:latinLit:phi0690",
}
