#!/usr/bin/env python

# ultimately, we want to use some machine learning model to intelligently
# decide how to resolve ambiguous references via some sort of ML
# hoover all abbreviated citations into a file with abbreviated form and resolved form
# do this for numeric citations as well
# also have a file mapping all refs to their resolutions

import logging
from typing import Optional

from works_greek import (
    GREEK_AUTH_URNS,
    GREEK_WORK_URNS,
    GREEK_AUTH_ABB,
    GREEK_SINGLE_WORK_AUTHORS,
)
from works_latin import (
    LATIN_AUTH_URNS,
    LATIN_WORK_URNS,
    LATIN_AUTH_ABB,
    LATIN_SINGLE_WORK_AUTHORS,
)
from works_other import OTHER_AUTH_ABB, OTHER_WORK_URNS, OTHER_AUTH_URNS

# check for duplicate keys betwen greek and latin works
assert not set(GREEK_AUTH_URNS.keys()).intersection(LATIN_AUTH_URNS.keys())
assert not set(GREEK_WORK_URNS.keys()).intersection(LATIN_WORK_URNS.keys())
assert not set(GREEK_AUTH_ABB.keys()).intersection((LATIN_AUTH_ABB.keys()))

# check for duplicate keys betwen greek and other works
assert not set(GREEK_AUTH_URNS.keys()).intersection(OTHER_AUTH_URNS.keys())
assert not set(GREEK_WORK_URNS.keys()).intersection(OTHER_WORK_URNS.keys())
assert not set(GREEK_AUTH_ABB.keys()).intersection((OTHER_AUTH_ABB.keys()))

# check for duplicate keys betwen latin and other works
assert not set(LATIN_AUTH_URNS.keys()).intersection(OTHER_AUTH_URNS.keys())
assert not set(LATIN_WORK_URNS.keys()).intersection(OTHER_WORK_URNS.keys())
assert not set(LATIN_AUTH_ABB.keys()).intersection((OTHER_AUTH_ABB.keys()))

AUTH_URNS = GREEK_AUTH_URNS | LATIN_AUTH_URNS | OTHER_AUTH_URNS
AUTH_ABB = GREEK_AUTH_ABB | LATIN_AUTH_ABB | OTHER_AUTH_ABB
WORK_URNS = GREEK_WORK_URNS | LATIN_WORK_URNS | OTHER_WORK_URNS
SINGLE_WORK_AUTHORS = GREEK_SINGLE_WORK_AUTHORS.union(LATIN_SINGLE_WORK_AUTHORS)

AUTHORS = set(AUTH_URNS.keys())

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="log_ref_to_urn.log", encoding="utf-8", level=logging.DEBUG
)


def _smart_suspend(title: str, skip_de=True, join_char=".") -> str:
    func_words = {"the", "a", "an", "of", "in", "by", "for", "on", "and", "de", "ad"}
    vowels = {"a", "e", "i", "o", "u", "y"}
    plosives = {"t", "p", "d", "g", "k", "x", "c", "b"}
    suspensions = []
    title = title.replace(" ", "_")  # standardize spacing
    for word in title.split("_"):
        vowel_seen = False
        cons_last_seen = False
        if word in {"de", "on"}:
            if skip_de:
                continue
            suspensions.append(word)
            continue
        elif (
            word in func_words
        ):  # I don't think it's common to abbreviate nouns/adjective but keep these other function words
            continue
        buffer = []
        for char in word:
            if char in vowels:
                if vowel_seen and cons_last_seen:
                    break
                vowel_seen = True
                cons_last_seen = False
                buffer.append(char)
            else:
                if vowel_seen and char in plosives:
                    buffer.append(char)
                    break
                else:  # catches cases where char is consonant but not plosive, and where char is consonant at start of word
                    cons_last_seen = True
                    buffer.append(char)

        suspensions.append("".join(buffer))
    terminal = "." if join_char == "." else ""
    if suspensions[0] in {"de", "on"}:
        return suspensions[0] + "_" + join_char.join(suspensions[1:]) + terminal
    return join_char.join(suspensions) + terminal


