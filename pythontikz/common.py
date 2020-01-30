# -*- coding: utf-8 -*-
"""
This module implements the classes used to show plots.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""
from .base_classes import LatexObject, Environment, Command, Options, Container
from . import Package


class TikZOptions(Options):
    """Options class, do not escape."""

    escape = False

    def append_positional(self, option):
        """Add a new positional option."""

        self._positional_args.append(option)


class TikZLibrary(Package):
    """Wrapper for package command for inclusion of tikz libraries. Allows
    automatic detection of some tikz libraries.
    """

    _latex_name = 'usetikzlibrary'


class TikZ(Environment):
    """Basic TikZ container class."""

    _latex_name = 'tikzpicture'
    packages = [Package('tikz')]


class Axis(Environment):
    """PGFPlots axis container class, this contains plots."""

    packages = [Package('pgfplots'), Command('pgfplotsset', 'compat=newest')]

    def __init__(self, options=None, *, data=None):
        """
        Args
        ----
        options: str, list or `~.Options`
            Options to format the axis environment.
        """

        super().__init__(options=options, data=data)


class TikZScope(Environment):
    """TikZ Scope Environment."""

    _latex_name = 'scope'


class TikZObject(Container):
    """Abstract Class that some TikZ Objects inherits from."""

    def __init__(self, options=None):
        """
        Args
        ----
        options: list
            Options pertaining to the object
        """

        super(TikZObject, self).__init__()
        self.options = options

    def dumps(self):
        """Return string representation of the node."""

        ret_str = []
        ret_str.append(Command('node', options=self.options).dumps())

        if self.handle is not None:
            ret_str.append('({})'.format(self.handle))

        if self._node_position is not None:
            ret_str.append('at {}'.format(str(self._node_position)))

        if self._node_text is not None:
            ret_str.append('{{{text}}};'.format(text=self._node_text))
        else:
            ret_str.append('{};')
        return ' '.join(ret_str)

    def get_anchor_point(self, anchor_name):
        """Return an anchor point of the node, if it exists."""

        if anchor_name in self._possible_anchors:
            return TikZNodeAnchor(self.handle, anchor_name)
        else:
            try:
                anchor = int(anchor_name.split('_')[1])
            except:
                anchor = None

            if anchor is not None:
                return TikZNodeAnchor(self.handle, str(anchor))

        raise ValueError('Invalid anchor name: "{}"'.format(anchor_name))

    def __getattr__(self, attr_name):
        try:
            point = self.get_anchor_point(attr_name)
            return point
        except ValueError:
            pass

        # raise AttributeError(
        #    'Invalid attribute requested: "{}"'.format(attr_name))


class Plot(LatexObject):
    """A class representing a PGFPlot."""

    packages = [Package('pgfplots'), Command('pgfplotsset', 'compat=newest')]

    def __init__(self,
                 name=None,
                 func=None,
                 coordinates=None,
                 error_bar=None,
                 options=None):
        """
        Args
        ----
        name: str
            Name of the plot.
        func: str
            A function that should be plotted.
        coordinates: list
            A list of exact coordinates tat should be plotted.

        options: str, list or `~.Options`
        """

        self.name = name
        self.func = func
        self.coordinates = coordinates
        self.error_bar = error_bar
        self.options = options

        super().__init__()

    def dumps(self):
        """Represent the plot as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        string = Command('addplot', options=self.options).dumps()

        if self.coordinates is not None:
            string += ' coordinates {%\n'

            if self.error_bar is None:
                for x, y in self.coordinates:
                    # ie: "(rot,y)"
                    string += '(' + str(x) + ',' + str(y) + ')%\n'

            else:
                for (x, y), (e_x, e_y) in zip(self.coordinates,
                                              self.error_bar):
                    # ie: "(rot,y) +- (e_x,e_y)"
                    string += '(' + str(x) + ',' + str(y) + \
                              ') +- (' + str(e_x) + ',' + str(e_y) + ')%\n'

            string += '};%\n%\n'

        elif self.func is not None:
            string += '{' + self.func + '};%\n%\n'

        if self.name is not None:
            string += Command('addlegendentry', self.name).dumps()

        super().dumps()

        return string


class TikZNodeAnchor(LatexObject):
    """Representation of a node's anchor point."""

    def __init__(self, node_handle, anchor_name):
        """
        Args
        ----
        node_handle: str
            Node's identifier
        anchor_name: str
            Name of the anchor
        """

        self.handle = node_handle
        self.anchor = anchor_name

    def __repr__(self):
        return '({}.{})'.format(self.handle, self.anchor)

    def dumps(self):
        """Return a representation. Alias for consistency."""

        return self.__repr__()
