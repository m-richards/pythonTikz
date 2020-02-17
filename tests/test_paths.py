#!/usr/bin/python

"""
Test of correctness of tikz classes

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""
import pytest
from pylatex import NoEscape
from pytest import raises
from pythontikz.common import TikzOptions
from pythontikz.paths import TikzUserPath, TikzPathList, TikzArc, TikzDraw, \
    TikzRadius
from pythontikz.positions import (TikzRectCoord, TikzPolCoord, TikzCalcCoord,
                                  TikzNode)


from contextlib import contextmanager


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
            TikzPathList('(0, 1)', '--', '(2, 0)', TikzRectCoord(0, 0), (3, 0))

    ###############
    fail_args = [
        (('--', '(0, 1)'), raises(TypeError)),
        (('(0, 1)', 'illegal', '(0, 2)'), raises(ValueError)),
        (('(0, 1)', '--', '--'), raises(ValueError)),
        (('(0, 1)', '--', 'illegal'), raises(ValueError)),
        # circle and ellipse errors
        (('(0, 0)', 'circle', rec_11), raises(TypeError)),
        (('(0, 0)', 'circle', '(3, 4)'), raises(TypeError)),
        (('(0, 0)', 'circle', TikzRadius(3, ellipse_semi_minor_ax=3)),
         raises(ValueError)),
        (('(0, 0)', 'ellipse', rec_11), raises(TypeError)),
        (('(0, 0)', 'ellipse', '(3)'), raises(TypeError)),
        (('(0, 0)', 'ellipse', TikzRadius(3, ellipse_semi_minor_ax=None)),
         raises(ValueError)),
    ]

    @pytest.mark.parametrize("args,expectation", fail_args)
    def test_fail_path_args(self, args, expectation):
        with expectation:
            TikzPathList(*args)

    ###############
    dumps_cases = [
        ('(0.0,1.0) ellipse [x radius=2.0, y radius=3.0]',
         TikzPathList('(0, 1)', 'ellipse', (2.0, 3.0))),
        ('(0.0,1.0) ellipse [x radius=2.0, y radius=3.0]',
         TikzPathList('(0, 1)', 'ellipse', '(2,3)')),
        ('(0.0,1.0) ellipse [x radius=2.0, y radius=3.0]',
         TikzPathList('(0, 1)', 'ellipse', TikzRadius(2.0, 3.0))),
        ('(0.0,1.0) circle [radius=2.0]',
         TikzPathList('(0, 1)', 'circle', '2.0')),
        ('(0.0,1.0) circle [radius=2.0]',
         TikzPathList('(0, 1)', 'circle', 2.0)),
        ('(0.0,1.0) circle [radius=2.0]',
         TikzPathList('(0, 1)', 'circle', TikzRadius(2.0))),
        ('(0.0,1.0) arc (3.0:90.0:180.0)',
         TikzPathList('(0, 1)', 'arc', (3, 90, 180))),

    ]

    @pytest.mark.parametrize("expected,actual", dumps_cases)
    def test_dumps(self, expected, actual):
        assert actual.dumps() == expected

    ###############
    fail_cases = [
        # below makes sense to be legal? not sure why it was it in failures.
        # (lambda: TikzPathList('(0, 1)', TikzArc(180, 45, radius=1)),
        #  raises(TypeError)),
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
            a = case()
            print(a.dumps())


class TestTikzDraw(object):
    r"""Tests a number of cases of dumps to ensure that the otherwise tested
    components are being assembled correctly. Additionally tests the parent
    TikzPath as there is only a minor difference between teh classes, namely
    the dumps method supplying \draw instead of \path

    Unfortunately, parameterised tests don't work with this class (perhaps
    due to the use of recursive repr?)
    """

    def test_misc(self):
        orig_handle = (0, 0)
        rad = 1
        draw_options = TikzOptions("very thick", "->")

        a = TikzDraw([orig_handle + TikzRectCoord(-rad, 0), '--',
                      orig_handle + TikzRectCoord(rad, 0),
                      TikzNode(text=NoEscape(r"{$\Re$}"),
                               options=['above'])],
                     options=draw_options)
        b = (r'\draw[very thick,->] (-1.0,0.0) -- (1.0,0.0)'
             r' node[above] {{$\Re$}};')
        assert a.dumps() == b


###############
    h = TikzCalcCoord(handle='h', at=TikzRectCoord(0, 3))
    h = h.get_handle()
    dumps_cases = [
        (
            [rec_11, 'arc', "(300:200:2)", '--', pol1],
            None,
            r'\draw (1.0,1.0) arc (300.0:200.0:2.0) -- (180.0:1.0);'
        ),
        (
            [rec_11, 'rectangle', h, '-|', pol1, TikzNode(text='$x_1$',
                                                          options='above')],
            TikzOptions("very thick", "->", 'fill=black'),
            (r'\draw[very thick,->,fill=black] (1.0,1.0) rectangle (h) -|'
             ' (180.0:1.0) node[above] {$x_1$};')
        ),


    ]
    #
    @pytest.mark.parametrize("path,options,expected", dumps_cases)
    def test_dumps(self, path, options, expected):
        actual = TikzDraw(path=path, options=options)
        assert actual.dumps() == expected


class TestRadius(object):
    ###############
    dumps_cases = [
        ('[radius=3]', TikzRadius(3)),
        ('[x radius=2, y radius=3]', TikzRadius(radius=2,
                                                ellipse_semi_minor_ax=3)),

    ]

    @pytest.mark.parametrize("expected,actual", dumps_cases)
    def test_dumps(self, expected, actual):
        assert actual.dumps() == expected

    ###############
    fail_cases = [

        (lambda: TikzRadius(rec_11), raises(TypeError)),
        (lambda: TikzRadius(-3), raises(ValueError)),
        (lambda: TikzRadius(3, rec_11), raises(TypeError)),
        (lambda: TikzRadius(3, -2), raises(ValueError)),

    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail_cases(self, case, expectation):
        with expectation:
            a = case()
            print(a.dumps())