def _transform_title(title: str, titles: list) -> list:
    prev_titles = set(titles)
    transformations = []

    if title.isnumeric():
        return []

    # latinize and anglicize one-word plural titles
    if len(title.split()) == 1:
        if title[-1] == "s":
            transformations.append(title[:-1] + "a")
        elif title[-1] == "a":
            transformations.append(title[:-1] + "s")

    initials = "".join([word[0] for word in title.split()])
    dot_initials = ".".join([word[0] for word in title.split()]) + "."
    under_initials = "_".join([word[0] for word in title.split()])
    dot_under_initials = "._".join([word[0] for word in title.split()]) + "."
    if initials not in prev_titles:
        transformations.append(initials)
    if dot_initials not in prev_titles:
        transformations.append(dot_initials)
    if under_initials not in prev_titles:
        transformations.append(under_initials)
    if dot_under_initials not in prev_titles:
        transformations.append(dot_under_initials)

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
    func_words = {"the", "a", "an", "of", "in", "by", "for", "on", "and", "de", "ad"}
    if func_words & set(title.split()):
        initials = "".join(
            [word[0] for word in title.split() if word not in func_words]
        )
        dot_initials = (
            ".".join([word[0] for word in title.split() if word not in func_words])
            + "."
        )
        under_initials = "_".join(
            [word[0] for word in title.split() if word not in func_words]
        )
        dot_under_initials = (
            "._".join([word[0] for word in title.split() if word not in func_words])
            + "."
        )
        if initials not in prev_titles:
            transformations.append(initials)
        if dot_initials not in prev_titles:
            transformations.append(dot_initials)
        if under_initials not in prev_titles:
            transformations.append(under_initials)
        if dot_under_initials not in prev_titles:
            transformations.append(dot_under_initials)

    # add transformation of title by taking suspensions
    # by going until you have (CONS* VOWEL CONS+) VOWEL, e.g. part.an. for de partibus animalium
    # note that get_urn will replace spaces with underscores before checking for known work titles
    smart_suspension = _smart_suspend(title, skip_de=True)
    if smart_suspension not in prev_titles:
        transformations.append(smart_suspension)

    smart_suspension = _smart_suspend(title, skip_de=False)
    if smart_suspension not in prev_titles:
        transformations.append(smart_suspension)

    if len(title.split()) > 1:
        underscored = title.replace(" ", "_")
        if underscored not in prev_titles:
            transformations.append(underscored)

    return list(set(transformations))


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


def get_urn(
    ref: str, content: Optional[str] = None, filename: Optional[str] = None
) -> str:
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
            if content:
                assert len(work_loc.split(".", maxsplit=1)) == 2, (
                    f"wrong format for citation ref: {content}\n\nfor ref {ref}\n\nin file {filename}"
                )
            else:
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
                if content:
                    assert len(work_loc.split(".", maxsplit=1)) == 2, (
                        f"wrong format for citation ref: {content}\nfor ref {ref}\n\nin file {filename}"
                    )
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
        assert auth, (
            f"Author not recognized for: {ref}\ncitation content, if provided, is: {content}"
        )

    auth_urn = AUTH_URNS[auth]

    # deal with authors known solely/primary from single work,
    # so that they are cited without ref to specific work
    # note that given the ambiguity in references of the form "#.#",
    # this can't handle an author sometimes being cited without work reference when
    # citation is to their best known work, and sometimes being cited with work refernce
    # when to other works. It's better to standardize the xml in this case
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
            Issue with the work name or the passage citation with {ref}.
            loc is {loc}.
        """
        work_number, loc = loc.split(".", maxsplit=1)
        work = work + "_" + work_number
        work_urn = WORK_URNS[auth].get(work)

    if not work_urn:
        logging.warning(f"Work not recognized for {ref}")
    # assert work_urn, f"Work not recognized for {ref}"

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
        logging.warning(f"""
        "warning: incorrectly formatted citation urn. 
        {urn}
        """)
    return urn


if __name__ == "__main__":
    # run module as script to output a text file with all
    # title forms and author abbreviations, both as specified explicitly
    # and as automatically generated
    with open("title_forms.txt", "w") as f:
        for auth in WORK_URNS.keys():
            f.write(f"___{auth}___\n")
            auth_abb_list = []
            for auth_form in AUTH_ABB.keys():
                # this assumes dictionary keys are in alphabetic order
                if auth_form[0] > auth[0]:
                    break
                if AUTH_ABB[auth_form] == auth:
                    auth_abb_list.append(auth_form)
            f.write(f"Author abbreviations: {','.join(auth_abb_list)}\n")
            f.write("Title forms:\n")
            for title_form in WORK_URNS[auth].keys():
                f.write(f"{title_form}\n")
