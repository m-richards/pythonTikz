"""
Baseclasses that can be used to create classes representing LaTeX objects.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from pylatex.base_classes.latex_object import LatexObject
from pylatex.base_classes.containers import Container, Environment, \
    ContainerCommand
from .command import CommandBase, Command, UnsafeCommand, Options, \
    SpecialOptions, Arguments
from pylatex.base_classes.float import Float

# Old names of the base classes for backwards compatibility
BaseLaTeXClass = LatexObject
BaseLaTeXContainer = Container
BaseLaTeXNamedContainer = Environment
