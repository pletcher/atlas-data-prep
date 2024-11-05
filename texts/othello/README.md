# Othello Example

This assumes that `canonical-engLit` branch `p6` is checked out adjacent to this repo.

`./convert_othello.py` processes the XML for Othello and produces two files:
- `othello-text.tsv` contains the text chunks with reference numbers in a TSV format
- `othello-text.jsonl` contains annotations tied to reference numbers (this includes speaker, chunk kind, stage direction type, and line part)

Information which is currently thrown away but could be included:

- `castList`
- `lb`

Still to do:

- a `metadata.json` for overall metadata
