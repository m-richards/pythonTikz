#!/usr/bin/python

"""
Test of correctness of tikz classes

This test calls functions with all available arguments to check whether they
still exist. An error from this file means that the public API has been
changed.
"""
import pytest
from pytest import raises
from pythontikz.positions import (TikzRectCoord, TikzPolCoord, TikzCalcCoord,
                                  TikzCalcScalar, _TikzCalcImplicitCoord,
                                  TikzNode
                                  )


from contextlib import contextmanager


@contextmanager
def does_not_raise():
    yield


rec_11 = TikzRectCoord(1, 1)


class TestRectangularCoords(object):

    def test_misc(self):
        x, y = TikzRectCoord(3, -4)
        assert x == 3 and y == -4
        a = TikzRectCoord.from_str('++(3,4)')
        assert a.relative is True
        assert a != TikzRectCoord(3, 4)

    ###############
    equality_cases = [
        (rec_11 + rec_11, TikzRectCoord(2, 2)),
        (rec_11 + (1, 1), TikzRectCoord(2, 2)),
        (rec_11 - (-1, 5), TikzRectCoord(2, -4)),
        ((-1, 5) - rec_11, TikzRectCoord(-2, 4)),
        (rec_11, (1, 1)),
        (TikzRectCoord.from_str("(1,1)"), rec_11)
    ]

    @pytest.mark.parametrize('actual,expected', equality_cases)
    def test_equality_checks(self, actual, expected):
        assert actual == expected

    ###############
    fail_cases = [
        (lambda: TikzRectCoord(0, 0) + 2, raises(TypeError)),
        (lambda: TikzRectCoord.from_str("(0,0"), raises(ValueError)),
        (lambda: TikzRectCoord.from_str("(x=0,y=0)"), raises(ValueError)),
        (lambda: rec_11 == 47.5, raises(TypeError)),
        (lambda: TikzRectCoord(0, 0, relative=True) + rec_11, raises(
            ValueError)),
    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail_cases(self, case, expectation):
        with expectation:
            case()

    ###############
    dumps_cases = [
        (TikzRectCoord(0, 5), '(0.0,5.0)'),
        (TikzRectCoord(0, 5) - (1, 2), '(-1.0,3.0)')
    ]

    @pytest.mark.parametrize("actual, expected", dumps_cases)
    def test_rect_dumps(self, actual, expected):
        assert actual.dumps() == expected


pol1 = TikzPolCoord(180, 1)
pol2 = TikzPolCoord(90, 1)


class TestPolarCoords(object):
    equality_cases = [
        (pol1 + pol1, TikzRectCoord(-2, 0)),
        (pol1 - pol1, TikzPolCoord(0, 0)),
        (pol2 - (-1, 2), TikzRectCoord(1, -1)),
        (TikzPolCoord.from_str('(180:1)'), pol1)
    ]

    @pytest.mark.parametrize('actual,expected', equality_cases)
    def test_equality_checks(self, actual, expected):
        assert actual == expected

    ###############
    fail_cases = [
        (lambda: TikzPolCoord(0, 0, relative=True) + 2, raises(TypeError)),
        (lambda: TikzPolCoord.from_str("(180,0)"), raises(ValueError)),
        (lambda: TikzPolCoord(0, -5), raises(ValueError)),
    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail(self, case, expectation):
        with expectation:
            case()

    ###############
    dumps_cases = [
        (TikzPolCoord(0, 5), '(0.0:5.0)'),
    ]

    @pytest.mark.parametrize("actual,expected", dumps_cases)
    def test_dumps(self, actual, expected):
        assert actual.dumps() == expected


calc1 = TikzCalcCoord(handle='h', at=rec_11, text='$(x_1, y_1)$')
h1 = calc1.get_handle()


class TestCalcCoords(object):
    equality_cases = [
        (pol1 + pol1, TikzRectCoord(-2, 0)),
        (pol1 - pol1, TikzPolCoord(0, 0)),
        (pol2 - (-1, 2), TikzRectCoord(1, -1)),
        (TikzPolCoord.from_str('(180:1)'), pol1),
    ]

    @pytest.mark.parametrize('actual,expected', equality_cases)
    def test_equality_checks(self, actual, expected):
        assert actual == expected

    ###############
    fail_cases = [
        (lambda: calc1 + calc1, raises(TypeError)),
        (lambda: (3, 4) + calc1, raises(TypeError)),
        (lambda: calc1 - calc1, raises(TypeError)),
        (lambda: calc1 * calc1, raises(TypeError)),
        (lambda: pol1 * calc1, raises(TypeError)),
        (lambda: pol1 + calc1, raises(TypeError)),
        (lambda: pol1 - calc1, raises(TypeError)),
        (lambda: calc1 * 4, raises(TypeError)),
        (lambda: h1 - 41, raises(TypeError)),
        (lambda: h1 - (3, 2), does_not_raise()),
        (lambda: h1 + (3, 2), does_not_raise()),
        (lambda: h1 + 7, raises(TypeError)),
        (lambda: h1 + pol1, does_not_raise()),
        (lambda: h1 - pol1, does_not_raise()),
        (lambda: h1 * 5.3, does_not_raise()),
        (lambda: (3, 4) + h1, does_not_raise()),
        (lambda: (3, 4) - h1, does_not_raise()),
        (lambda: 5.3 * h1, does_not_raise()),
        (lambda: h1 * pol1, raises(TypeError)),

    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail(self, case, expectation):
        with expectation:
            case()

    ###############
    # Note these dumps tests are important, since
    # they check that operations are well defined on coordinate handles
    # (easier than defining equality on implicit expressions just for this
    # purpose)
    dumps_cases = [
        (calc1, r"\coordinate (h) at (1.0,1.0) {$(x_1, y_1)$};"),
        (h1, "(h)"),
        (h1 + h1 + rec_11 + h1, r"($ (h) + (h) + (1.0,1.0) + (h) $)"),
        (h1 * TikzCalcScalar(5.3), r"($ 5.3*(h) $)"),
        (TikzCalcScalar(5.3) * h1, r"($ 5.3*(h) $)"),
        (h1 - rec_11, r"($ (h) - (1.0,1.0) $)"),
        (rec_11 - h1, r"($ (1.0,1.0) - (h) $)"),
    ]

    @pytest.mark.parametrize("actual,expected", dumps_cases)
    def test_dumps(self, actual, expected):
        assert actual.dumps() == expected


impl = _TikzCalcImplicitCoord(h1, '+', rec_11)


class TestCalcImplicitCoords(object):
    """Note that some of this has already been tested in the above case
    for operations on handles. We test the omissions. Most of these
    are unlikely to occur for end users as this class isn't exposed directly
    """

    fail_cases = [
        (lambda: impl - 42, raises(TypeError)),
        (lambda: impl + 42, raises(TypeError)),
    ]

    @pytest.mark.parametrize("case,expectation", fail_cases)
    def test_fail(self, case, expectation):
        with expectation:
            case()

    fail_cases2 = [
        ((rec_11, '^', rec_11), raises(ValueError)),  # not +/-
        ((3.2, '+', rec_11), raises(ValueError)),  # scalar needs * to follow
        ((calc1, '+', rec_11), raises(TypeError)),  # can't use calc directly
        ((rec_11, '+', "+"), raises(ValueError)),  # invalid post operator
        ((impl, '+', "+"), raises(ValueError)),  # check nesting of class
        ((rec_11, '+', 3), raises(ValueError)),  # check not string illegal
        ((rec_11, 3, rec_11), raises(ValueError)),  # check not string illegal
        ((rec_11, '+', TikzNode(at=rec_11)), does_not_raise()),
        # These cases can't arise unless done explicitly (operations won't
        # trigger them)
        ((rec_11, '*', rec_11), raises(ValueError)),
        ((rec_11, '*', 3), does_not_raise()),

    ]

    @pytest.mark.parametrize("case,expectation", fail_cases2)
    def test_fail_implicit_coord_args(self, case, expectation):
        with expectation:
            _TikzCalcImplicitCoord(*case)

    impl2 = _TikzCalcImplicitCoord(h1, '+', rec_11, '-', rec_11)
    dumps_cases = [
        (impl, "($ (h) + (1.0,1.0) $)"),
        (impl + rec_11, "($ (h) + (1.0,1.0) + (1.0,1.0) $)"),
        (impl - rec_11, "($ (h) + (1.0,1.0) - (1.0,1.0) $)"),
        (impl + impl, "($ (h) + (1.0,1.0) + (h) + (1.0,1.0) $)"),
        (impl + impl, "($ (h) + (1.0,1.0) + (h) + (1.0,1.0) $)"),
        (impl - impl2, "($ (h) + (1.0,1.0) - (h) - (1.0,1.0) + (1.0,1.0) $)"),
        (3 * h1 + impl, "($ 3*(h) + (h) + (1.0,1.0) $)"),

    ]

    @pytest.mark.parametrize("actual,expected", dumps_cases)
    def test_dumps(self, actual, expected):
        assert actual.dumps() == expected


def test_node():
    """Small test since Node also gets tested in paths. Also tests inherited
    methods from TikzObject
    """
    with raises(TypeError):
        TikzNode(at='(1,1)')
    with raises(TypeError):
        TikzNode(at=(1, 2))

    a = TikzNode('s', at=TikzRectCoord(1, 1), options=[
        'anchor=east'], text='$x_1$')
    assert a.dumps() == r'\node[anchor=east] (s) at (1.0,1.0) {$x_1$};'
    b = TikzNode('s', at=TikzRectCoord(1, 1), options=[
        'anchor=east'])
    assert b.dumps() == r'\node[anchor=east] (s) at (1.0,1.0) {};'
