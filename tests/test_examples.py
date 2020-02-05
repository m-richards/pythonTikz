#!/usr/bin/python
"""
Tests that the example files match the cached example output. Note that this
could be done in bash with git diff, but is written like this to integrate
with the rest of the pytest suite.
"""

import pytest
import os
import difflib


def test_example_tikzdraw():
    if str(os.getcwd()).endswith('tests'):
        expected_tex_path = r'examples_reference/tikzdraw.tex'
        actual_tex_path = r'../examples/tikzdraw.tex'
    else:  # Assume we are at root
        expected_tex_path = r'tests/examples_reference/tikzdraw.tex'
        actual_tex_path = r'examples/tikzdraw.tex'
    if os.path.exists(expected_tex_path):
        expected_tex = open(expected_tex_path, 'r')
    else:
        pytest.fail(f"{expected_tex_path} not found. \nIf you have"
                    " just added a "
                    f"new example, a copy of the .tex file\nmust go in"
                    f" 'tests/examples_reference/'. This cached copy is used\n"
                    "to check the output for changes when api changes.")
    if os.path.exists(expected_tex_path):
        actual_tex = open(actual_tex_path, 'r')
    else:
        expected_tex.close()
        pytest.fail(f"Something has gone wrong, {actual_tex_path} does not "
                    f"exist.", False)
    diff = list(difflib.ndiff(expected_tex.readlines(),
                actual_tex.readlines()))
    changes = [l for l in diff if
               l.startswith('+') or l.startswith('-')]
    if len(changes) == 0:
        return
    difftext = ''.join(diff)
    pytest.fail(msg=f'File diff is not null:\n{difftext}', pytrace=False)


def test_example_tikzplot():
    if str(os.getcwd()).endswith('tests'):
        expected_tex_path = r'examples_reference/tikzplot.tex'
        actual_tex_path = r'../examples/tikzplot.tex'
    else:  # Assume we are at root
        expected_tex_path = r'tests/examples_reference/tikzplot.tex'
        actual_tex_path = r'examples/tikzplot.tex'
    if os.path.exists(expected_tex_path):
        expected_tex = open(expected_tex_path, 'r')
    else:
        pytest.fail(f"{expected_tex_path} not found. \nIf you have"
                    " just added a "
                    f"new example, a copy of the .tex file\nmust go in"
                    f" 'tests/examples_reference/'. This cached copy is used\n"
                    "to check the output for changes when api changes.")
    if os.path.exists(expected_tex_path):
        actual_tex = open(actual_tex_path, 'r')
    else:
        expected_tex.close()
        pytest.fail(f"Something has gone wrong, {actual_tex_path} does not "
                    f"exist.", False)
    diff = list(difflib.ndiff(expected_tex.readlines(),
                actual_tex.readlines()))
    changes = [l for l in diff if
               l.startswith('+') or l.startswith('-')]
    if len(changes) == 0:
        return
    difftext = ''.join(diff)
    pytest.fail(msg=f'File diff is not null:\n{difftext}', pytrace=False)
