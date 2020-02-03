#!/usr/bin/python

"""
Test of correctness of tikz classes

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""
import pytest
from pytest import raises

from pythontikz import TikzUserPath, TikzOptions, TikzPathList, TikzArc
from pythontikz.positions import (TikzRectCoord, TikzPolCoord, TikzCalcCoord,
                                  TikzCalcScalar, _TikzCalcImplicitCoord,
                                  TikzNode
                                  )


from contextlib import contextmanager
from io import StringIO
import sys


@contextmanager
def does_not_raise():
    yield


rec_11 = TikzRectCoord(1, 1)


class TestUserPath(object):
    """This is tested poorly, I don't use this class or the underlying tikz
    it represents
    """

    def test_misc(self):
        # necessary here because 'in' is a python keyword
        path_options = {'in': 90, 'out': 0}
        p = TikzUserPath('edge',
                     TikzOptions('-latex', **path_options))
        assert p.dumps() == "edge[-latex,in=90,out=0]"




pol1 = TikzPolCoord(180, 1)
pol2 = TikzPolCoord(90, 1)


class TestPathList(object):

    def test_warning_case(self):
        with pytest.warns(UserWarning):
            a = TikzPathList('(0, 1)', '--', '(2, 0)', TikzRectCoord(0,0), (3,0))

    ###############
    fail_args = [
        (('--', '(0, 1)'), raises(TypeError)),
        (('(0, 1)', 'illegal', '(0, 2)'), raises(ValueError)),
        (('(0, 1)', '--', '--'), raises(ValueError)),
        (('(0, 1)', '--', 'illegal'), raises(ValueError))
    ]

    @pytest.mark.parametrize("args,expectation", fail_args)
    def test_fail_path_args(self, args, expectation):
        with expectation:
            TikzPathList(*args)

    ###############
    dumps_cases = [
        (TikzPathList('(0, 1)', '--', '(2, 0)'),
            '(0.0,1.0) -- (2.0,0.0)'),
        (TikzPathList('(0, 1)', 'rectangle', '(2, 3)'),
            '(0.0,1.0) rectangle (2.0,3.0)'),
        (TikzPathList('(0, 1)', 'arc', TikzArc(180, 45, radius=1), '--',
                      'cycle'),
         '(0.0,1.0) arc (180.0:45.0:1.0) -- cycle'),
        (TikzPathList('(0, 1)',  TikzUserPath(
            path_type="edge", options=TikzOptions('bend right')),
                      (2,2), TikzNode(text='$x_2$')),
         '(0.0,1.0) edge[bend right] (2.0,2.0) node {$x_2$}'),
        (TikzPathList('(0, 1)', 'arc', '(0:300:2)'),
         '(0.0,1.0) arc (0.0:300.0:2.0)'),
        (TikzPathList('(0, 1)', 'arc', (0,300,2)),
         '(0.0,1.0) arc (0.0:300.0:2.0)'),
    ]

    @pytest.mark.parametrize("expected,actual", dumps_cases)
    def test_dumps(self, expected, actual):
        assert expected.dumps() == actual

    ###############
    fail_cases = [
        (lambda: TikzPathList('(0, 1)', TikzArc(180, 45, radius=1)),
                              raises(TypeError)),
        (lambda: TikzPathList('arc', TikzArc(180, 45, radius=1)),
         raises(TypeError)),
        (lambda: TikzPathList(TikzArc(180, 45, radius=1)),
         raises(TypeError)),
        # require brackets
        (lambda: TikzPathList('(0, 1)', 'arc', '0:300:2'), raises(ValueError)),
        (lambda: TikzPathList('(0, 1)', 'arc', rec_11), raises(TypeError))
    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail_cases(self, case, expectation):
        with expectation:
            case()





