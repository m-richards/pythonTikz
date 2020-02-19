# -*- coding: utf-8 -*-
"""
This module implements LaTeX base classes that can be subclassed.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
import pylatex
from .latex_object import LatexObject


class Container(pylatex.base_classes.Container, LatexObject):
    """Shallow wrapper to enable use of updated Parent class. This docstring
    is overridden in sphinx documentation.
    """

    __doc__ = pylatex.base_classes.Container.__doc__

    def get_package_sources(self):
        """Return a list of all data sources which can contain a package
        dependence.
        """
        return [self.data]


class Environment(pylatex.base_classes.Environment, Container):
    """Shallow wrapper to enable use of updated Parent class. This docstring
    is overridden in sphinx documentation.
    """

    __doc__ = pylatex.base_classes.Environment.__doc__


class ContainerCommand(Container):
    """Shallow wrapper to enable use of updated Parent class. This docstring
    is overridden in sphinx documentation.
    """

    __doc__ = pylatex.base_classes.ContainerCommand
