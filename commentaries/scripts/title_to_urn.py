#!/usrt/bin/env python

# values must have no white space
AUTH_ABB = {
    "aesch.": "aeschylus",
    "aeschin.": "aeschines",
    "andoc.": "andocides",
    "antiph.": "antiphon",
    "aristoph.": "aristophanes",
    "aristot.": "aristotle",
    "athen.": "athenaeus",
    "callim.": "callimachus",
    "dem.": "demosthenes",
    "dio chrys.": "dio",
    "dio chrysostom": "dio",
    "diog. laert.": "diogenes",
    "d.l.": "diogenes",
    "dion. hal.": "dionysius",
    "dionysius of halicarnassus": "dionysius",
    "eur.": "euripides",
    "eustath.": "eustathius",
    "hdt.": "herodotus",
    "hes.": "hesiod",
    "hesych.": "hesychius",
    "hh": "homeric hymns",
    "h.h.": "homeric hymns",
    "hippoc.": "hippocrates",
    "hom.": "homer",
    "isae.": "isaeus",
    "isoc.": "isocrates",
    "luc.": "lucian",
    "lys.": "lysias",
    "menand.": "menander",
    "paus.": "pausanias",
    "pind.": "pindar",
    "plat.": "plato",
    "plaut.": "plautus",
    "polyb.": "polybius",
    "plut.": "plutarch",
    "sext. emp.": "sextus",
    "sextus empiricus": "sextus",
    "sext.": "sextus",
    "soph.": "sophocles",
    "strab.": "strabo",
    "tac.": "tacitus",
    "theocr.": "theocritus",
    "thuc.": "thucydides",
    "tyrt.": "tyrtaeus",
    "verg.": "vergil",
    "xen.": "xenophon",
    "shaksp.": "shakespeare",
}


