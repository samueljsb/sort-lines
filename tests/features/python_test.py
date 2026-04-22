from __future__ import annotations

from pathlib import Path

from sort_lines import main


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
