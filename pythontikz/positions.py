# -*- coding: utf-8 -*-
"""
This module the TikZ classes which keep track of positions, namely
    coordinates and nodes

..  :copyright: (c) 2020 by Matthew Richards.
    :license: MIT, see License for more details.
"""
from abc import ABC

from .base_classes import Command
import re
import math

from .common import TikzLibrary, TikzObject
from .base_classes import LatexObject


class TikzNode(TikzObject):
    """A class that represents a TiKZ node."""

    _possible_anchors = ['north', 'south', 'east', 'west']

    def __init__(self, handle=None, options=None, at=None, text=None):
        """
        Args
        ----
        handle: str or None
            Node identifier, may be none for inline text usage
        options: list or `~.TikzOptions`
            List of options
        at: BaseTikzCoord or tuple
            Coordinate where node is placed
        text: str
            Body text of the node
        """
        super(TikzNode, self).__init__(options=options)

        self.handle = handle

        error_msg = TypeError(f"'at' argument of TikzNode must be a "
                              f"TikzCoordinate type or tuple specifying "
                              f"rectangular coordinates.")

        if isinstance(at, tuple):
            try:
                self._node_position = TikzRectCoord(*at, relative=False)
            except (TypeError, ValueError):
                raise error_msg

        elif isinstance(at, (BaseTikzCoord, type(None))):
            self._node_position = at
        else:
            raise error_msg

        self._node_text = text


class BaseTikzCoord(LatexObject, ABC):
    """Marker abstract class from which all coordinate classes inherit. Allows
    for cleaner use of isinstance regarding all coordinate objects.

    Note this intentionally breaks the naming convention of Tikz<**>Coord
    as it not to be used.

    This should be a private class, but sphinx throws a reference target not
    found error if it is.

    This should be an abstract class with ABC but could not implement this in
    a python 2/3 friendly way that also worked with the 3to2 conversion.
    """


class TikzRectCoord(BaseTikzCoord):
    r"""Extension of `~.BaseTikzCoord`. Forms a General Purpose
    Coordinate Class, representing a tuple of points specified, as opposed
    to the node shortcut command \coordinate.
    """

    _coordinate_str_regex = re.compile(r'(\+\+)?\(\s*(-?[0-9]+(\.[0-9]+)?)\s*'
                                       r',\s*(-?[0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, x, y, relative=False):
        """
        Args
        ----
        x: float or int
            X coordinate
        y: float or int
            Y coordinate
        relative: bool
            Coordinate is relative or absolute
        """
        self._x = float(x)
        self._y = float(y)
        self.relative = relative
        self.to_stop = False

    def __repr__(self):
        if self.relative:
            ret_str = '++'
        else:
            ret_str = ''
        return ret_str + '({},{})'.format(round(self._x, 3), round(self._y, 3))

    def dumps(self):
        """Return representation."""

        return self.__repr__()

    def __iter__(self):
        return iter((self._x, self._y))

    @classmethod
    def from_str(cls, coordinate):
        """Build a TikzCoordinate object from a string."""

        m = cls._coordinate_str_regex.match(coordinate)

        if m is None:
            raise ValueError('invalid coordinate string')

        if m.group(1) == '++':
            relative = True
        else:
            relative = False

        return cls(
            float(m.group(2)), float(m.group(4)), relative=relative)

    def __eq__(self, other):
        if isinstance(other, tuple):
            # if comparing to a tuple, assume it to be an absolute coordinate.
            other_relative = False
            other_x = float(other[0])
            other_y = float(other[1])
        elif isinstance(other, TikzRectCoord):
            other_relative = other.relative
            other_x = other._x
            other_y = other._y
        else:
            raise TypeError('can only compare tuple and TikzRectCoord types')

        # prevent comparison between relative and non relative
        # by returning False
        if other_relative != self.relative:
            return False

        tol = 1e-6

        # return comparison result
        return abs(other_x - self._x) < tol and abs(other_y - self._y) < tol

    def _arith_check(self, other):
        if isinstance(other, tuple):
            other_coord = TikzRectCoord(*other)
        elif isinstance(other, TikzRectCoord):
            if other.relative is True or self.relative is True:
                raise ValueError('refusing to add relative coordinates')
            other_coord = other
        elif isinstance(other, BaseTikzCoord):
            return False
        else:
            raise TypeError('can only add tuple or TiKZCoordinate types')
        return other_coord

    def __add__(self, other):
        other_coord = self._arith_check(other)
        # we have a legal type but can't use other coord syntax
        # hope that operation is implemented in reverse
        if other_coord is False:
            return other + self
        return TikzRectCoord(self._x + other_coord._x,
                             self._y + other_coord._y)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, second, first=None):
        """First - second, optional arg for rsubs"""
        first = self if first is None else first
        second_coord = self._arith_check(second)
        if second_coord is False:
            return second.__rsub__(first)
        return TikzRectCoord(first._x - second_coord._x,
                             first._y - second_coord._y)

    def __rsub__(self, other):
        other = self._arith_check(other)
        # note that other should never return the exception flag False
        # as every class which extends BaseTikzCoord should also
        # support subtraction with rectangular coords. If not, the defautlt
        # exception should suffice
        return self.__sub__(first=other, second=self)

    def distance_to(self, other):
        """Euclidean distance between two coordinates."""

        other_coord = self._arith_check(other)
        return math.sqrt(math.pow(self._x - other_coord._x, 2)
                         + math.pow(self._y - other_coord._y, 2))


