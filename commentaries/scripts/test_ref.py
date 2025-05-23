from ref_to_urn import get_ref, get_urn


def test_get_ref():
    n = "HH 29"
    bibl = "HH 29.2"
    assert get_ref(n, bibl) == bibl.lower(), get_ref(n, bibl)


def test_pref_n():
    n = "HH 29.2"
    bibl = "HH 29.2"
    assert get_ref(n, bibl) == n.lower(), get_ref(n, bibl)


def test_best_pattern():
    n = "Hom. Od. 4.66"
    bibl = "Od. 4.66"
    assert get_ref(n, bibl) == n.lower(), get_ref(n, bibl)


def test_second_best():
    n = "Hom. Od. 4"
    bibl = "Hom. Od."
    assert get_ref(n, bibl) == n.lower(), get_ref(n, bibl)


def test_third_best():
    n = "Hom. 1.5"
    bibl = "Hom. 1"
    assert get_ref(n, bibl) == n.lower(), get_ref(n, bibl)


def test_fourth_best():
    n = "Hom."
    bibl = "Hom. 1"
    assert get_ref(n, bibl) == bibl.lower(), get_ref(n, bibl)


def test_pref_recog_auth():
    n = "Hrmrm. Od."
    bibl = "Hom. Od."
    assert get_ref(n, bibl) == bibl.lower(), get_ref(n, bibl)


def test_pref_recog_work():
    n = "Hom. Simpsons"
    bibl = "Hom. Od."
    assert get_ref(n, bibl) == bibl.lower(), get_ref(n, bibl)


def test_schol_work():
    n = None
    bibl = "Bekker <title>Anecd.</title> 325. 13"
    assert get_ref(n, bibl) == "bekker anecd. 325. 13", get_ref(n, bibl)


def test_primary_work():
    n = None
    bibl = "(dionys. periegetes 1006)"
    ref = get_ref(n, bibl)
    urn = get_urn(ref)
    assert urn == "urn:cts:greekLit:tlg0084.tlg001.perseus-grc2:1006", urn


def test_detect_urn():
    n = "tlg5037.tlg006 72"
    bibl = "schol."
    ref = get_ref(n, bibl)
    urn = get_urn(ref)
    assert urn == "urn:cts:greekLit:tlg5037.tlg006.perseus-grc2:72", urn