# note: multiword titles have spaces replaced with "_"
# # titles with spaces replaced with "_" are automatically added to WORK_URNS
WORK_URNS = {
    "aeschines": {
        "against timarchus": "tlg001",
        "on the embassy": "tlg002",
        "against ctesiphon": "tlg003",
        "epistulae": "tlg004",
    },
    "aeschylus": {
        "suppliant maidens": "tlg001",
        "persians": "tlg002",
        "prometheus bound": "tlg003",
        "seven against thebes": "tlg004",
        "agamemnon": "tlg005",
        "choephoroi": "tlg006",
        "libation bearers": "tlg006",
        "eumenidies": "tlg007",
        "fragmenta": "tlg008",
        "fragmentum": "tlg009",
        "epigrammata": "tlg010",
        "fragmenta (tgf)": "tlg011",
    },
    "andocides": {
        "de mysteriis": "tlg001",
    },
    "antiphon": {
        "against the stepmother for poisoning": "tlg001",
        "first tetralogy": "tlg002",
        "second tetralogy": "tlg003",
        "third tetralogy": "tlg004",
        "on the murder of herodes": "tlg005",
        "on the choreutes": "tlg006",
        "fragmenta": "tlg007",
    },
    "aristophanes": {
        "acharnians": "tlg001",
        "knights": "tlg002",
        "clouds": "tlg003",
        "wasps": "tlg004",
        "peace": "tlg005",
        "birds": "tlg006",
        "lysistrata": "tlg007",
        "thesmophoriazusae": "tlg008",
        "frogs": "tlg009",
        "ecclesiazusae": "tlg010",
        "plutus": "tlg011",
        "fragmenta": "tlg013",
        "aristophanis cantica": "tlg030",
    },
    "aristotle": {
        "on the soul": "tlg002",
        "soul": "tlg002",
        "de anima": "tlg002",
        "de an.": "tlg002",
        "nicomachean ethics": "tlg010",
        "nic. eth.": "tlg010",
        "historia animalium": "tlg014",
        "hist. an.": "tlg014",
        "meteorologica": "tlg026",
        "rhetoric": "tlg038",
        "topica": "tlg044",
    },
    "bion": {
        "epitaphius adonis": "tlg001",
        "epithalamium achillis et deidameiae": "tlg002",
        "fragmenta": "tlg003",
        "idyll.": "idyll",
    },
    "callimachus": {
        "epigrams": "tlg003",
        "epigrams, fragmenta": "tlg004",
        "aetia": "tlg006",
        "iambi": "tlg007",
        "hecale": "tlg009",
        "epigrammata fragmenta": "tlg011",
        "hymn to zeus": "tlg015",
        "zeus": "tlg015",
        "hymn to apollo": "tlg016",
        "apollo": "tlg016",
        "hymn to artemis": "tlg017",
        "artemis": "tlg017",
        "hymn to delos": "tlg018",
        "delos": "tlg018",
        "hymn to athena": "tlg019",
        "athena": "tlg019",
        "hymn to demeter": "tlg020",
        "demeter": "tlg020",
    },
    "demosthenes": {
        "on the false embassy": "tlg019",
    },
    "dionysius": {
        "antiquitates romanae": "tlg001",
        "de antiquis oratoribus": "tlg002",
    },
    "hesiod": {
        "theogony": "tlg001",
        "works and days": "tlg002",
        "shield of heracles": "tlg003",
        "fragmenta": "tlg004",
        "testimonia": "tlg005",
        "fragmenta astronomica": "tlg006",
    },
    "hippocrates": {
        "de prisca medicina": "tlg001",
        "de aere aquis et locis": "tlg002",
        "prognosticon": "tlg003",
        "de diaeta in morbis acutis": "tlg004",
        "de diaeta acutorum": "tlg005",
        "de morbis popularibus": "tlg006",
        "de capitis vulneribus": "tlg007",
        "de officina medici": "tlg008",
        "de fracturis": "tlg009",
        "de articulis": "tlg010",
        "vectiarius": "tlg011",
        "aphorismi": "tlg012",
        "jusjurandum": "tlg013",
        "lex": "tlg014",
        "de morbo sacro": "tlg027",
        "de ulceribus": "tlg028",
        "de haemorrhoidibus": "tlg029",
        "de fistulis": "tlg030",
        "de alimento": "tlg046",
        "praeceptiones": "tlg051",
        "epistulae": "tlg055",
    },
    "homer": {"iliad": "tlg001", "odyssey": "tlg002", "epigrammata": "tlg003"},
    "homeric hymns": {
        "hymn 1 to dionysus": "tlg001",
        "dionysus": "tlg001",
        "hymn 2 to demeter": "tlg002",
        "demeter": "tlg002",
        "hymn 3 to apollo": "tlg003",
        "apollo": "tlg003",
        "hymn 4 to hermes": "tlg004",
        "hermes": "tlg004",
        "hymn 5 to aphrodite": "tlg005",
        "hymn 6 to aphrodite": "tlg006",
        "hymn 7 to dionysus": "tlg007",
        "hymn 8 to ares": "tlg008",
        "hymn 9 to artemis": "tlg009",
        "hymn 10 to aphrodite": "tlg010",
        "hymn 11 to athena": "tlg011",
        "athena": "tlg011",
        "hymn 12 to hera": "tlg012",
        "hera": "tlg012",
        "hymn 13 to demeter": "tlg013",
        "hymn 14 to the mother of the gods": "tlg014",
        "mother of the gods": "tlg014",
        "hymn 15 to heracles": "tlg015",
        "heracles": "tlg015",
        "hymn 16 to asclepius": "tlg016",
        "asclepius": "tlg016",
        "hymn 17 to the dioscuri": "tlg017",
        "dioscuri": "tlg017",
        "hymn 18 to hermes": "tlg018",
        "hymn 19 to pan": "tlg019",
        "pan": "tlg019",
        "hymn 20 to hephaestus": "tlg020",
        "hephaetus": "tlg020",
        "hymn 21 to apollo": "tlg021",
        "hymn 22 to poseidon": "tlg022",
        "poseidon": "tlg022",
        "hymn 23 to zeus": "tlg023",
        "zeus": "tlg023",
        "hymn 24 to hestia": "tlg024",
        "hestia": "tlg024",
        "hymn 25 to the muses and apollo": "tlg025",
        "hymn 26 to dionysus": "tlg026",
        "hymn 27 to artemis": "tlg027",
        "hymn 28 to athena": "tlg028",
        "hymn 29 to hestia": "tlg029",
        "hymn 30 to earth": "tlg030",
        "hymn 31 to helios": "tlg031",
        "helios": "tlg031",
        "hymn to selene": "tlg032",
        "selene": "tlg032",
        "hymn 33 to the dioscuri": "tlg033",
    },
    "euripides": {
        "cyclops": "tlg001",
        "alcestis": "tlg002",
        "medea": "tlg003",
        "heraclidae": "tlg004",
        "heraclid.": "tlg004",
        "hippolytus": "tlg005",
        "andromache": "tlg006",
        "hecuba": "tlg007",
        "suppliants": "tlg008",
        "supplices": "tlg008",
        "heracles": "tlg009",
        "ion": "tlg010",
        "trojan women": "tlg011",
        "trojades": "tlg011",
        "troiades": "tlg011",
        "electra": "tlg012",
        "iphigeneia in taurus": "tlg013",
        "iphigeneia in tauris": "tlg013",
        "helen": "tlg014",
        "phoenician women": "tlg015",
        "orestes": "tlg016",
        "bacchae": "tlg017",
        "iphigeneia in aulis": "tlg018",
        "rhesus": "tlg019",
        "fragmenta (tgf)": "tlg020",
        "fragmenta papyacea. cretum": "tlg021",
        "epinicium in alcibiadem": "tlg022",
        "fragments phaethontis": "tlg023",
        "fragmenta alexandri": "tlg025",
        "hypsiples fragmenta": "tlg026",
        "fragmenta phrixei": "tlg027",
        "fragmenta fabulae incertae": "tlg028",
        "fragmenta oenei": "tlg030",
        "epigrammata": "tlg031",
    },
    "isaeus": {
        "apollodorus": "tlg007",
    },
    "isocrates": {
        "ad alexandrum": "tlg028",
        "helen": "tlg009",
        "ad timotheum": "tlg026",
        "letter 7": "tlg026",
    },
    "lucian": {
        "hippias": "tlg002",
        "symposium": "tlg015",
        "iuppiter trageodeus": "tlg018",
        "juppiter trageodeus": "tlg018",
        "iupp. trag.": "tlg018",
        "jupp. trag.": "tlg018",
        "icaromenippus": "tlg021",
        "dialogi mortuorum": "tlg066",
        "dial. mort.": "tlg066",
        "dialogi deorum": "tlg068",
        "dial. deor.": "tlg068",
        "dial. d.": "tlg068",
    },
    "lysias": {
        "against eratosthenes": "tlg012",
    },
    "menander": {
        "dyscolus": "tlg007",
        "sententiae e codicibus byzantinis": "tlg042",
        "sententiae": "tlg024",
        "samia": "tlg029",
    },
    "pindar": {
        "olympia": "tlg001",
        "pythia": "tlg002",
        "nemea": "tlg003",
        "isthmea": "tlg004",
        "fragmenta": "tlg005",
    },
    "plato": {
        "euthyphro": "tlg001",
        "euthyph.": "tlg001",
        "apology": "tlg002",
        "crito": "tlg003",
        "phaedo": "tlg004",
        "cratylus": "tlg005",
        "theaetetus": "tlg006",
        "sophist": "tlg007",
        "statesman": "tlg008",
        "parmenides": "tlg009",
        "philebus": "tlg010",
        "symposium": "tlg011",
        "phaedrus": "tlg012",
        "alcibiades 1": "tlg013",
        "alc. 1": "tlg013",
        "alcibiades 2": "tlg014",
        "alc. 2": "tlg014",
        "hipparchus": "tlg015",
        "lovers": "tlg016",
        "theages": "tlg017",
        "charmides": "tlg018",
        "laches": "tlg019",
        "lysis": "tlg020",
        "euthydemus": "tlg021",
        "protagoras": "tlg022",
        "gorgias": "tlg023",
        "meno": "tlg024",
        "greater hippias": "tlg025",
        "hippias major": "tlg025",
        "hipp. maj.": "tlg025",
        "lesser hippias": "tlg026",
        "hippias minor": "tlg026",
        "hippias min.": "tlg026",
        "hipp. min.": "tlg026",
        "ion": "tlg027",
        "menexenus": "tlg028",
        "cleitophon": "tlg029",
        "republic": "tlg030",
        "timaeus": "tlg031",
        "critias": "tlg032",
        "minos": "tlg033",
        "laws": "tlg34",
        "epinomis": "tlg035",
        "letters": "tlg036",
        "definitiones": "tlg037",
        "spuria": "tlg038",
        "eryxias": "tlg038",
        "axiochus": "tlg038",
        "epigrammata": "tlg039",
    },
    "plautus": {
        "trinummus": "phi019",
    },
    "plutarch": {
        "theseus": "tlg001",
        "pericles": "tlg012",
        "aristeides": "tlg024",
        "alexander": "tlg047",
        "tiberius gracchus": "tlg052",
        "tib. gracch.": "tlg052",
        "demosthenes": "tlg054",
        "dem.": "tlg054",
        "artaxerxes": "tlg064",
        "moralia": "moralia",
    },
    "shakespeare": {
        "<title>macbeth</title>": "macbeth",
    },
    "sextus": {
        "pyrrhoniae hypotyposes": "tlg001",
        "adversus mathematicos": "tlg002",
        "adv. math.": "tlg002",
    },
    "sophocles": {
        "trachiniae": "tlg001",
        "antigone": "tlg002",
        "ajax": "tlg003",
        "oedipus tyrannus": "tlg004",
        "oedipus rex": "tlg004",
        "electra": "tlg005",
        "philoctetes": "tlg006",
        "oedipus at colonus": "tlg007",
        "oedipus coloneus": "tlg007",
        "ichneutai": "tlg008",
        "fragmenta (elegiaca)": "tlg009",
    },
    "tacitus": {
        "agricola": "phi001",
    },
    "theocritus": {
        "idylls": "tlg001",
        "epigrams": "tlg002",
    },
    "thucydides": {
        "history of the peloponnesian war": "tlg001",
        "epigramma": "tlg002",
    },
    "vergil": {
        "eclogues": "phi001",
        "georgics": "phi002",
        "aeneid": "phi003",
    },
    "xenophon": {  # note: epistles have different auth urn
        "hellenica": "tlg001",
        "memorabilia": "tlg002",
        "economics": "tlg003",
        "symposium": "tlg004",
        "apology": "tlg005",
        "anabasis": "tlg006",
        "cyropedia": "tlg007",
        "hiero": "tlg008",
        "agesilaus": "tlg009",
        "constitution of the lacedaimonians": "tlg010",
        "ways and means": "tlg011",
        "on the cavalry commander": "tlg012",
        "on the art of horsemanship": "tlg013",
        "on hunting": "tlg014",
        "constitution of the athenians": "tlg015",
    },
}

