from __future__ import annotations

from pathlib import Path

from sort_lines import main
from sort_lines import sort_lines


class TestSortLines:
    def test_sort_lines(self):
        lines = [
            '# pragma: alphabetize\n',
            'Bob\n',
            'Alice\n',
            'Eve\n',
            'David\n',
            'Charlie\n',
        ]

        sorted_lines = list(sort_lines(lines))

        assert sorted_lines == [
            '# pragma: alphabetize\n',
            'Alice\n',
            'Bob\n',
            'Charlie\n',
            'David\n',
            'Eve\n',
        ]

    def test_already_sorted(self):
        lines = [
            '# pragma: alphabetize\n',
            'Alice\n',
            'Bob\n',
            'Charlie\n',
            'David\n',
            'Eve\n',
        ]

        sorted_lines = list(sort_lines(lines))

        assert sorted_lines == lines

    def test_sorting_stops_when_indentation_changes(self):
        lines = [
            '# pragma: alphabetize\n',
            '    Bob\n',
            '    Alice\n',
            '    Eve\n',
            'David\n',
            'Charlie\n',
        ]

        sorted_lines = list(sort_lines(lines))

        assert sorted_lines == [
            '# pragma: alphabetize\n',
            '    Alice\n',
            '    Bob\n',
            '    Eve\n',
            'David\n',
            'Charlie\n',
        ]

    def test_sorting_stops_at_empty_line(self):
        lines = [
            '# pragma: alphabetize\n',
            'Bob\n',
            'Alice\n',
            'Eve\n',
            '\n',
            'David\n',
            'Charlie\n',
        ]

        sorted_lines = list(sort_lines(lines))

        assert sorted_lines == [
            '# pragma: alphabetize\n',
            'Alice\n',
            'Bob\n',
            'Eve\n',
            '\n',
            'David\n',
            'Charlie\n',
        ]


def test_file_needs_no_sorting(tmp_path: Path):
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


def test_file_already_sorted(tmp_path: Path):
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


def test_file_changed(tmp_path: Path):
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
""",
    )

    ret = main([str(file)])

    assert ret == 1
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
"""


def test_multiple_files(tmp_path: Path):
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

    assert ret == 1
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
