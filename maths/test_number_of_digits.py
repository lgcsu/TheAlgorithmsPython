"""
Tests for maths/number_of_digits.py that compare the three implementations with
each other close to powers of ten, where the floating point logarithm used by
num_digits_fast() is least accurate.

Every test calls itself from its own docstring, so the assertions run under both
pytest and ``python3 -m doctest maths/test_number_of_digits.py``.
"""

from collections.abc import Callable

from maths.number_of_digits import num_digits, num_digits_fast, num_digits_faster

IMPLEMENTATIONS = (num_digits, num_digits_fast, num_digits_faster)


def raises_type_error(function: Callable[..., int], value: object) -> bool:
    """
    Report whether calling function(value) raises a TypeError.

    >>> raises_type_error(num_digits, "123")
    True
    >>> raises_type_error(num_digits, 123)
    False
    """
    try:
        function(value)
    except TypeError:
        return True
    return False


def test_implementations_agree_around_powers_of_ten() -> None:
    """
    10**exponent is the smallest number with exponent + 1 digits, so the two
    numbers below it have exponent digits and the number above it exponent + 1.

    >>> test_implementations_agree_around_powers_of_ten()
    """
    for exponent in range(1, 41):
        for offset in (-2, -1, 0, 1):
            number = 10**exponent + offset
            expected = exponent if offset < 0 else exponent + 1
            for function in IMPLEMENTATIONS:
                assert function(number) == expected, (function.__name__, number)


def test_single_digit_numbers() -> None:
    """
    Zero has no logarithm and still counts as one digit.

    >>> test_single_digit_numbers()
    """
    for number in range(10):
        for function in IMPLEMENTATIONS:
            assert function(number) == 1, (function.__name__, number)


def test_negative_numbers_mirror_positive_numbers() -> None:
    """
    The sign is not a digit: -n has as many digits as n.

    >>> test_negative_numbers_mirror_positive_numbers()
    """
    for number in (1, 9, 10, 10**15 - 2, 10**15, 10**16 - 1, 10**16, 10**20 - 1):
        for function in IMPLEMENTATIONS:
            assert function(-number) == function(number), (function.__name__, number)


def test_numbers_beyond_float_range() -> None:
    """
    float(10**400) raises an OverflowError, the digit count must still be exact.

    >>> test_numbers_beyond_float_range()
    """
    for function in IMPLEMENTATIONS:
        assert function(10**400 - 2) == 400, function.__name__
        assert function(10**400 - 1) == 400, function.__name__
        assert function(10**400) == 401, function.__name__
        assert function(10**400 + 1) == 401, function.__name__
        assert function(-(10**400 - 1)) == 400, function.__name__


def test_non_integer_input_raises_type_error() -> None:
    """
    >>> test_non_integer_input_raises_type_error()
    """
    for value in ("123", 123.0, None, [123]):
        for function in IMPLEMENTATIONS:
            assert raises_type_error(function, value), (function.__name__, value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
