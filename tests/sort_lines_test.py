from __future__ import annotations

from pathlib import Path

import pytest

from sort_lines import CaseSensitivity
from sort_lines import main
from sort_lines import NaiveSorter


class TestNaiveSorter_GetSorter:
    @pytest.mark.parametrize(
        'line',
        (
            # bare pragma
            '# pragma: alphabetize\n',
            'some_values = [  # pragma: alphabetize\n',
        ),
    )
    @pytest.mark.parametrize(
        ('case_sensitivity', 'expected_sorter'),
        (
            pytest.param(
                CaseSensitivity.CASE_INSENSITIVE, NaiveSorter._case_insensitive_sort,
                id='case-insensitive',
            ),
            pytest.param(
                CaseSensitivity.CASE_SENSITIVE, NaiveSorter._case_sensitive_sort,
                id='case-sensitive',
            ),
        ),
    )
    def test_default_sorter(
        self, case_sensitivity: CaseSensitivity, line: str, expected_sorter: object,
    ) -> None:
        sorter = NaiveSorter(case=case_sensitivity)._get_sorter(line)
        assert sorter is expected_sorter

    @pytest.mark.parametrize(
        'line',
        (
            # 'case-insensitive' option
            '# pragma: alphabetize[case-sensitive]\n',
            'some_values = [  # pragma: alphabetize[case-sensitive]\n',
            # 'ci' option
            '# pragma: alphabetize[cs]\n',
            'some_values = [  # pragma: alphabetize[cs]\n',
        ),
    )
    def test_case_sensitive(self, line: str) -> None:
        sorter = NaiveSorter()._get_sorter(line)
        assert sorter is NaiveSorter._case_sensitive_sort

    @pytest.mark.parametrize(
        'line',
        (
            # 'case-insensitive' option
            '# pragma: alphabetize[case-insensitive]\n',
            'some_values = [  # pragma: alphabetize[case-insensitive]\n',
            # 'ci' option
            '# pragma: alphabetize[ci]\n',
            'some_values = [  # pragma: alphabetize[ci]\n',
        ),
    )
    def test_case_insensitive(self, line: str) -> None:
        sorter = NaiveSorter()._get_sorter(line)
        assert sorter is NaiveSorter._case_insensitive_sort

    def test_unknown_options(self) -> None:
        with pytest.raises(
            ValueError,
            match=r"unrecognised options: '\[sort-lines\]'",
        ):
            NaiveSorter()._get_sorter('# pragma: alphabetize[sort-lines]\n')


class TestNaiveSorter:
    def test_sort_lines(self) -> None:
        lines = [
            '# pragma: alphabetize\n',
            'Bob\n',
            'Alice\n',
            'Eve\n',
            'David\n',
            'Charlie\n',
        ]

        sort = NaiveSorter()
        sorted_lines = list(sort(lines))

        assert sorted_lines == [
            '# pragma: alphabetize\n',
            'Alice\n',
            'Bob\n',
            'Charlie\n',
            'David\n',
            'Eve\n',
        ]

    def test_case_insensitive(self) -> None:
        lines = [
            '# pragma: alphabetize[case-insensitive]\n',
            'Bob\n',
            'alice\n',
            'eve\n',
            'David\n',
            'charlie\n',
        ]

        sort = NaiveSorter()
        sorted_lines = list(sort(lines))

        assert sorted_lines == [
            '# pragma: alphabetize[case-insensitive]\n',
            'alice\n',
            'Bob\n',
            'charlie\n',
            'David\n',
            'eve\n',
        ]

    def test_already_sorted(self) -> None:
        lines = [
            '# pragma: alphabetize\n',
            'Alice\n',
            'Bob\n',
            'Charlie\n',
            'David\n',
            'Eve\n',
        ]

        sort = NaiveSorter()
        sorted_lines = list(sort(lines))

        assert sorted_lines == lines

    def test_sorting_stops_when_indentation_changes(self) -> None:
        lines = [
            '# pragma: alphabetize\n',
            '    Bob\n',
            '    Alice\n',
            '    Eve\n',
            'David\n',
            'Charlie\n',
        ]

        sort = NaiveSorter()
        sorted_lines = list(sort(lines))

        assert sorted_lines == [
            '# pragma: alphabetize\n',
            '    Alice\n',
            '    Bob\n',
            '    Eve\n',
            'David\n',
            'Charlie\n',
        ]

    def test_sorting_stops_at_empty_line(self) -> None:
        lines = [
            '# pragma: alphabetize\n',
            'Bob\n',
            'Alice\n',
            'Eve\n',
            '\n',
            'David\n',
            'Charlie\n',
        ]

        sort = NaiveSorter()
        sorted_lines = list(sort(lines))

        assert sorted_lines == [
            '# pragma: alphabetize\n',
            'Alice\n',
            'Bob\n',
            'Eve\n',
            '\n',
            'David\n',
            'Charlie\n',
        ]


def test_file_needs_no_sorting(tmp_path: Path) -> None:
    file = tmp_path / 't.py'
    file.write_text(
        """\
# a list to keep unsorted
families = [
    'Wren',
    'Lark',
    'Tarrk',
]
""",
    )

    ret = main([str(file)])

    assert ret == 0
    assert file.read_text() == """\
# a list to keep unsorted
families = [
    'Wren',
    'Lark',
    'Tarrk',
]
"""


