#!/usr/bin/python
"""
This example shows PGFPlot drawing capabilities.

..  :copyright: (c) 2020 by Matthew Richards.
    This example is inferred from the documentation and may not be the most
    optimal use of these classes. I do not use PGFPlot.
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex import NoEscape

from pythontikz import Document
from pythontikz.common import Plot, TikzPicture, Axis, TikzOptions

# create document
doc = Document(documentclass='standalone')

with doc.create(TikzPicture()) as pic:
    with pic.create(Axis(options={
        'axis x line': 'center',
        'axis y line': 'middle',
        'tick align': 'outside',
    })) as pic:
        p = Plot(name=NoEscape(r"$-\sin(x) + 4$"), func=r"-sin(\x r)+4",
                 # coordinates=[(1,1), (2,2), (3,-3)],
                 error_bar_deltas=None,
                 options=TikzOptions({
                     'domain': '-10:10',
                     'samples': 80,
                     'mark size': '0.6pt'
                 }),
                 use_auto_format=True
                 )
        pic.append(p)


if __name__ == '__main__':
    print(doc.dumps())
    doc.generate_pdf('tikzplot', clean_tex=False, compiler='pdflatex')
