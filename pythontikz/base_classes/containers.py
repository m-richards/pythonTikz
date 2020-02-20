# -*- coding: utf-8 -*-
"""
This module implements LaTeX base classes that can be subclassed.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
import pylatex
from .latex_object import LatexObject


class Container(LatexObject, pylatex.base_classes.Container):
    """Shallow wrapper to enable use of updated Parent class. This docstring
    is overridden in sphinx documentation.
    """

    __doc__ = pylatex.base_classes.Container.__doc__

    def dumps_packages(self):
        r"""Represent the packages needed as a string in LaTeX syntax.

        Returns
        -------
        string:
            A LaTeX string representing the packages of the container
        """

        self._propagate_packages()

        return super().dumps_packages()

    def _get_dependency_sources(self):
        """Return a list of all data sources which can contain a package
        dependence.
        """
        return super()._get_dependency_sources() + [self.data]


class Environment(pylatex.base_classes.Environment, Container):
    """Shallow wrapper to enable use of updated Parent class. This docstring
    is overridden in sphinx documentation.
    """

    __doc__ = pylatex.base_classes.Environment.__doc__

    def _get_dependency_sources(self):
        return (super()._get_dependency_sources()
                + [self.options, self.arguments, self.start_arguments])


class ContainerCommand(Container):
    """Shallow wrapper to enable use of updated Parent class. This docstring
    is overridden in sphinx documentation.
    """

    __doc__ = pylatex.base_classes.ContainerCommand