class TikzPolCoord(TikzRectCoord):
    """Class representing the Tikz polar coordinate specification"""

    _coordinate_str_regex = re.compile(r'(\+\+)?\(\s*(-?[0-9]+(\.[0-9]+)?)\s*'
                                       r':\s*([0-9]+(\.[0-9]+)?)\s*\)')

    def __init__(self, angle, radius, relative=False):
        """
        angle: float or int
            angle in degrees
        radius: float or int, non-negative
            radius from orig
        relative: bool
            Coordinate is relative or absolute

        """
        if radius < 0:
            raise ValueError("Radius must be positive")
        self._radius = float(radius)
        self._angle = float(angle)
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        super(TikzPolCoord, self).__init__(x, y, relative=relative)

    def __repr__(self):
        if self.relative:
            ret_str = '++'
        else:
            ret_str = ''
        return ret_str + '({}:{})'.format(self._angle, self._radius)


class _TikzCalcCoordHandle(BaseTikzCoord):
    r"""Class to represent the syntax of using coordinate handle defined with
     \coordinate as opposed to defining the coordinate.

    Perhaps this can avoid being a seperate class, but the clear solution
    would be to make init return a tuple,  - the comand defn reference and
    the handle, which is also confusing. Still not happy with how this works.

    Perhaps a conditional dumps could work somehow (Note boolean flag on first
    call to dumps is not safe though).
    """

    def __init__(self, handle):
        self.handle = handle

    def dumps(self):
        return "({})".format(self.handle)

    def __add__(self, other):
        if isinstance(other, tuple):
            other = TikzRectCoord(*other)
        if isinstance(other, BaseTikzCoord) is False:
            raise TypeError("Only can add coordinates with other"
                            " coordinate types")
        return _TikzCalcImplicitCoord(self, "+", other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, second, first=None):
        """First - second, optional param for rsubs use"""
        if first is None:
            first = self
        if isinstance(second, tuple):
            second = TikzRectCoord(*second)
        if isinstance(second, BaseTikzCoord) is False:
            raise TypeError("Only can subtract coordinates with other"
                            " coordinate types")
        return _TikzCalcImplicitCoord(first, "-", second)

    def __rsub__(self, other):
        return self.__sub__(first=other, second=self)

    def __mul__(self, other):
        if isinstance(other, (float, int, TikzCalcScalar)) is False:
            raise TypeError("Coordinates can only be multiplied by scalars")
        return _TikzCalcImplicitCoord(other, "*", self)

    def __rmul__(self, other):
        return self.__mul__(other)


