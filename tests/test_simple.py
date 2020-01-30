#!/usr/bin/python

"""
Test of correctness of tikz classes

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""
import pytest
from pytest import raises
from pythontikz import (TikzPicture, TikzRectCoord, TikzNode,
                        TikzAnchor, TikzUserPath, TikzPathList, TikzPath,
                        TikzDraw,
                        TikzScope, TikzOptions, TikZLibrary,
                        TikzPolCoord, TikzArc,
                        TikzCalcCoord, TikZCalcScalar, Plot, Axis)
from pythontikz.positions import (TikzRectCoord, TikzPolCoord, TikzCalcCoord,
                                  TikzNode, TikZCalcScalar)

from pythontikz.positions import _TikzCalcImplicitCoord
from contextlib import contextmanager


@contextmanager
def does_not_raise():
    yield


rec_11 = TikzRectCoord(1, 1)


class TestRectangularCoords(object):
    equality_cases = [
        (rec_11 + rec_11, TikzRectCoord(2, 2)),
        (rec_11 + (1, 1), TikzRectCoord(2, 2)),
        (rec_11 - (-1, 5), TikzRectCoord(2, -4)),
        (TikzRectCoord.from_str("(1,1)"), rec_11)
        ]

    @pytest.mark.parametrize('expected,actual', equality_cases)
    def test_rect_equality_checks(self, expected, actual):
        assert expected == actual

    fail_cases = [
        (lambda: TikzRectCoord(0, 0) + 2, raises(TypeError)),
        (lambda: TikzRectCoord.from_str("(0,0"), raises(ValueError)),
        (lambda: TikzRectCoord.from_str("(x=0,y=0)"), raises(ValueError)),
         ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_rect_fail(self, case, expectation):
        with expectation:
            case()

    dumps_cases = [
        (TikzRectCoord(0, 5), '(0.0,5.0)'),
        (TikzRectCoord(0, 5) - (1, 2), '(-1.0,3.0)')
    ]

    @pytest.mark.parametrize("expected,actual", dumps_cases)
    def test_rect_dumps(self, expected, actual):
        assert expected.dumps() == actual


pol1 = TikzPolCoord(180, 1)
pol2 = TikzPolCoord(90, 1)

class TestPolarCoords(object):
    equality_cases = [
        (pol1 + pol1, TikzRectCoord(-2, 0)),
        (pol1 - pol1, TikzPolCoord(0, 0)),
        (pol2 - (-1, 2), TikzRectCoord(1, -1)),
        (TikzPolCoord.from_str('(180:1)'), pol1)
    ]

    @pytest.mark.parametrize('expected,actual', equality_cases)
    def test_equality_checks(self, expected, actual):
        assert expected == actual

    fail_cases = [
        (lambda: TikzPolCoord(0, 0) + 2, raises(TypeError)),
        (lambda: TikzPolCoord.from_str("(180,0)"), raises(ValueError)),
    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail(self, case, expectation):
        with expectation:
            case()

    dumps_cases = [
        (TikzPolCoord(0, 5), '(0.0:5.0)'),
    ]

    @pytest.mark.parametrize("expected,actual", dumps_cases)
    def test_dumps(self, expected, actual):
        assert expected.dumps() == actual



    # def test_node(self):
    #     pass
    #
    # def test_dumps(self):
    #     pass


    pass
