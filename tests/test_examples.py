#!/usr/bin/python
"""
Tests that the example files match the cached example output. Note that this
could be done in bash with git diff, but is written like this to integrate
with the rest of the pytest suite.
"""

import pytest
import os
from os.path import join
import difflib


def test_example_tikzdraw():
    curr_dir = os.getcwd()
    if str(curr_dir).endswith('tests'):
        expected_tex_path = r'examples_reference/tikzdraw.tex'
        os.chdir(join('..', 'examples'))
    else:  # Assume we are at root
        expected_tex_path = r'tests/examples_reference/tikzdraw.tex'
        os.chdir(join('.', 'examples'))
    from examples.tikzdraw import doc
    os.chdir(curr_dir)
    if os.path.exists(expected_tex_path):
        expected_tex = open(expected_tex_path, 'r')
    else:
        pytest.fail(f"{expected_tex_path} not found. \nIf you have"
                    " just added a "
                    f"new example, a copy of the .tex file\nmust go in"
                    f" 'tests/examples_reference/'. This cached copy is used\n"
                    "to check the output for changes when api changes.")
    cached_lines = [l.strip() for l in expected_tex.readlines()]
    output_str = doc.dumps()
    output_lines = output_str.split('\n')
    # note list cast is important - stops generator consuming.
    diff = list(difflib.unified_diff(output_lines, cached_lines))
    changes = [l for l in diff if
               l.startswith('+') or l.startswith('-')]
    if len(changes) == 0:
        return
    difftext = ''.join(diff)
    pytest.fail(msg=f'File diff is not null:\n{difftext}', pytrace=False)


def test_example_tikzplot():
    curr_dir = os.getcwd()
    if str(curr_dir).endswith('tests'):
        expected_tex_path = r'examples_reference/tikzplot.tex'
        os.chdir(join('..', 'examples'))
    else:  # Assume we are at root
        expected_tex_path = r'tests/examples_reference/tikzplot.tex'
        os.chdir(join('.', 'examples'))
    from examples.tikzplot import doc
    os.chdir(curr_dir)
    if os.path.exists(expected_tex_path):
        expected_tex = open(expected_tex_path, 'r')
    else:
        pytest.fail(f"{expected_tex_path} not found. \nIf you have"
                    " just added a "
                    f"new example, a copy of the .tex file\nmust go in"
                    f" 'tests/examples_reference/'. This cached copy is used\n"
                    "to check the output for changes when api changes.")
    cached_lines = [l.strip() for l in expected_tex.readlines()]
    output_str = doc.dumps()
    output_lines = output_str.split('\n')
    # note list cast is important - stops generator consuming.
    diff = list(difflib.unified_diff(output_lines, cached_lines))
    changes = [l for l in diff if
               l.startswith('+') or l.startswith('-')]
    if len(changes) == 0:
        return
    difftext = ''.join(diff)
    pytest.fail(msg=f'File diff is not null:\n{difftext}', pytrace=False)
