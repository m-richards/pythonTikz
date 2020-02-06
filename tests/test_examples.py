#!/usr/bin/python

"""
Tests that the example files match the cached example output. Note that this
could be done in bash with git diff, but is written like this to integrate
with the rest of the pytest suite.
"""
from io import StringIO

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

import os.path

def test_examples():
    expected_tex_path = 'examples_reference/tikzdraw.tex'
    actual_tex_path = '../examples/tikzdraw.tex'

    if os.path.exists(expected_tex_path):
        expected_tex = open(expected_tex_path, 'r')
    else:
        expected_tex = StringIO("")

    if os.path.exists(actual_tex_path):
        expected_tex = open(actual_tex_path, 'r')
    else:
        expected_tex = StringIO("")

    actual_tex = open(actual_tex_path)

    for n, e_line, a_line in enumerate(zip(expected_tex, actual_tex), start=1):
        if e_line != a_line:
            pytest.fail(msg=(f"Example output has change on line {n}."
                        f"{e_line} != {a_line}"))


    expected_tex.close()
    actual_tex.close()