SINGLE_WORK_AUTHORS = {
    "athenaeus",
    "dio",
    "diogenes",  # laertius
    "eustathius",
    "herodotus",
    "hesychius",  # the grammarian
    "pausanias",
    "polybius",
    "strabo",
    "tyrtaeus",
}

AUTH_URNS = {
    "thucydides": "urn:cts:greekLit:tlg0003",
    "theocritus": "urn:cts:greekLit:tlg0005",
    "euripides": "urn:cts:greekLit:tlg0006",
    "plutarch": "urn:cts:greekLit:tlg0007",
    "athenaeus": "urn:cts:greekLit:tlg0008",
    "isocrates": "urn:cts:greekLit:tlg0010",
    "sophocles": "urn:cts:greekLit:tlg0011",
    "homer": "urn:cts:greekLit:tlg0012",
    "homeric hymns": "urn:cts:greekLit:tlg0013",
    "demosthenes": "urn:cts:greekLit:tlg0014",
    "diogenes": "urn:cts:greekLit:tlg0004",
    "herodotus": "urn:cts:greekLit:tlg0016",
    "isaeus": "urn:cts:greekLit:tlg0017",
    "aristophanes": "urn:cts:greekLit:tlg0019",
    "hesiod": "urn:cts:greekLit:tlg0020",
    "aeschines": "urn:cts:greekLit:tlg0026",
    "andocides": "urn:cts:greekLit:tlg0027",
    "antiphon": "urn:cts:greekLit:tlg0028",
    "xenophon": "urn:cts:greekLit:tlg0032",
    "pindar": "urn:cts:greekLit:tlg0033",
    "bion": "urn:cts:greekLit:tlg0036",
    "plato": "urn:cts:greekLit:tlg0059",
    "lucian": "urn:cts:greekLit:tlg0062",
    "dionysius": "urn:cts:greekLit:tlg0081",
    "aeschylus": "urn:cts:greekLit:tlg0085",
    "aristotle": "urn:cts:greekLit:tlg0086",
    "strabo": "urn:cts:greekLit:tlg0099",
    "tyrtaeus": "urn:cts:greekLit:tlg0266",
    "pausanias": "urn:cts:greekLit:tlg0525",
    "callimachus": "urn:cts:greekLit:tlg0533",
    "lysias": "urn:cts:greekLit:tlg0540",
    "menander": "urn:cts:greekLit:tlg0541",
    "polybius": "urn:cts:greekLit:tlg0543",
    "sextus": "urn:cts:greekLit:tlg0544",
    "dio": "urn:cts:greekLit:tlg0612",
    "hippocrates": "urn:cts:greekLit:tlg0627",
    "eustathius": "urn:cts:greekLit:tlg4083",
    "plautus": "urn:cts:latinLit:phi0119",
    "tacitus": "urn:cts:latinLit:phi1351",
    "vergil": "urn:cts:latinLit:phi0690",
    "hesychius": "urn:cts:greekLit:hesychius",  # placeholder urn since none has been minted
    "shakespeare": "urn:cts:englishLit:shakespare",
}

