Library usage
=============
We assume the reader is familiar with the `usage principles of PyLaTeX <https://jeltef.github.io/PyLaTeX/latest/usage.html>`_.
If not, it might be work checking that.

pythontikz package Intent
-------------------------
pythontikz is intended to integrate with  and extend the two use cases of PyLaTeX;
Generating LaTeX code, and compiling LaTeX documents. Additionally, it aims to 
cater towards producing standalone LaTeX documents containing TikZ using
the standalone documentclass.


Workflow Using Standalone
~~~~~~~~~~~~~~~~~~~~~~~~~
For writing documents with a large number of TikZ pictures, it can be of benefit
to seperate these into individual files to help with compile time. Using
the standalone package and documentclass one can include the output pdf image
as a figure in the main document, avoiding the need to "typeset" each picture
on each compilation. Additionally, figures become easier to maintain, modify
and reuse, as there is a one-to-one correspondence between the python file,
tex file and output figure.

