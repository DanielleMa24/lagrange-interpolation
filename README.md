# lagrange-interpolation

A small, dependency-free Python library that constructs and evaluates the Lagrange interpolating polynomial through a given set of points.

## Usage

```python
from lagrange_interpolation import interpolate

x = [0.0, 1.0, 2.0]
y = [1.0, 2.0, 5.0]

print(interpolate(x, y, 1.5))  # 4.75
print(interpolate(x, y, [0.0, 1.0, 2.0]))  # [1.0, 2.0, 5.0]
```

## Why this library exists

Lagrange interpolation is a classic numerical method for finding a polynomial that passes exactly through a set of given data points. The polynomial is built as a weighted sum of basis polynomials, each of which is 1 at one data point and 0 at all the others. This makes the method straightforward to implement and understand, and it is exact for the provided points.

The main trade-off is numerical stability and efficiency. Each query point requires O(n^2) operations, and for large numbers of points the computed values can suffer from floating-point cancellation. This library is intended for small to moderate point sets where simplicity and clarity are more important than raw performance.

## Edge cases

- At least one interpolation point is required; an empty point set raises `ValueError`.
- The x-coordinates must be distinct; duplicates raise `ValueError`.
- The `x_query` argument may be a single number or an iterable of numbers. A single number returns a `float`, while an iterable returns a `list` of floats.
- Strings are not accepted as query values and raise `TypeError`.

## Exports

The package exports a single function:

- `interpolate(x, y, x_query)`

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