AUTHORS = set(AUTH_URNS.keys())


def _transform_title(title: str, titles: list) -> list:
    prev_titles = set(titles)
    transformations = []

    if title.isnumeric():
        return []

    initials = "".join([word[0] for word in title.split()])
    dot_initials = ".".join([word[0] for word in title.split()])
    if initials not in prev_titles:
        transformations.append(initials)
    if dot_initials not in prev_titles:
        transformations.append(dot_initials)

    first_letter = title[0]
    if first_letter not in prev_titles:
        transformations.append(first_letter)
    if f"{first_letter}." not in prev_titles:
        transformations.append(f"{first_letter}.")
    first_two = title[:2]
    if first_two not in prev_titles:
        transformations.append(first_two)
    if f"{first_two}." not in prev_titles:
        transformations.append(f"{first_two}.")
    if len(title.split()[0]) > 2:
        first_three = title[:3]
        if first_three not in prev_titles:
            transformations.append(first_three)
        if f"{first_three}." not in prev_titles:
            transformations.append(f"{first_three}.")
    if len(title.split()[0]) > 3:
        first_four = title[:4]
        if first_four not in prev_titles:
            transformations.append(first_four)
        if f"{first_four}." not in prev_titles:
            transformations.append(f"{first_four}.")
    if len(title.split()[0]) > 4:
        first_five = title[:5]
        if first_five not in prev_titles:
            transformations.append(first_five)
        if f"{first_five}." not in prev_titles:
            transformations.append(f"{first_five}.")
    if len(title.split()[0]) > 5:
        first_six = title[:6]
        if first_six not in prev_titles:
            transformations.append(first_six)
        if f"{first_six}." not in prev_titles:
            transformations.append(f"{first_six}.")

    if len(title.split()) > 1:
        first_word = title.split()[0]
        if first_word not in prev_titles:
            transformations.append(first_word)

    # deal with function words
    func_words = {"the", "a", "an", "of", "in", "by", "for", "on", "and"}
    if func_words & set(title.split()):
        initials = "".join(
            [word[0] if word not in func_words else "" for word in title.split()]
        )
        dot_initials = ".".join(
            [word[0] if word not in func_words else "" for word in title.split()]
        )
        if initials not in prev_titles:
            transformations.append(initials)
        if dot_initials not in prev_titles:
            transformations.append(dot_initials)

    if len(title.split()) > 1:
        underscored = title.replace(" ", "_")
        if underscored not in prev_titles:
            transformations.append(underscored)

    return transformations


