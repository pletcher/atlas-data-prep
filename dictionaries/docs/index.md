# Dictionaries in Scaife

## Overview

Marked-up dictionaries typically have very rich information but a lot of use can be made of dictionaries even if much of this markup is ignored by the reading environment. At a most basic level, all that is needed is to retrieve an entry by headword and then render the entry. However it is often useful to be able to distinguish different senses of a word. There may be citations in an entry and it would also be nice to allow the opening of a text cited in a dictionary entry. Texts may be lemmatized, which in this context means a link from a token to a dictionary entry can be determined. There may also be word sense disambiguation either at a token level or at least at a text level which allows determination of a link from a token to a specific sense within an entry. If entries or senses have citations, a different type of link can be determined from a chunk or token to an entry or sense. Entries may have alternative lemmas (either explicitly given or determined through some normalization process) for situations where the lemmatization of a text does not match a particular choice of headword in a particular dictionary.

In short, the following capabilities may exist depending on the data available:

* retrieval of an entry by headword or alternative / normalized lemma
* retrieval of a particular sense within entry
* opening a text from a citation in an entry
* navigate from a lemmatized token to a dictionary entry
* navigate from a word-sense-disambiguated token to a dictionary entry sense
* determine which tokens in a lemmatized text are covered by a dictionary
* determine which chunks or tokens in a lemmatized text are cited in a dictionary entry

## The Data Format for Ingestion

For ingestion into ATLAS, a dictionary is laid out in a directory with a `metadata.json` file containing overall metadata about the dictionary and then one or more `jsonl` files containing the entries themselves.

### Metadata File

The `metadata.json` gives the dictionary a label and urn along with what the entry files are. The file typically looks something like this:

```
{
    "kind": "Dictionary",
    "label": "My Dictionary",
    "urn": "urn:cite2:scaife-viewer:dictionaries.v1:my-dictionary",
    "entries": [
      "entries-001.jsonl",
      "entries-002.jsonl",
    ]
}
```

### Entries

In the entry `jsonl` files, each line is a JSON object. At a minimum, the entry object should contain a `headword`, `urn`, and a `data` object containing `content`.

```
{"headword": "μῆνις", "data": {"content": "wrath, anger"}, "urn": "urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:short-def-56795"}
```

Here is the equivalent entry in the Cambridge Greek Lexicon (without senses or citations):

```
{
  "headword": "μῆνις",
  "urn": "urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:cambridge-greek-lexicon-26128"
  "data": {
    "headword_display": "<b>μῆνις</b>",
    "content": "<NE><HG><HL>μῆνις</HL><DL><Lbl>dial.</Lbl><FmHL>μᾶνις</FmHL></DL><Infl>ιος</Infl><PS>f</PS></HG> <nS1><Def>resentful or vengeful anger</Def><Tr>anger, wrath<Expl>of persons, gods, the spirits of the dead, or sim.</Expl></Tr><Au>Hom. Hes. Thgn. Lyr. Hdt. Trag.<NBPlus/></Au><nS2><Indic>pl.</Indic><Au>AR.</Au></nS2><nS2><Indic>personif.</Indic><Tr>Wrath</Tr><Au>A.</Au></nS2></nS1></NE>",
    "key": "μῆνις"
  },
}
```

Here, a custom CSS stylesheet has to be applied to render the content. The `key` exists because more than one entry may have the same headword. For example, in the Cambridge Greek Lexicon there are two "headword": "μήν". They have "headword_display": "<b>μήν</b><sup>1</sup>" and "headword_display": "<b>μήν</b><sup>2</sup>" but also "key": "μήν_1" and "key": "μήν_2".


And here is a truncated version of the Cunliffe entry where senses and citations are included.

Notice here the top-level properties include `senses` and `citations` lists.

Senses have a `label`, `urn`, `definition` and `citations`.

Citations have a `urn` and `data` object consisting of `ref` and optional `quote` and `urn` properties.


```
    {
      "headword": "μῆνις",
      "urn": "urn:cite2:exploreHomer:entries.atlas_v1:1.6424",
      "data": {
        "content": "<p>ἡ.</p>"
      },
      "senses": [
        {
          "label": "1",
          "urn": "urn:cite2:exploreHomer:senses.atlas_v1:1.13168",
          "definition": "Wrath, ire :",
          "citations": [
            {
              "urn": "urn:cite2:scholarlyEditions:citations.v1:1.13168_1",
              "data": {
                "ref": "Il. 1.1",
                "quote": "μῆνιν ἄειδε Ἀχιλῆος",
                "urn": "urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:1.1"
              }
            },
            {
              "urn": "urn:cite2:scholarlyEditions:citations.v1:1.13168_2",
              "data": {
                "ref": "Il. 1.75",
                "quote": null,
                "urn": "urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:1.75"
              }
            }
          ]
        },
        {
          "label": "2",
          "urn": "urn:cite2:exploreHomer:senses.atlas_v1:1.13169",
          "definition": "The operation or effect of wrath :",
          "citations": [ … ]
        }
      ]
    }
```

Note that this format is subject to change and feedback is very welcome.
