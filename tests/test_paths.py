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

    # fail_cases = [
    # ]
    #
    # @pytest.mark.parametrize("case,expectation", fail_cases)
    # def test_fail(self, case, expectation):
    #     with expectation:
    #         case()

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
        (TikzPathList('(0, 1)', 'arc', TikzArc(180, 45, radius=1)),
         '(0.0,1.0) arc (180.0:45.0:1.0)'),
        (TikzPathList('(0, 1)', '--', (2,2), TikzNode(
                                               text='$x_2$')),
         '(0.0,1.0) -- (2.0,2.0) node {$x_2$}'),
    ]

    @pytest.mark.parametrize("expected,actual", dumps_cases)
    def test_dumps(self, expected, actual):
        assert expected.dumps() == actual



#
# calc1 = TikzCalcCoord(handle='h', at=rec_11, text='$(x_1, y_1)$')
# h1 = calc1.get_handle()
#
#
# class TestCalcCoords(object):
#     equality_cases = [
#         (pol1 + pol1, TikzRectCoord(-2, 0)),
#         (pol1 - pol1, TikzPolCoord(0, 0)),
#         (pol2 - (-1, 2), TikzRectCoord(1, -1)),
#         (TikzPolCoord.from_str('(180:1)'), pol1),
#     ]
#
#     @pytest.mark.parametrize('expected,actual', equality_cases)
#     def test_equality_checks(self, expected, actual):
#         assert expected == actual
#
#     ###############
#     fail_cases = [
#         (lambda: calc1 + calc1, raises(TypeError)),
#         (lambda: (3, 4) + calc1, raises(TypeError)),
#         (lambda: calc1 - calc1, raises(TypeError)),
#         (lambda: calc1 * calc1, raises(TypeError)),
#         (lambda: pol1 * calc1, raises(TypeError)),
#         (lambda: pol1 + calc1, raises(TypeError)),
#         (lambda: pol1 - calc1, raises(TypeError)),
#         (lambda: calc1 * 4, raises(TypeError)),
#         (lambda: h1 - 41, raises(TypeError)),
#         (lambda: h1 - (3, 2), does_not_raise()),
#         (lambda: h1 + (3, 2), does_not_raise()),
#         (lambda: h1 + 7, raises(TypeError)),
#         (lambda: h1 + pol1, does_not_raise()),
#         (lambda: h1 - pol1, does_not_raise()),
#         (lambda: h1 * 5.3, does_not_raise()),
#         (lambda: (3, 4) + h1, does_not_raise()),
#         (lambda: (3, 4) - h1, does_not_raise()),
#         (lambda: 5.3 * h1, does_not_raise()),
#         (lambda: h1 * pol1, raises(TypeError)),
#
#     ]
#
#     @pytest.mark.parametrize("case,expectation", fail_cases)
#     def test_fail(self, case, expectation):
#         with expectation:
#             case()
#
#     ###############
#     # Note these dumps tests are important, since
#     # they check that operations are well defined on coordinate handles
#     # (easier than defining equality on implicit expressions just for this
#     # purpose)
#     dumps_cases = [
#         (calc1, r"\coordinate (h) at (1.0,1.0) {$(x_1, y_1)$};"),
#         (h1, "(h)"),
#         (h1 + h1 + rec_11 + h1, r"($ (h) + (h) + (1.0,1.0) + (h) $)"),
#         (h1 * TikzCalcScalar(5.3), r"($ 5.3*(h) $)"),
#         (TikzCalcScalar(5.3) * h1, r"($ 5.3*(h) $)"),
#         (h1 - rec_11, r"($ (h) - (1.0,1.0) $)"),
#         (rec_11 - h1, r"($ (1.0,1.0) - (h) $)"),
#     ]
#
#     @pytest.mark.parametrize("expected,actual", dumps_cases)
#     def test_dumps(self, expected, actual):
#         assert expected.dumps() == actual
#
#
# impl = _TikzCalcImplicitCoord(h1, '+', rec_11)
#
#
# class TestCalcImplicitCoords(object):
#     """Note that some of this has already been tested in the above case
#     for operations on handles. We test the omissions. Most of these
#     are unlikely to occur for end users as this class isn't exposed directly
#     """
#
#     fail_cases = [
#         (lambda: impl - 42, raises(TypeError)),
#         (lambda: impl + 42, raises(TypeError)),
#     ]
#
#     @pytest.mark.parametrize("case,expectation", fail_cases)
#     def test_fail(self, case, expectation):
#         with expectation:
#             case()
#
#     fail_cases2 = [
#         ((rec_11, '^', rec_11), raises(ValueError)),  # not +/-
#         ((3.2, '+', rec_11), raises(ValueError)),  # scalar needs * to follow
#         ((calc1, '+', rec_11), raises(TypeError)),  # can't use calc directly
#         ((rec_11, '+', "+"), raises(ValueError)),  # invalid post operator
#         ((impl, '+', "+"), raises(ValueError)),  # check nesting of class
#         ((rec_11, '+', 3), raises(ValueError)),  # check not string illegal
#         ((rec_11, 3, rec_11), raises(ValueError)),  # check not string illegal
#         ((rec_11, '+', TikzNode(at=rec_11)), does_not_raise()),
#         # These cases can't arise unless done explicitly (operations won't
#         # trigger them)
#         ((rec_11, '*', rec_11), raises(ValueError)),
#         ((rec_11, '*', 3), does_not_raise()),
#
#     ]
#
#     @pytest.mark.parametrize("case,expectation", fail_cases2)
#     def test_fail_implicit_coord_args(self, case, expectation):
#         with expectation:
#             _TikzCalcImplicitCoord(*case)
#
#     impl2 = _TikzCalcImplicitCoord(h1, '+', rec_11, '-', rec_11)
#     dumps_cases = [
#         (impl, "($ (h) + (1.0,1.0) $)"),
#         (impl + rec_11, "($ (h) + (1.0,1.0) + (1.0,1.0) $)"),
#         (impl - rec_11, "($ (h) + (1.0,1.0) - (1.0,1.0) $)"),
#         (impl + impl, "($ (h) + (1.0,1.0) + (h) + (1.0,1.0) $)"),
#         (impl + impl, "($ (h) + (1.0,1.0) + (h) + (1.0,1.0) $)"),
#         (impl - impl2, "($ (h) + (1.0,1.0) - (h) - (1.0,1.0) + (1.0,1.0) $)"),
#         (3 * h1 + impl, "($ 3*(h) + (h) + (1.0,1.0) $)"),
#
#     ]
#
#     @pytest.mark.parametrize("expected,actual", dumps_cases)
#     def test_dumps(self, expected, actual):
#         assert expected.dumps() == actual
#
#
# def test_node():
#     with raises(TypeError):
#         TikzNode(at='(1,1)')
#     with raises(TypeError):
#         TikzNode(at=(1, 2))