class TikzCalcCoord(BaseTikzCoord, TikzNode):
    r"""Represents the \coordinate syntax for defining a coordinate handle in
    TikZ. This itself is a shortcut for a special case of node. Use
    get_handle method to retrieve object corresponding to use of the
    coordinate handle (as opposed to the initial definition)
    """

    packages = [TikzLibrary('calc')]

    def get_handle(self):
        """Retrieves the associated coordinate handle accessor. # noqa: D401

        This handle is for the inline re-referencing of the same
        coordinate using the label text supplied at definition.
        """
        return _TikzCalcCoordHandle(self.handle)

    def dumps(self):
        """Return string representation of the node."""

        ret_str = []
        ret_str.append(Command('coordinate', options=self.options).dumps())

        if self.handle is not None:
            ret_str.append('({})'.format(self.handle))

        if self._node_position is not None:
            ret_str.append('at {}'.format(str(self._node_position)))

        if self._node_text is not None:
            ret_str.append('{{{text}}}'.format(text=self._node_text))
        # note text can be empty in / coordinate
        return ' '.join(ret_str) + ";"  # avoid space on end

    def __add__(self, other, error_text="addition"):
        raise TypeError("TikzCalcCoord does not support the operation"
                        " '{}' as it represents the variable "
                        "definition. \n The handle returned by "
                        "TikzCalcCoord.get_handle() does support "
                        "arithmetic operators.".format(error_text))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(other, error_text="subtraction")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        return self.__add__(other, error_text="multiplication")

    def __rmul__(self, other):
        return self.__mul__(other)


class TikzCalcScalar(LatexObject):
    """Wrapper for multiplication scalar in calc expressions e.g.
    ($ 4*(3,2.2) $)
    Written explicitly as a separate class to enable dumps support.
    Simpler than trying to deal with casting floats and strings
    without having other string parsing cause issues.
    """

    def __init__(self, value):
        """
        Args
        ----
        value: float or int
            The scalar operator to be applied to the successor coordinate.
        """
        self._value = value

    def dumps(self):
        """Represent the Scalar as a string in LaTeX syntax valid for a calc
        calculation.
        """
        return str(round(self._value, 2))


