from __future__ import annotations

import pytest

from sort_lines import CaseSensitivity
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
