"""
A library for creating TikZ pictures from python.

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""


from .document import Document
from pylatex.package import Package
from pylatex.utils import NoEscape
from .common import (TikZ, TikZOptions, TikZLibrary, TikZScope, Plot, Axis,
                     TikZNodeAnchor)
from .positions import (TikZCoordinate, TikZPolarCoordinate,
                        TikZCoordinateVariable, TikZCoordinateBase,
                        TikZCalcScalar, _TikZCoordinateHandle,
                        _TikZCoordinateImplicitCalculation, TikZNode, )
from .paths import (TikZPath, TikZPathList, TikZUserPath, TikZDraw, TikZArc)
from .base_classes import Command, UnsafeCommand


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
