from __future__ import annotations

import argparse
import dataclasses
import enum
import sys
from collections.abc import Iterator
from collections.abc import Sequence
from typing import Protocol

print(sys.version_info)
if sys.version_info < (3, 11):
    from typing import NoReturn

    def assert_never(arg: NoReturn) -> None:
        raise AssertionError(arg)  # pragma: no cover
else:
    from typing import assert_never


class CaseSensitivity(enum.Enum):
    CASE_INSENSITIVE = enum.auto()
    CASE_SENSITIVE = enum.auto()


@dataclasses.dataclass(frozen=True)
class NaiveSorter:
    case: CaseSensitivity = CaseSensitivity.CASE_SENSITIVE

    class _SortFn(Protocol):
        def __call__(self, lines: Sequence[str]) -> Sequence[str]: ...

    def __call__(
            self, lines: Sequence[str],
    ) -> Iterator[str]:
        sorter: NaiveSorter._SortFn | None = None
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
                sorter = self._get_sorter(line)
                to_sort = []
                indentation = None  # not known yet

            yield line
        else:
            if sorter:  # file ended during sorting
                yield from sorter(to_sort)

    def _get_sorter(self, line: str) -> NaiveSorter._SortFn:
        _, _, options = line.rstrip().partition('# pragma: alphabetize')
        if options == '':
            if self.case is CaseSensitivity.CASE_INSENSITIVE:
                return self._case_insensitive_sort
            elif self.case is CaseSensitivity.CASE_SENSITIVE:
                return self._case_sensitive_sort
            else:
                assert_never(self.case)
        if options in {'[case-sensitive]', '[cs]'}:
            return self._case_sensitive_sort
        elif options in {'[case-insensitive]', '[ci]'}:
            return self._case_insensitive_sort
        else:
            raise ValueError(f'unrecognised options: {options!r}')

    @staticmethod
    def _case_sensitive_sort(lines: Sequence[str]) -> list[str]:
        return sorted(lines)

    @staticmethod
    def _case_insensitive_sort(lines: Sequence[str]) -> list[str]:
        return sorted(lines, key=str.casefold)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    case_mutex = parser.add_mutually_exclusive_group()
    case_mutex.set_defaults(case_sensitivity=CaseSensitivity.CASE_SENSITIVE)
    case_mutex.add_argument(
        '--case-sensitive',
        help='sort lines case-sensitively by default (default)',
        action='store_const', dest='case_sensitivity',
        const=CaseSensitivity.CASE_SENSITIVE,
    )
    case_mutex.add_argument(
        '--case-insensitive',
        help='sort lines case-insensitively by default',
        action='store_const', dest='case_sensitivity',
        const=CaseSensitivity.CASE_INSENSITIVE,
    )
    args = parser.parse_args(argv)

    sorter = NaiveSorter(case=args.case_sensitivity)

    for filename in args.filenames:
        with open(filename) as f:
            src_lines = f.readlines()

        sorted_lines = list(sorter(src_lines))

        if sorted_lines != src_lines:
            with open(filename, 'w') as f:
                f.writelines(sorted_lines)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
