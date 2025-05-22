from ref_to_urn import get_ref


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
