from __future__ import annotations

import argparse
from collections.abc import Callable
from collections.abc import Iterator
from collections.abc import Sequence


def _get_sorter(line: str) -> Callable[[Sequence[str]], Sequence[str]]:
    _, _, options = line.rstrip().partition('# pragma: alphabetize')
    if options in {'', '[case-sensitive]', '[cs]'}:
        return _case_sensitive_sort
    elif options in {'[case-insensitive]', '[ci]'}:
        return _case_insensitive_sort
    else:
        raise ValueError(f'unrecognised options: {options!r}')


def _case_sensitive_sort(lines: Sequence[str]) -> list[str]:
    return sorted(lines)


def _case_insensitive_sort(lines: Sequence[str]) -> list[str]:
    return sorted(lines, key=str.casefold)


def sort_lines(lines: Sequence[str]) -> Iterator[str]:
    sorter: Callable[[Sequence[str]], Sequence[str]] | None = None
    indentation: str | None = None
    to_sort: list[str] = []
    for line in lines:
        if sorter:
            if indentation is None:  # first line
                indentation = line.removesuffix(line.lstrip())
                to_sort.append(line)
                continue
            elif line.strip() and line.startswith(indentation):  # line to sort
                to_sort.append(line)
                continue
            else:  # sorting has ended
                yield from sorter(to_sort)
                sorter = None

        if '# pragma: alphabetize' in line:  # start sorting
            sorter = _get_sorter(line)
            to_sort = []
            indentation = None  # not known yet

        yield line
    else:
        if sorter:  # file ended during sorting
            yield from sorter(to_sort)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    ret = 0
    for filename in args.filenames:
        with open(filename) as f:
            src_lines = f.readlines()

        sorted_lines = list(sort_lines(src_lines))

        if sorted_lines != src_lines:
            with open(filename, 'w') as f:
                f.writelines(sorted_lines)

            ret |= 1

    return ret


if __name__ == '__main__':
    raise SystemExit(main())
