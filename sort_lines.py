from __future__ import annotations

import argparse
from collections.abc import Iterator
from collections.abc import Sequence
from typing import Protocol


class Sorter(Protocol):
    def __call__(self, lines: Sequence[str]) -> Sequence[str]: ...


def _get_sorter(line: str, default_sorter: Sorter) -> Sorter:
    _, _, options = line.rstrip().partition('# pragma: alphabetize')
    if options == '':
        return default_sorter
    if options in {'[case-sensitive]', '[cs]'}:
        return _case_sensitive_sort
    elif options in {'[case-insensitive]', '[ci]'}:
        return _case_insensitive_sort
    else:
        raise ValueError(f'unrecognised options: {options!r}')


def _case_sensitive_sort(lines: Sequence[str]) -> list[str]:
    return sorted(lines)


def _case_insensitive_sort(lines: Sequence[str]) -> list[str]:
    return sorted(lines, key=str.casefold)


def sort_lines(
        lines: Sequence[str], default_sorter: Sorter = _case_sensitive_sort,
) -> Iterator[str]:
    sorter: Sorter | None = None
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
            sorter = _get_sorter(line, default_sorter)
            to_sort = []
            indentation = None  # not known yet

        yield line
    else:
        if sorter:  # file ended during sorting
            yield from sorter(to_sort)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    case_mutex = parser.add_mutually_exclusive_group()
    case_mutex.set_defaults(default_sorter=_case_sensitive_sort)
    case_mutex.add_argument(
        '--case-sensitive',
        help='sort lines case-sensitively by default (default)',
        action='store_const', dest='default_sorter', const=_case_sensitive_sort,
    )
    case_mutex.add_argument(
        '--case-insensitive',
        help='sort lines case-insensitively by default',
        action='store_const', dest='default_sorter', const=_case_insensitive_sort,
    )
    args = parser.parse_args(argv)

    for filename in args.filenames:
        with open(filename) as f:
            src_lines = f.readlines()

        sorted_lines = list(sort_lines(src_lines, default_sorter=args.default_sorter))

        if sorted_lines != src_lines:
            with open(filename, 'w') as f:
                f.writelines(sorted_lines)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