additions = {}

for author in WORK_URNS.keys():
    for title in WORK_URNS[author].keys():
        prev_titles = list(additions.get(author, {}).keys()) + list(
            WORK_URNS[author].keys()
        )
        for transform in _transform_title(title, prev_titles):
            if not additions.get(author):
                additions[author] = {transform: WORK_URNS[author][title]}
            else:
                additions[author][transform] = WORK_URNS[author][title]

for author in additions.keys():
    for title in additions[author].keys():
        WORK_URNS[author][title] = additions[author][title]


def get_urn(ref: str) -> str:
    # for now, keep ff in references to line numbers,
    # but remove " " and "." to make it easier to process
    if ref[-2:] == "ff":
        if ref[-3] == " ":
            ref = ref[:-3] + ref[-2:]
    elif ref[-3:] == "ff.":
        if ref[-4] == " ":
            ref = ref[:-4] + "ff"
        else:
            ref = ref[:-3] + "ff"

    # deal with bigram author designations, e.g. Dion. Hal.
    if " ".join(ref.lower().split()[:2]) in AUTHORS or AUTH_ABB.get(
        " ".join(ref.lower().split()[:2])
    ):
        auth = AUTH_ABB.get(" ".join(ref.lower().split()[:2]))
        if not auth:
            auth = " ".join(ref.split()[:2])
            assert auth in AUTHORS, (
                f"Issue dealing with bigram author designation in {ref}"
            )
        ref = ref.replace(" ".join(ref.split()[:2]), auth)
        # deal with work titles with spaces
        new_ref = ref
        for i, term in enumerate(ref.split()[1:]):
            if term[0].isnumeric():
                break
            if i > 0:
                term_index = new_ref.index(term)
                new_ref = new_ref[: term_index - 1] + "_" + new_ref[term_index:]

        ref = new_ref

        assert len(ref.split()) in (2, 3), f"wrong format for citation ref: {ref}"

        if len(ref.split()) == 2:
            work_loc = ref.split()[1]
            assert len(work_loc.split(".", maxsplit=1)) == 2, (
                f"wrong format for citation ref: {ref}"
            )
            work, loc = work_loc.split(".", maxsplit=1)
        else:
            work, loc = ref.split()[1:]

    else:
        # deal with work titles with spaces
        new_ref = ref
        for i, term in enumerate(ref.split()[1:]):
            if term[0].isnumeric():
                break
            if i > 0:
                term_index = new_ref.index(term)
                new_ref = new_ref[: term_index - 1] + "_" + new_ref[term_index:]
        ref = new_ref

        if len(ref.split()) > 3:
            auth = AUTH_ABB.get(ref.split()[0].lower(), ref.split()[0]).lower()
            if WORK_URNS[auth].get("_".join(ref.split()[1:3]).lower()):
                ref = ref.replace(
                    " ".join(ref.split()[1:3]), "_".join(ref.split()[1:3])
                )
        assert len(ref.split()) in (2, 3), f"wrong format for citation ref: {ref}"

        if len(ref.split()) == 2:
            auth, work_loc = ref.split()
            if AUTH_ABB.get(auth.lower(), auth) in SINGLE_WORK_AUTHORS:
                work = ""
                loc = work_loc
            else:
                assert len(work_loc.split(".", maxsplit=1)) == 2, (
                    f"wrong format for citation ref: {ref}"
                )
                work, loc = work_loc.split(".", maxsplit=1)
        else:
            auth, work, loc = ref.split()

    auth = auth.lower()
    work = work.lower()

    if auth not in AUTHORS:
        auth = AUTH_ABB.get(auth)
        assert auth, f"Author not recognized for: {ref}"

    auth_urn = AUTH_URNS[auth]

    if auth in SINGLE_WORK_AUTHORS:
        assert "greekLit" in auth_urn, f"""
        "warning: incorrectly formatted citation urn. 
        {ref}
        """
        urn = f"{auth_urn}.tlg001.perseus-grc2:{'.'.join([work, loc])}"
        return urn

    work_urn = WORK_URNS[auth].get(work)
    if not work_urn and work.isnumeric():
        if "tlg" in auth_urn:
            prefix = "tlg"
        elif "phi" in auth_urn:
            prefix = "phi"
        else:
            prefix = ""

        if work[0] == "0":
            work_urn = f"{prefix}{work}"
        else:
            work_urn = f"{prefix}0{work}"

    # deal with cases like Isoc. Letter 7.7,
    # where "Letter 7" identifies the work urn
    elif not work_urn:
        assert len(loc.split(".", maxsplit=1)) == 2, f"""
            Issue with the work name or the passage citation with {ref}
        """
        work_number, loc = loc.split(".", maxsplit=1)
        work = work + "_" + work_number
        work_urn = WORK_URNS[auth].get(work)

    assert work_urn, f"Work not recognized for {ref}"
    if "greekLit" in auth_urn:
        urn = f"{auth_urn}.{work_urn}.perseus-grc2:{loc}"
    elif "latinLit" in auth_urn:
        urn = f"{auth_urn}.{work_urn}.perseus-lat2:{loc}"
    else:
        urn = f"{auth_urn}.{work_urn}:{loc}"
        print(f"""
        "warning: incorrectly formatted citation urn. 
        {urn}
        """)
    return urn
