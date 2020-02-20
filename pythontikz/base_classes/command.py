#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module implements a class that implements a latex command.

This can be used directly or it can be inherited to make an easier interface
to it.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from reprlib import recursive_repr

from . import LatexObject
import pylatex
from pylatex.utils import dumps_list  # noqa: F401

# imports to keep standardised structure (unchanged classes are imported
# for files which are different)
from pylatex.base_classes import (CommandBase, Command,  # noqa: F401
                                  UnsafeCommand)  # noqa: F401


class Parameters(pylatex.base_classes.command.Parameters, LatexObject):
    """The base class used by :class:`~Options` and
    `~Arguments`.

    This class should probably never be used on its own and inhereting from it
    is only useful if a class like `~Options` or `~Arguments` is needed again.
    """

    def _get_dependency_sources(self):
        return (super()._get_dependency_sources()
                + [self._positional_args, self._key_value_args.values()])

    @recursive_repr()
    def __repr__(self):
        args = [repr(a) for a in self._positional_args]
        args += ["{}={}".format(
            k, v.dumps() if isinstance(v, LatexObject) else v)
            for (k, v) in self._key_value_args.items()]
        return self.__class__.__name__ + '(' + ', '.join(args) + ')'

    def __contains__(self, item):
        """Define contains to support in queries. Returns true if
        item present in positional list, or item matches string
        representation of keyword args; {k}={v}.
        """
        return item in self._list_args_kwargs()

    def _list_args_kwargs(self):
        """Make a list of strings representing all parameters.

        Returns
        -------
        list
        """

        params = []
        params.extend(self._positional_args)
        params.extend(['{}={}'.format(k, v.dumps()
                       if isinstance(v, LatexObject) else v)
                       for k, v in self._key_value_args.items()])
        return params


class Options(pylatex.base_classes.Options, Parameters):
    """Shallow Wrapper class to enable inheritance from overridden parameters
    class, with otherwise same behaviour as
    `pylatex.base_classes.command.Options`
    """

    __doc__ += pylatex.base_classes.Options.__doc__


class SpecialOptions(pylatex.base_classes.SpecialOptions, Parameters):
    """Shallow wrapper to enable use of updated Parameters class"""

    __doc__ = pylatex.base_classes.SpecialOptions.__doc__


class Arguments(pylatex.base_classes.Arguments, Parameters):
    """Shallow wrapper to enable use of updated Parameters class"""

    __doc__ = pylatex.base_classes.Arguments.__doc__
