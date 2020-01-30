"""
A library for creating TikZ pictures from python.

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""


from .document import Document
from pylatex.package import Package
from pylatex.utils import NoEscape
from .common import (TikzPicture, TikzOptions, TikzLibrary, TikzScope, Plot,
                     Axis, TikzAnchor)
from .positions import (TikzRectCoord, TikzPolCoord,
                        TikzCalcCoord, BaseTikzCoord,
                        TikZCalcScalar, _TikZCalcCoordHandle,
                        _TikzCalcImplicitCoord, TikzNode, )
from .paths import (TikzPath, TikzPathList, TikzUserPath, TikzDraw, TikzArc)
from .base_classes import Command, UnsafeCommand

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

# Backwards compatible names for the existing TikZ classes
Tikz = TikzPicture
TikzNodeAnchor = TikzAnchor
TikzCoordinate = TikzRectCoord
