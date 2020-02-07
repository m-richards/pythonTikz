# -*- coding: utf-8 -*-
"""
This module implements the classes used to show plots.

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""
from .base_classes import LatexObject, Command
import re

from .common import TikzLibrary, TikzObject, TikzAnchor
from .positions import (TikzRectCoord, BaseTikzCoord, TikzNode,
                        )
import warnings


def _warning(message, category, filename, lineno, file=None, line=None):
    # note coverage excluded since this is never directly called since it is
    # a monkey patch
    name = category.__name__ if category else None  # pragma: no cover
    return f"{name} {message}"  # pragma: no cover


warnings.formatwarning = _warning


class TikzUserPath(LatexObject):
    """Represents a possible TikZ path."""

    def __init__(self, path_type, options=None):
        """
        Args
        ----
        path_type: str
            Type of path used
        options: Options
            List of options to add
        """
        super(TikzUserPath, self).__init__()
        self.path_type = path_type
        self.options = options

    def dumps(self):
        """Return path command representation."""

        ret_str = self.path_type

        if self.options is not None:
            ret_str += self.options.dumps()

        return ret_str


class TikzRadius(LatexObject):
    """Class which represents specification of a radius or radii for use with
    the 'circle' path argument. Should not need to be used directly, should
    be able inference from context.
    """

    def __init__(self, radius, ellipse_second_rad=None):
        """Initialise a Radius object for a circle or ellipse respectively"""
        if ellipse_second_rad is None:
            self.is_ellipse = False
        else:
            self.is_ellipse = True
        self._radius = radius
        self._ellipse_second_rad = ellipse_second_rad

        if isinstance(radius, (float, int)) is False:
            raise TypeError("Radius must be an integer for float.")
        if radius < 0:
            raise ValueError(f"{__class__} radius cannot be negative.")

        if ellipse_second_rad is not None:
            if ellipse_second_rad < 0:
                raise ValueError(f"{__class__} secondary radius cannot be "
                                 f"negative.")
            if isinstance(ellipse_second_rad, (float, int)) is False:
                raise TypeError("Secondary radius must be an integer for "
                                "float.")

    def dumps(self):
        """Return a string representation of a radius argument."""
        if self.is_ellipse:
            return "[x radius={}, y radius={}]".format(
                self._radius, self._ellipse_second_rad)
        else:
            return "[radius={}]".format(self._radius)


class TikzPathList(LatexObject):
    """Represents a path drawing."""

    _base_legal_path_types = ['--', '-|', '|-', 'to',
                              'rectangle', 'circle', 'ellipse',
                              'arc', 'edge']

    def __init__(self, *args, additional_path_types=None):
        """
        Args
        ----
        *args: list
            A list of path elements
        """
        self._last_item_type = None
        self._arg_list = []

        self._legal_path_types = self._base_legal_path_types
        if additional_path_types is not None:
            self._legal_path_types.extend(additional_path_types)

        # parse list and verify legality
        self._parse_arg_list(args)

    def append(self, item):
        """Add a new element to the current path."""
        self._parse_next_item(item)

    def _parse_next_item(self, item):
        # assume first item is a point
        if self._last_item_type is None:
            try:
                self._add_point(item)
            except (TypeError, ValueError):
                # not a point, do something
                raise TypeError(
                    'First element of path list must be a node identifier'
                    ' or coordinate'
                )
        elif self._last_item_type in ('point', 'arc', 'circle', 'ellipse'):

            if isinstance(item, TikzNode):
                # Note that we drop the preceding backslash since that is
                # not part of inline syntax. trailing ";" dropped as well
                # since TikzPath will add this from its own dumps
                self._arg_list.append(item.dumps()[1:-1])
                return

            # point after point is permitted, doesnt draw
            try:
                self._add_point(item)
                warnings.warn('TikzPath contains no path '
                              'specifier between successive coordinates. '
                              f'"{self.dumps()}" is legal '
                              'TikZ but is unlikely to produce the desired '
                              'result.\n')
                return
            except (ValueError, TypeError):
                # not a point, try path
                pass

            if isinstance(item, (str, TikzUserPath)):
                # special cases need more information
                if item in ('circle', 'ellipse', 'arc'):
                    self._add_path(item, append_text=item)
                else:
                    self._add_path(item, append_text=None)

        # block for dealing with all path types
        elif 'path' in self._last_item_type:
            if self._last_item_type == 'path.arc':
                # only allow arc specifier after arc path
                # note this will throw exceptions if incorrect
                self._add_arc_spec(item)
                return
            if self._last_item_type == 'path.circle':
                self._add_circle(item)
            elif self._last_item_type == 'path.ellipse':
                self._add_ellipse(item)

            else:  # ordinary path - last type == 'path'
                # only point  or cycle allowed after path
                if isinstance(item, str) and item.strip() == 'cycle':
                    self._arg_list.append(item)
                    return

                try:
                    self._add_point(item)
                    return
                except (TypeError, ValueError):
                    raise ValueError('only a point descriptor  or "cycle" can '
                                     'come after a path descriptor, got {}'
                                     .format(type(item)))

    def _parse_arg_list(self, args):

        for item in args:
            self._parse_next_item(item)

    def _add_path(self, path, append_text=None):
        """Attempt to add input argument as a path type specifier,
        raises and appropriate exception if invalid.
        """
        if isinstance(path, str):
            if path in self._legal_path_types:
                _path = TikzUserPath(path)
            else:
                raise ValueError('Illegal user path type: "{}"'.format(path))
        elif isinstance(path, TikzUserPath):
            _path = path

        # add
        self._arg_list.append(_path)
        self._last_item_type = 'path'
        # add additional info if needed
        if append_text is not None:
            self._last_item_type += "." + append_text

    def _add_point(self, point):
        if isinstance(point, str):
            try:
                _item = TikzRectCoord.from_str(point)
            except ValueError:
                raise ValueError('Illegal point string: "{}"'.format(point))
        elif isinstance(point, BaseTikzCoord):
            _item = point
        elif isinstance(point, tuple):
            _item = TikzRectCoord(*point)
        elif isinstance(point, TikzNode):
            _item = '({})'.format(point.handle)
        elif isinstance(point, TikzAnchor):
            _item = point.dumps()
        else:
            raise TypeError('Only str, tuple or  Tikz positional '
                            'classes are allowed,'
                            ' got: {}'.format(type(point)))
        # add, finally
        self._arg_list.append(_item)
        self._last_item_type = 'point'

    def _add_arc_spec(self, arc):
        if isinstance(arc, str):
            try:
                _arc = TikzArc.from_str(arc)
            except ValueError:
                raise ValueError('Illegal arc string: "{}"'.format(arc))
        elif isinstance(arc, TikzArc):
            _arc = arc
        elif isinstance(arc, tuple):
            _arc = TikzArc(*arc)

        else:
            raise TypeError('Only str, tuple or TikzArc'
                            'arc allowed to follow arc specifier,'
                            ' got: {}'.format(type(arc)))
        # add, finally
        self._arg_list.append(_arc)
        self._last_item_type = 'arc'

    def _add_circle(self, item):
        """If circle is false then ellipse"""
        method_error_msg = TypeError("Circle radius must be of type float, "
                                     "str which is castable to float, "
                                     f"or TikzRadius. Got {type(item)}.")
        if isinstance(item, str):

            try:
                _item = TikzRadius(float(item))
            except ValueError:
                raise method_error_msg

        elif isinstance(item, (float, int)):
            # note non-negative is check on initialisation
            _item = TikzRadius(item)
        elif isinstance(item, TikzRadius):
            if item.is_ellipse:
                raise ValueError("'circle' path cannot be succeeded by"
                                 " ellipse specifier")
            _item = item
        else:
            raise method_error_msg
        self._arg_list.append(_item)
        self._last_item_type = 'circle'

    def _add_ellipse(self, item):
        method_error_msg = TypeError(
            "Ellipse radius must be of type tuple [of length 2], "
            "a string representation of a tuple or "
            f"or TikzRadius. Got {type(item)}.")
        if isinstance(item, str):
            m = re.match(r'\('
                         r'\s*([0-9]+(\.[0-9]+)?)\s*,'
                         r'\s*([0-9]+(\.[0-9]+)?)\s*\)', item)
            if m is None:
                raise method_error_msg
            _item = TikzRadius(m.group(1), m.group(3))
        elif (isinstance(item, (list, tuple)) and len(item) == 2
              and (isinstance(item[0], (float, int))
              and (item[1], (float, int)))):
            _item = TikzRadius(*item)

        elif isinstance(item, TikzRadius):
            if item.is_ellipse is False:
                raise ValueError("'ellipse' path cannot be succeeded by"
                                 " circle specifier.")
            _item = item

        else:
            raise method_error_msg
        self._arg_list.append(_item)
        self._last_item_type = 'ellipse'

    def dumps(self):
        """Return representation of the path command."""

        ret_str = []
        for item in self._arg_list:
            if isinstance(item, str):
                ret_str.append(item)
            elif isinstance(item, LatexObject):
                ret_str.append(item.dumps())
        return ' '.join(ret_str)


class TikzPath(TikzObject):
    r"""The TikZ \path command."""

    def __init__(self, path=None, options=None):
        """
        Args
        ----
        path: TikzPathList or list
            A list of the nodes, path types in the path
        options: TikzOptions
            A list of options for the command
        """
        super(TikzPath, self).__init__(options=options)

        additional_path_types = None
        if options is not None and 'use Hobby shortcut' in options:
            self.packages.add(TikzLibrary('hobby'))
            additional_path_types = [".."]

        # if already a TikzPathList, additional paths should have already been
        # supplied
        if isinstance(path, TikzPathList):
            self.path = path
        elif isinstance(path, list):
            self.path = TikzPathList(
                *path, additional_path_types=additional_path_types)
        elif path is None:
            self.path = TikzPathList(
                additional_path_types=additional_path_types)
        else:
            raise TypeError(
                'argument "path" can only be of types list or TikzPathList')

    def append(self, element):
        """Append a path element to the current list."""
        self.path.append(element)

    def dumps(self):
        """Return a representation for the command."""

        ret_str = [Command('path', options=self.options).dumps()]

        ret_str.append(self.path.dumps())
        return ' '.join(ret_str) + ';'


class TikzDraw(TikzPath):
    """A draw command is just a path command with the draw option."""

    def __init__(self, path=None, options=None):
        """
        Args
        ----
        path: `~.TikzPathList` or List
            A list of the nodes, path types in the path
        options: TikzOptions
            A list of options for the command
        """
        super(TikzDraw, self).__init__(path=path, options=options)

    def dumps(self):
        r"""Return a representation for the command. Override
        to provide clearer syntax to user instead of \path[draw]
        """
        ret_str = [Command('draw', options=self.options).dumps()]

        ret_str.append(self.path.dumps())
        return ' '.join(ret_str) + ";"


class TikzArc(LatexObject):
    """A class to represent the tikz specification for arcs
    i.e. (ang1: ang2: rad)
    """

    _str_verif_regex = re.compile(r'\('
                                  r'\s*(-?[0-9]+(\.[0-9]+)?)\s*:'
                                  r'\s*(-?[0-9]+(\.[0-9]+)?)\s*:'
                                  r'\s*([0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, start_ang, finish_ang, radius,
                 force_far_direction=False):
        """
        start_ang: float or int
            angle in degrees
        radius: float or int
            radius from orig
        force_far_direction: bool
            forces arc to go in the longer direction around circumference

        """
        if force_far_direction:
            # forcing an extra rotation around
            if start_ang > finish_ang:
                start_ang -= 360
            else:
                finish_ang -= 360

        self._radius = float(radius)
        self._start_ang = float(start_ang)
        self._finish_ang = float(finish_ang)

    def __repr__(self):
        return "({}:{}:{})".format(
            self._start_ang, self._finish_ang, self._radius)

    def dumps(self):
        """Return a representation. Alias for consistency."""

        return self.__repr__()

    @classmethod
    def from_str(cls, arc):
        """Build a TikzArc object from a string."""
        m = cls._str_verif_regex.match(arc)

        if m is None:
            raise ValueError('invalid arc string')

        return cls(float(m.group(1)), float(m.group(3)), float(m.group(5)))
