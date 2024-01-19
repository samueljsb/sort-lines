from __future__ import annotations

import argparse
from collections.abc import Iterator
from collections.abc import Sequence


def sort_lines(lines: Sequence[str]) -> Iterator[str]:
    sorting = False
    indentation: str | None = None
    to_sort: list[str] = []
    for line in lines:
        if sorting:
            if indentation is None:  # first line
                indentation = line.removesuffix(line.lstrip())
                to_sort.append(line)
                continue
            elif line and line.startswith(indentation):  # line to sort
                to_sort.append(line)
                continue
            else:  # sorting has ended
                yield from sorted(to_sort)
                sorting = False

        if '# pragma: alphabetize' in line:  # start sorting
            sorting = True
            to_sort = []
            indentation = None  # not known yet

        yield line
    else:
        if sorting:  # file ended during sorting
            yield from sorted(to_sort)


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
