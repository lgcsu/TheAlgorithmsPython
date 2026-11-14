import math
from timeit import timeit


def num_digits(n: int) -> int:
    """
    Find the number of digits in a number.

    >>> num_digits(12345)
    5
    >>> num_digits(123)
    3
    >>> num_digits(0)
    1
    >>> num_digits(-1)
    1
    >>> num_digits(-123456)
    6
    >>> num_digits('123')  # Raises a TypeError for non-integer input
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")

    digits = 0
    n = abs(n)
    while True:
        n = n // 10
        digits += 1
        if n == 0:
            break
    return digits


def num_digits_fast(n: int) -> int:
    """
    Find the number of digits in a number.
    abs() is used as logarithm for negative numbers is not defined.

    The number of digits of a positive integer n is the only integer d with
    10**(d - 1) <= n < 10**d, i.e. d = floor(log10(n)) + 1. math.log10() returns a
    float, so it is only used to estimate d: just below a power of ten the
    logarithm rounds up to a whole number and the estimate is one too large.
    Comparing n with exact integer powers of ten corrects the estimate.
    https://en.wikipedia.org/wiki/Logarithm#Applications
    https://docs.python.org/3/tutorial/floatingpoint.html

    >>> num_digits_fast(12345)
    5
    >>> num_digits_fast(123)
    3
    >>> num_digits_fast(1000)
    4
    >>> num_digits_fast(10**15)
    16
    >>> num_digits_fast(0)
    1
    >>> num_digits_fast(-1)
    1
    >>> num_digits_fast(-123456)
    6
    >>> num_digits_fast(10**15 - 3)
    15
    >>> num_digits_fast(10**15 - 2)  # log10() rounds up to exactly 15.0
    15
    >>> num_digits_fast(10**15 - 1)
    15
    >>> num_digits_fast(10**16 - 1)  # float(10**16 - 1) is already 1e+16
    16
    >>> num_digits_fast(-(10**16 - 1))
    16
    >>> num_digits_fast(10**16)
    17
    >>> num_digits_fast(10**400 - 1)  # too large to be converted to a float
    400
    >>> num_digits_fast(10**400)
    401
    >>> all(num_digits_fast(10**exponent - 1) == exponent for exponent in range(1, 400))
    True
    >>> all(num_digits_fast(10**exponent) == exponent + 1 for exponent in range(400))
    True
    >>> num_digits_fast('123')  # Raises a TypeError for non-integer input
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n == 0:
        return 1
    n = abs(n)
    # log10() works in floating point, so close to a power of ten the estimate
    # can be off by one: the exact integer comparisons below correct it.
    digits = math.floor(math.log10(n)) + 1
    upper_bound = 10**digits
    while upper_bound <= n:
        digits += 1
        upper_bound *= 10
    while upper_bound // 10 > n:
        digits -= 1
        upper_bound //= 10
    return digits


def num_digits_faster(n: int) -> int:
    """
    Find the number of digits in a number.
    abs() is used for negative numbers.

    >>> num_digits_faster(12345)
    5
    >>> num_digits_faster(123)
    3
    >>> num_digits_faster(0)
    1
    >>> num_digits_faster(-1)
    1
    >>> num_digits_faster(-123456)
    6
    >>> num_digits_faster('123')  # Raises a TypeError for non-integer input
    Traceback (most recent call last):
        ...
    TypeError: Input must be an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")

    return len(str(abs(n)))


def benchmark() -> None:
    """
    Benchmark multiple functions with three different integer sizes.
    """
    from collections.abc import Callable

    def benchmark_a_function(func: Callable, value: int) -> None:
        call = f"{func.__name__}({value})"
        timing = timeit(f"__main__.{call}", setup="import __main__")
        print(f"{call}: {func(value)} -- {timing:.6f} seconds")

    for value in (262144, 1125899906842624, 1267650600228229401496703205376):
        for func in (num_digits, num_digits_fast, num_digits_faster):
            benchmark_a_function(func, value)
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
