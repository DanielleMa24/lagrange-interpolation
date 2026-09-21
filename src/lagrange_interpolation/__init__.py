"""Lagrange interpolation for a set of points.

This package provides a single function, :func:`interpolate`, which
constructs and evaluates the Lagrange interpolating polynomial through a
given set of points.
"""

from .core import interpolate

__all__ = ["interpolate"]