class _TikzCalcImplicitCoord(BaseTikzCoord):
    r"""Class representing an implicit coordinate that would be defined in
    TikZ using \coordinate. Supports addition/ subtraction of coordinates as
    can be done in the TikZ calc library.

    Should never be directly instantiated by user.
    """

    _legal_operators = ['-', '+']

    def __init__(self, *args):
        """
        Args
        ----
        args: BaseTikzCoord or str
            A list of coordinate elements
        """
        self._last_item_type = None
        self._arg_list = []

        # parse list and verify legality
        self._parse_arg_list(args)

    def _parse_next_item(self, item):
        # assume first item is a point
        if self._last_item_type is None:
            if self._add_scalar(item):
                return
            self._add_point_wrapper(
                item, error_to_raise=TypeError(
                    'First element of operator list must '
                    'be a or coordinate or scalar, got{}'.format(type(item))))

        elif self._last_item_type == 'point':
            if item == "*":
                self._arg_list.append(item)
                self._last_item_type = "point,multiplication"
                return
            try:
                self._add_operator(item)
            except (TypeError, ValueError):
                raise ValueError("Only a valid operator can follow a point")
        elif 'multiplication' in self._last_item_type:
            if self._last_item_type.startswith('point'):
                if self._add_scalar(item):
                    return
                raise ValueError(
                    'Point multiplication must be followed by a '
                    'scalar to be legal')
            else:  # starts with scalar
                self._add_point_wrapper(
                    item, ValueError("Scalar multiplication must be followed "
                                     "by a point to be legal.")
                )

        elif self._last_item_type == 'operator':
            self._add_point_wrapper(
                item, error_to_raise=ValueError(
                    'only a point descriptor can come after an operator'))

        elif self._last_item_type == 'scalar':
            if item == "*":
                self._arg_list.append(item)
                self._last_item_type = "scalar,multiplication"
                return
            else:
                raise ValueError("Multiplication symbol * must follow scalar"
                                 " in calc syntax.")

    def _add_scalar(self, item) -> bool:
        """Attempt to process item as a scalar, returns result as boolean"""
        if isinstance(item, (float, int)):
            self._last_item_type = "scalar"
            self._arg_list.append(TikzCalcScalar(item))
            return True
        elif isinstance(item, TikzCalcScalar):
            self._last_item_type = "scalar"
            self._arg_list.append(item)
            return True
        return False

    def _parse_arg_list(self, args):

        for item in args:
            # relatively easy error to make so ensure error is descriptive
            if isinstance(item, TikzCalcCoord):
                raise TypeError(
                    "TikzCalcCoord is invalid in an arithmetic "
                    "operation as it represents coordinate definition. "
                    "Instead, "
                    "TikzCalcCoord.get_handle() should be used.")
            # if we have nested, we expand to have single instance
            if isinstance(item, _TikzCalcImplicitCoord):
                for i in item._arg_list:
                    self._parse_next_item(i)
                continue
            self._parse_next_item(item)

    def _add_operator(self, operator):
        if isinstance(operator, str):
            if operator not in self._legal_operators:
                raise ValueError('Illegal user operator type: "{}"'
                                 .format(operator))
        else:
            raise TypeError('Only string type operators are allowed')

        self._arg_list.append(operator)
        self._last_item_type = 'operator'

    def _add_point_wrapper(self, point, error_to_raise: Exception) -> bool:
        try:
            self._add_point(point)
            return True
        except (TypeError, ValueError):
            # not a point, do something
            raise error_to_raise

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
            _item = _TikzCalcCoordHandle(point.handle)
        else:
            raise TypeError('Only str, tuple and  Tikz Positional '
                            'classes are allowed,'
                            ' got: {}'.format(type(point)))
        # add, finally
        self._arg_list.append(_item)
        self._last_item_type = 'point'

    def __add__(self, other):
        if isinstance(other, _TikzCalcImplicitCoord):
            args = self._arg_list.copy()
            args.append("+")
            args.extend(other._arg_list)
            return _TikzCalcImplicitCoord(*args)

        elif isinstance(other, BaseTikzCoord):
            args = self._arg_list.copy()
            args.extend(['+', other])
            return _TikzCalcImplicitCoord(*args)

        raise TypeError("Addition/ Subtraction unsupported for types"
                        " {} and {}".format(type(self), type(other)))

    def __sub__(self, other):
        if isinstance(other, _TikzCalcImplicitCoord):
            args = self._arg_list.copy()

            args.extend(self.negate_signs(other._arg_list))
            return _TikzCalcImplicitCoord(*args)

        elif isinstance(other, BaseTikzCoord):
            args = self._arg_list.copy()
            args.extend(["-", other])
            return _TikzCalcImplicitCoord(*args)

        raise TypeError("Addition/ Subtraction unsupported for types"
                        " {} and {}".format(type(self), type(other)))

    @classmethod
    def negate_signs(cls, input_list: list) -> list:
        """Swap + and - (for recursive subtraction)"""
        input_list = input_list.copy()  # in case input is used
        if input_list[0] not in cls._legal_operators:
            input_list.insert(0, '+')
        out_list = []
        for i in input_list:
            if isinstance(i, str):
                if i == '-':
                    out_list.append('+')
                elif i == '+':
                    out_list.append('-')
            else:
                out_list.append(i)
        return out_list

    def dumps(self):
        """Return representation of the implicit unevaluated coordinates."""

        ret_list = []
        for item in self._arg_list:
            if isinstance(item, str):
                ret_list.append(item)
            elif isinstance(item, LatexObject):
                ret_list.append(item.dumps())

        ret_str = ""
        for i in ret_list:
            # Asterisk in this context is for a calc line,
            # which means spaces are invalid, so string them
            if i == "*":
                ret_str = ret_str[:-1] + str(i)
            else:
                ret_str += str(i) + " "

        return "($ {}$)".format(ret_str)
