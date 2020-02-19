# -*- coding: utf-8 -*-
"""
This module implements the base LaTeX object.

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""

import pylatex


class LatexObject(pylatex.base_classes.LatexObject):
    """The class that every other LaTeX class is a subclass of.

    This class implements the main methods that every LaTeX object needs. For
    conversion to LaTeX formatted strings it implements the dumps, dump and
    generate_tex methods. It also provides the methods that can be used to
    represent the packages required by the LatexObject.
    """

    dumps_docstring = "Represent the class as a string in LaTeX syntax."

    def get_package_sources(self):
        """Return a list of all associated data which may contain a package
        dependence.
        """
        return []

    def _propagate_packages(self):
        """Make sure packages get propagated."""
        print("propagate packages, sources are:", self.get_package_sources())
        for source in self.get_package_sources():
            if source is None:
                continue
            for item in source:
                print("item:", item, end='')
                if isinstance(item, pylatex.base_classes.LatexObject):
                    print('->', item)
                    for p in item.packages:
                        self.packages.add(p)
                    # pythontikz latex object should all have propagate
                    # packages defined
                    if isinstance(item, LatexObject):
                        item._propagate_packages()
                else:
                    print()
        print("\t\t total list: ", self.packages)
