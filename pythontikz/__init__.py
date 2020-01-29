"""
A library for creating TikZ pictures from python.

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""


from .document import Document
from pylatex.package import Package
from pylatex.utils import NoEscape
from .tikz import TikZ, Axis, Plot, TikZNode, TikZDraw, TikZCoordinate,\
    TikZPolarCoordinate, TikZArc, TikZPathList, TikZPath, TikZUserPath, \
    TikZOptions, TikZNodeAnchor, \
    TikZScope, TikZCoordinateVariable, TikZCalcScalar, TikZLibrary, \
    TikZCoordinateBase, _TikZCoordinateImplicitCalculation, \
    _TikZCoordinateHandle

from .base_classes import Command, UnsafeCommand


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
