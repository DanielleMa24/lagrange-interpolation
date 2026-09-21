"""Core implementation of Lagrange interpolation.

The module exposes :func:`interpolate`, which constructs the Lagrange
interpolating polynomial for a given set of points and evaluates it at
one or more query points.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Union


def _validate_points(
    x: Sequence[float], y: Sequence[float]
) -> tuple[list[float], list[float]]:
    """Validate and normalise interpolation points.

    The function checks that both sequences have the same non-zero length,
    that all x-coordinates are distinct, and that all values are real
    numbers.  A ``ValueError`` or ``TypeError`` is raised for invalid input;
    the error message states what was wrong.

    Returns copies of the inputs as lists to avoid accidental mutation by
    the caller.
    """
    if not isinstance(x, Sequence) or not isinstance(y, Sequence):
        raise TypeError("x and y must be sequences of numbers")

    if len(x) != len(y):
        raise ValueError("x and y must have the same length")

    if len(x) == 0:
        raise ValueError("at least one interpolation point is required")

    x_list = list(x)
    y_list = list(y)

    for i, (xi, yi) in enumerate(zip(x_list, y_list)):
        if not isinstance(xi, (int, float)) or not isinstance(yi, (int, float)):
            raise TypeError(f"point {i} must contain real numbers")

    if len(set(x_list)) != len(x_list):
        raise ValueError("x-coordinates must be distinct")

    return x_list, y_list


def _lagrange_basis(
    x_points: list[float], i: int, x_query: float
) -> float:
    """Evaluate the i-th Lagrange basis polynomial at ``x_query``.

    The basis polynomial is defined as

        L_i(x) = prod_{j != i} (x - x_j) / (x_i - x_j)

    For a single query point this is the most direct and numerically stable
    form when the number of points is small.
    """
    xi = x_points[i]
    numerator = 1.0
    denominator = 1.0

    for j, xj in enumerate(x_points):
        if j == i:
            continue
        numerator *= x_query - xj
        denominator *= xi - xj

    return numerator / denominator


def interpolate(
    x: Sequence[float],
    y: Sequence[float],
    x_query: Union[float, Iterable[float]],
) -> Union[float, list[float]]:
    """Evaluate the Lagrange interpolating polynomial.

    Parameters
    ----------
    x, y :
        The interpolation nodes.  ``x`` contains the x-coordinates and ``y``
        the corresponding y-values.  Both must be sequences of real numbers
        with the same length.  The x-coordinates must be distinct.
    x_query :
        A single number or an iterable of numbers at which the interpolating
        polynomial is evaluated.

    Returns
    -------
    float or list of float
        If ``x_query`` is a single number, a ``float`` is returned.  If it is
        an iterable, a ``list`` of floats is returned, one for each query
        point, preserving the order of the iterable.

    Raises
    ------
    TypeError
        If the arguments have the wrong type.
    ValueError
        If ``x`` and ``y`` have different lengths, ``x`` is empty, or
        duplicate x-coordinates are present.

    Notes
    -----
    The implementation uses the explicit Lagrange basis polynomial for each
    query point.  It is intended for small to moderate numbers of
    interpolation nodes.  For large node sets the algorithm is O(n^2) per
    query point and may suffer from numerical instability, which is an
    inherent trade-off of this simple approach.
    """
    x_points, y_points = _validate_points(x, y)

    # A single number is not an Iterable; strings are iterable but are not
    # valid numeric input, so they are handled explicitly.
    if isinstance(x_query, str):
        raise TypeError("x_query must be a number or an iterable of numbers")

    if isinstance(x_query, (int, float)):
        queries = [float(x_query)]
        single = True
    else:
        try:
            queries = [float(q) for q in x_query]
        except TypeError as exc:
            raise TypeError(
                "x_query must be a number or an iterable of numbers"
            ) from exc
        single = False

    results = []
    for q in queries:
        value = 0.0
        for i, yi in enumerate(y_points):
            value += yi * _lagrange_basis(x_points, i, q)
        results.append(value)

    return results[0] if single else results
