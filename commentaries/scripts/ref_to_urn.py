#!/usr/bin/env python

# ultimately, we want to use some machine learning model to intelligently
# decide how to resolve ambiguous references via some sort of ML
# hoover all abbreviated citations into a file with abbreviated form and resolved form
# do this for numeric citations as well
# also have a file mapping all refs to their resolutions

import logging
from typing import Optional
import re

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


def get_ref(from_n: Optional[str] = None, from_bibl: Optional[str] = None) -> str:
    """
    Takes in string contents of bibl element within cit element, as well as
    string contents of attribute "n" of bibl element,
    compares them, evaluates which better fits the desired citation format,
    cleans this string, and returns it. Returns None if no viable ref found.
    """
    if isinstance(from_n, str):
        from_n = from_n.lower().strip()
    if isinstance(from_bibl, str):
        from_bibl = from_bibl.lower().strip()

    # early return conditions
    if not isinstance(from_bibl, str) or not from_bibl.strip():
        assert isinstance(from_n, str)
        return from_n
    elif not isinstance(from_n, str) or not from_n.strip():
        assert isinstance(from_bibl, str)
        return from_bibl

    # process in list form to apply same operations to both from_bibl and from_n
    refs = [from_n, from_bibl]
    refs = [re.sub("<title.*?>", "", ref) for ref in refs]
    refs = [ref.replace("</title>", "") for ref in refs]
    # deal with section symbols
    refs = [re.sub(r" *§ *", ".", ref) for ref in refs]
    # deal with spacing issues with alphabetic page/section references (e.g. with Stephanus pages)
    refs = [re.sub(r"(\d+) ([A-Za-z])", r"\1\2", ref) for ref in refs]
    from_n, from_bibl = refs

    # check if at least one string begins with the best case
    # where we have at least 2 alphabetic strings followed by two numeric strings
    # this can get refs of format Dion. Hal. Rom. ant. 2.2, with author and work as bigrams
    best_pattern = (
        r"([a-zA-Z]+\.?\s?[a-zA-Z]*) ([a-zA-Z]+\.?\s?[a-zA-Z]*) \d+(\s|\.|:)\d+"
    )
    # second_best has two strings followed by one numeric string
    second_best = r"([a-zA-Z]+\.?\s?[a-zA-Z]*) ([a-zA-Z]+\.?\s?[a-zA-Z]*) \d+"
    # third_best has one alphabetic string followed by two numeric strings,
    # and captures cases where the work is given by a numeral
    third_best = r"([a-zA-Z]+\.?) \d+(\s|\.|:)\d+"
    # This captures something like Bion 20, where Bion can be presumed to ref to
    # his main surviving work, the Lament for Adonis, and 20 to he line number
    fourth_best = r"([a-zA-Z]+\.?) \d+"

    patterns = (best_pattern, second_best, third_best, fourth_best)
    ref = None

    # the basic idea here is:
    # we take the best pattern, and if a given pattern matches from_n and from_n has
    # a recognized author, we from_n. If not, we do the same check on from_bibl, and if it
    # matches, we return from_bibl. We then do the same for the other patterns in order.
    # If no pattern matches, we instead simply try to identify an author in one of
    # from_n and from_bibl.

    for pattern in patterns:
        if re.search(pattern, from_n):
            split = from_n.split()
            # check that author is recognized, up to trigram
            if AUTH_ABB.get(split[0]) or split[0] in AUTHORS:
                ref = from_n
                break
            elif AUTH_ABB.get(" ".join(split[:2])) or " ".join(split[:2]) in AUTHORS:
                ref = from_n
                break
            elif AUTH_ABB.get(" ".join(split[:3])) or " ".join(split[:3]) in AUTHORS:
                ref = from_n
                break
        # at this point, we know that from_n either does not fit pattern, or has unrecognized author
        # so we do the same check on from_bibl
        if re.search(pattern, from_bibl):
            split = from_bibl.split()
            # check that author is recognized, up to trigram
            if AUTH_ABB.get(split[0]) or split[0] in AUTHORS:
                ref = from_bibl
                break
            elif AUTH_ABB.get(" ".join(split[:2])) or " ".join(split[:2]) in AUTHORS:
                ref = from_bibl
                break
            elif AUTH_ABB.get(" ".join(split[:3])) or " ".join(split[:3]) in AUTHORS:
                ref = from_bibl
                break

    # organized this way so more checks could easily be added
    if ref:
        return ref

    # at this point, none of the desired patterns have been recognized
    # check if either or both strings have a recognized author
    n_auth_rec = False
    bibl_auth_rec = False
    auth_form_from_n = ""  # so we can try to match work
    auth_form_from_bibl = ""

    split = from_n.split()
    if AUTH_ABB.get(split[0]) or split[0] in AUTHORS:
        n_auth_rec = True
        auth_form_from_n = split[0]
    elif AUTH_ABB.get(" ".join(split[:2])) or " ".join(split[:2]) in AUTHORS:
        n_auth_rec = True
        auth_form_from_n = " ".join(split[:2])
    elif AUTH_ABB.get(" ".join(split[:3])) or " ".join(split[:3]) in AUTHORS:
        n_auth_rec = True
        auth_form_from_n = " ".join(split[:3])

    split = from_bibl.split()
    if AUTH_ABB.get(split[0]) or split[0] in AUTHORS:
        bibl_auth_rec = True
        auth_form_from_bibl = split[0]
    elif AUTH_ABB.get(" ".join(split[:2])) or " ".join(split[:2]) in AUTHORS:
        bibl_auth_rec = True
        auth_form_from_bibl = " ".join(split[:2])
    elif AUTH_ABB.get(" ".join(split[:3])) or " ".join(split[:3]) in AUTHORS:
        bibl_auth_rec = True
        auth_form_from_bibl = " ".join(split[:3])

    if n_auth_rec and not bibl_auth_rec:
        return from_n
    if bibl_auth_rec and not n_auth_rec:
        return from_bibl

    # if both have a recognized author, determine which has a recognized work
    if n_auth_rec and bibl_auth_rec:
        if auth_form_from_n in AUTHORS:
            auth = auth_form_from_n
        else:
            auth = AUTH_ABB.get(auth_form_from_n, "")
        split = from_n[len(auth_form_from_n) :].split()
        auth_space = WORK_URNS.get(auth)
        if auth_space:
            # check for work up to trigram
            if len(split) > 0 and auth_space.get(split[0]):
                return from_n
            elif len(split) > 1 and auth_space.get(" ".join(split[:2])):
                return from_n
            elif len(split) > 2 and auth_space.get(" ".join(split[:3])):
                return from_n

        if auth_form_from_bibl in AUTHORS:
            auth = auth_form_from_bibl
        else:
            auth = AUTH_ABB.get(auth_form_from_bibl, "")
        split = from_bibl[len(auth_form_from_bibl) :].split()
        auth_space = WORK_URNS.get(auth)
        if auth_space:
            # check for work up to trigram
            if len(split) > 0 and auth_space.get(split[0]):
                return from_bibl
            elif len(split) > 1 and auth_space.get(" ".join(split[:2])):
                return from_bibl
            elif len(split) > 2 and auth_space.get(" ".join(split[:3])):
                return from_bibl

    error_msg = (
        f"Problem where n attribute is\n{from_n}\nand bibl element is\n{from_bibl}\n"
    )
    assert isinstance(ref, str), error_msg
    # this line should be unreachable
    return ref


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

        # there are various cases where the ref at this point has more than three words
        # one is where the title of the work has multiple words, which is addressed by thecking
        # if the possible multiple word titles are known words and replacing replevant spaces with underscores
        if len(ref.split()) > 3:
            auth = AUTH_ABB.get(ref.split()[0].lower(), ref.split()[0]).lower()
            # iterate through work titles of two words and more
            for i in range(3, len(ref)):
                if WORK_URNS[auth].get("_".join(ref.split()[1:i]).lower()):
                    ref = ref.replace(
                        " ".join(ref.split()[1:i]), "_".join(ref.split()[1:i])
                    )
                break
            # now, deal with cases where there are spaces between digits giving location in text
            ref = re.sub(r"(?<=\d\.) (?=\d)", "", ref)
        assert len(ref.split()) in (2, 3), f"""
            wrong format for citation ref: {ref}\n
            citation content, if available, is: {content}\n
            filename, if available, is: {filename}
        """

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
    elif "englishLit" in auth_urn:
        urn = f"{auth_urn}.{work_urn}.perseus-eng2:{loc}"
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
