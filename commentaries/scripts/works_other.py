OTHER_AUTH_ABB = {
    "shakesp.": "shakespeare",
    "shaksp.": "shakespeare",
    "shak.": "shakespeare",
    "shak": "shakespeare",
}

OTHER_WORK_URNS = {
    "milton": {
        "paradise lost": "pl",
        "par. lost.": "pl",
    },
    "shakespeare": {
        "all's well that ends well": "aww",
        "antony and cleopatra": "ant",
        "as you like it": "ayl",
        "the comedy of errors": "err",
        "coriolanus": "cor",
        "cymbeline": "cym",
        "edward iii": "edw",  # not perseus abb
        "hamlet": "ham",
        "julius caesar": "jc",
        "king henry iv. part i": "1h4",
        "king henry iv. part ii": "2h4",
        "king henry v": "h5",
        "king henry vi. part i.": "1h6",
        "king henry vi. part ii.": "2h6",
        "king henry vi. part iii.": "3h6",
        "king henry viii.": "h8",
        "king john": "jn",
        "king lear": "lr",
        "a lover's complaint": "lc",  # not perseus abb
        "love's labor's lost": "lll",
        "lear": "lr",
        "macbeth": "mac",
        "Measure for Measure": "mm",
        "the merchant of venice": "mv",
        "the merry wives of windsor": "wiv",
        "a midsummer night's dream": "mnd",
        "much ado about nothing": "ado",
        "othello": "oth",
        "the passionate pilgrim": "pp",
        "pericles prince of tyre": "per",
        "the phoenix and the turtle": "pht",
        "the rape of lucrece": "luc",
        "richard ii": "r2",
        "richard iii": "r3",
        "romeo and juliet": "rom",
        "sir thomas more": "stm",  # not perseus abb
        "sonnets": "son",
        "the taming of the shrew": "shr",
        "the tempest": "tmp",
        "timon of athens": "tim",
        "titus andronicus": "tit",
        "troilus and cressida": "tro",
        "twelfth night": "tn",
        "two gentlemen of verona": "tgv",
        "the two noble kinsmen": "tnk",  # not perseus abb
        "venus and adonis": "ven",
        "a winter's tale": "wt",
    },
}

# since the urn stems for shakespeare works are themselves abbreviations
# for the works, add them to keys
abbreviations = OTHER_WORK_URNS["shakespeare"].copy()
abbreviations = abbreviations.values()
for val in abbreviations:
    OTHER_WORK_URNS["shakespeare"][val] = val

OTHER_AUTH_URNS = {
    "shakespeare": "urn:cts:englishLit:shak",
    "milton": "urn:tcs:englishLit:milt",
}
