#!/usr/bin/python
"""
This example shows TikZ drawing capabilities.

..  :copyright: (c) 2020 by Matthew Richards
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pythontikz import (Document, TikzPicture, TikzNode, TikzDraw,
                        TikzRectCoord, TikzCalcCoord, TikzLibrary)


# create document
from pythontikz.paths import TikzRadius

doc = Document(documentclass='standalone')

# can manually add tikz libraries to document
# (some are detected automatically, like calc)

doc.preamble.append(TikzLibrary("arrows.meta"))
doc.preamble.append(TikzLibrary("decorations.markings"))


# add our sample drawings
with doc.create(TikzPicture()) as pic:

    # define a coordinate so that we can reposition the origin easily
    # after the latex is produced
    orig = TikzCalcCoord(handle="orig", at=TikzRectCoord(5, -3))
    orig_handle = orig.get_handle()  # handle label to coordinate
    pic.append(orig)  # add definition of coordinate

    pic.append(TikzDraw([orig_handle, 'circle', TikzRadius(3)]))

    pic.append(TikzDraw([(3, 4), 'ellipse', (5, 2), TikzNode(text='Test '
                                                                  'ellipse')]))

if __name__ == "__main__":
    from os.path import basename
    # automatically set the pdf file name the same as the script name
    # note the os.path.basename is needed to ensure that we just get the
    # script name without a preceding relative path which would move
    # where the output pdf goes.
    fname = str(basename(__file__)).split('.')[0]

    doc.generate_pdf(fname, clean_tex=False)
