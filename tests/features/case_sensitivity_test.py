from __future__ import annotations

from pathlib import Path

from sort_lines import main


def test_case_sensitivity(tmp_path: Path) -> None:
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
