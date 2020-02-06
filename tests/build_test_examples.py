#!/usr/bin/python
"""Script to automatically produce the test_examples.py script which
dynamically updates to test new examples

Do not manually run in a shell where $PWD is not the directory this file is
located in. Ideally just run as part of testall.sh

The tests
"""

import os.path
from os.path import join

test_examples_docstring = """
Tests that the example files match the cached example output. Note that this
could be done in bash with git diff, but is written like this to integrate
with the rest of the pytest suite.
"""


def indent_write(fp, indent=0, text="", *args, **kwargs):
    indent_text = indent * 4 * " "  # use space indents to make strings
    # behave better
    return fp.write(f"{indent_text}{text}\n", *args, **kwargs)


def write_test(fp, example_filename, example_dir, cache_dir):
    example_filename = example_filename.split(".")[0]
    # full_cache_path = join(cache_dir, example_filename)
    # full_current_example_path = join(example_dir, example_filename)
    lines = [
        (0, f"def test_example_{example_filename}():"),
        (1, "curr_dir = os.getcwd()"),
        (1, "if str(curr_dir).endswith('tests'):"),
        (2, "expected_tex_path = r'"
            f"{join('examples_reference', example_filename)}.tex'"),
        (2, "os.chdir(join('..', 'examples'))"),
        (1, "else:  # Assume we are at root"),
        (2, f"expected_tex_path = r'"
            f"{join('tests', 'examples_reference', example_filename)}.tex'"),
        (2, "os.chdir(join('.', 'examples'))"),
        (1, f"from examples.{example_filename} import doc"),
        (1, "os.chdir(curr_dir)"),
        (1, "if os.path.exists(expected_tex_path):"),
        (2, "expected_tex = open(expected_tex_path, 'r')"),
        (1, "else:"),
        (2, r"""pytest.fail(f"{expected_tex_path} not found. \nIf you have"
                    " just added a "
                    f"new example, a copy of the .tex file\nmust go in"
                    f" 'tests/examples_reference/'. This cached copy is used\n"
                    "to check the output for changes when api changes.")"""),
        (1, "cached_lines = [l.strip() for l in expected_tex.readlines()]"),
        (1, "output_str = doc.dumps()"),
        (1, r"output_lines = output_str.split('\n')"),
        (1, "# note list cast is important - stops generator consuming."),
        (1, "diff = list(difflib.unified_diff(output_lines, cached_lines))"),
        (1, """changes = [l for l in diff if
               l.startswith('+') or l.startswith('-')]"""),
        (1, "if len(changes) == 0:"),
        (2, "return"),
        # (1, "print(''.join(diff), end='')"),
        (1, "difftext = ''.join(diff)"),
        (1, r"pytest.fail(msg=f'File diff is not null:\n{difftext}', "
            r"pytrace=False)")

    ]
    fp.write("\n\n")
    for indent, text in lines:
        # use spaces so that spaces in strings above don't cause issues
        indent_text = indent * 4 * ' '
        fp.write(f"{indent_text}{text}\n")


if __name__ == "__main__":
    with open('test_examples.py', 'w') as f:
        f.write('#!/usr/bin/python\n')

        f.write(f'"""{test_examples_docstring}"""\n\n')

        f.write("import pytest\n")
        f.write("import os\n")
        f.write("from os.path import join\n")
        f.write("import difflib\n")
        if str(os.getcwd()).endswith("tests"):
            example_dir = join("..", "examples")
            cache_dir = join(".", "examples_reference")
        else:  # called from root
            raise OSError("Script should only be run from within the /tests "
                          "directory.")
        all_examples = [g for g in os.listdir(example_dir) if (
                        os.path.isfile(os.path.join(example_dir, g))
                        and g.endswith(".py"))]
        for example in all_examples:
            write_test(f, example, example_dir, cache_dir)
