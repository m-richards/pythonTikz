# -*- coding: utf-8 -*-
"""
This module implements the base LaTeX object.

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""

import pylatex
from collections.abc import Iterable


class LatexObject(pylatex.base_classes.LatexObject):
    """The class that every other LaTeX class is a subclass of.

    This class implements the main methods that every LaTeX object needs. For
    conversion to LaTeX formatted strings it implements the dumps, dump and
    generate_tex methods. It also provides the methods that can be used to
    represent the packages required by the LatexObject.
    """

    dumps_docstring = "Represent the class as a string in LaTeX syntax."

    def _get_dependency_sources(self):
        """Return a list of all associated data which may contain a package
        dependence.
        """
        return []

    def _propagate_packages(self):
        """Make sure packages get propagated. Recursive DFS to obtain all
        package dependencies of sub-components
        """
        for source in self._get_dependency_sources():
            if source is None:
                continue
            if isinstance(source, Iterable) is False:
                source = [source]
            for item in source:
                if isinstance(item, pylatex.base_classes.LatexObject):
                    # pythontikz latex object should all have propagate
                    # packages defined
                    if isinstance(item, (LatexObject,
                                         pylatex.base_classes.Container)):
                        item._propagate_packages()
                    for p in item.packages:
                        self.packages.add(p)
