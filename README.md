# sort lines

Alphabetize lines in a file.

This tool uses leading whitespace to delimit the lines that should be alphabetized.
It is intended for use with Python code
but should work with anything that has consistent indentation.

## usage

Indicate that some lines should be alphabetized
by including a comment on the line above
(the comment must include `# pragma: alphabetize`).

```python
# names.py
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]
```

Run this tool on the file:

```shell
sort-lines names.py
```

Indentation will be used to decide which lines need to be sorted.
The first line after the `pragma` comment will set the indentation level
and every subsequent line with the same amount of indentation will be included in the sorting.
The first line with a different indentation(including blank lines) will indicate the end of the sorted lines.

## pre-commit

This tool can be used with [pre-commit](https://pre-commit.com):

```yaml
repos:
-   repo: https://github.com/samueljsb/sort-files
    rev: v0.1.0
    hooks:
    -   id: sort-files
```