def test_file_already_sorted(tmp_path: Path) -> None:
    file = tmp_path / 't.py'
    file.write_text(
        """\
# a list already sorted
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]

# a list to keep unsorted
families = [
    'Wren',
    'Lark',
    'Tarrk',
]
""",
    )

    ret = main([str(file)])

    assert ret == 0
    assert file.read_text() == """\
# a list already sorted
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]

# a list to keep unsorted
families = [
    'Wren',
    'Lark',
    'Tarrk',
]
"""


def test_file_changed(tmp_path: Path) -> None:
    file = tmp_path / 't.py'
    file.write_text(
        """\
# a list already sorted
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]

# a list to keep unsorted
families = [
    'Wren',
    'Lark',
    'Tarrk',
]

# a list to sort
animals = [  # pragma: alphabetize
    'Tiger',
    'Hyena'
    'Elephant',
    'Lion',
]

# a list to sort with default sorting (case-sensitive)
scientists = [  # pragma: alphabetize
    'von Neumann',
    'Mandelbrot'
    'Cantor',
    'Willbanks',
]

# a list to sort case-sensitive
scientists = [  # pragma: alphabetize[case-sensitive]
    'Cantor',
    'von Neumann',
    'Mandelbrot'
    'Willbanks',
]

# a list to sort case-insensitive
scientists = [  # pragma: alphabetize[case-insensitive]
    'von Neumann',
    'Mandelbrot'
    'Cantor',
    'Willbanks',
]
""",
    )

    ret = main([str(file)])

    assert ret == 0
    assert file.read_text() == """\
# a list already sorted
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]

# a list to keep unsorted
families = [
    'Wren',
    'Lark',
    'Tarrk',
]

# a list to sort
animals = [  # pragma: alphabetize
    'Elephant',
    'Hyena'
    'Lion',
    'Tiger',
]

# a list to sort with default sorting (case-sensitive)
scientists = [  # pragma: alphabetize
    'Cantor',
    'Mandelbrot'
    'Willbanks',
    'von Neumann',
]

# a list to sort case-sensitive
scientists = [  # pragma: alphabetize[case-sensitive]
    'Cantor',
    'Mandelbrot'
    'Willbanks',
    'von Neumann',
]

# a list to sort case-insensitive
scientists = [  # pragma: alphabetize[case-insensitive]
    'Cantor',
    'Mandelbrot'
    'von Neumann',
    'Willbanks',
]
"""


def test_case_insensitive(tmp_path: Path) -> None:
    file = tmp_path / 't.txt'
    file.write_text(
        """\
# a list already sorted
names:  # pragma: alphabetize
    Alice
    Bob
    Charlie
    David
    Eve

# a list to keep unsorted
families:
    Wren
    Lark
    Tarrk

# a list to sort
animals:  # pragma: alphabetize
    Tiger
    Hyena
    Elephant
    Lion

# a list to sort with default sorting (case-insensitive)
scientists:  # pragma: alphabetize
    von Neumann
    Mandelbrot
    Cantor
    Willbanks

# a list to sort case-sensitive
scientists:  # pragma: alphabetize[case-sensitive]
    von Neumann
    Mandelbrot
    Cantor
    Willbanks

# a list to sort case-insensitive
scientists:  # pragma: alphabetize[case-insensitive]
    von Neumann
    Mandelbrot
    Cantor
    Willbanks
""",
    )

    ret = main([str(file), '--case-insensitive'])

    assert ret == 0
    assert file.read_text() == """\
# a list already sorted
names:  # pragma: alphabetize
    Alice
    Bob
    Charlie
    David
    Eve

# a list to keep unsorted
families:
    Wren
    Lark
    Tarrk

# a list to sort
animals:  # pragma: alphabetize
    Elephant
    Hyena
    Lion
    Tiger

# a list to sort with default sorting (case-insensitive)
scientists:  # pragma: alphabetize
    Cantor
    Mandelbrot
    von Neumann
    Willbanks

# a list to sort case-sensitive
scientists:  # pragma: alphabetize[case-sensitive]
    Cantor
    Mandelbrot
    Willbanks
    von Neumann

# a list to sort case-insensitive
scientists:  # pragma: alphabetize[case-insensitive]
    Cantor
    Mandelbrot
    von Neumann
    Willbanks
"""


def test_multiple_files(tmp_path: Path) -> None:
    unchanged_file = tmp_path / 'unchanged.py'
    unchanged_file.write_text(
        """\
# a list already sorted
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]
""",
    )
    changed_file = tmp_path / 'changed.py'
    changed_file.write_text(
        """\
# a list to sort
animals = [  # pragma: alphabetize
    'Tiger',
    'Hyena'
    'Elephant',
    'Lion',
]
""",
    )

    ret = main([str(unchanged_file), str(changed_file)])

    assert ret == 0
    assert unchanged_file.read_text() == """\
# a list already sorted
names = [  # pragma: alphabetize
    'Alice',
    'Bob',
    'Charlie',
    'David',
    'Eve',
]
"""
    assert changed_file.read_text() == """\
# a list to sort
animals = [  # pragma: alphabetize
    'Elephant',
    'Hyena'
    'Lion',
    'Tiger',
]
"""
