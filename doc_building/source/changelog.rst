Change Log
==========

All notable changes to this project will be documented on this page.  This
project adheres to `Semantic Versioning <http://semver.org/>`_.

.. highlight:: bash

Unreleased
-----------------------------------
..  #_ - `docs <../latest/>`__
  
See these docs for changes that have not yet been released and are
only present in the development version.
This version might not be stable, but to install it use::

    pip install git+https://github.com/m-richards/pythonTikz.git
	
(This might not work yet)

Added
~~~~~
- New extension of basic TikZ drawing functions to support arcs,
  hobby shortcut paths, inline path nodes,
- Extended support for coordinates and coordinate arithmetic using calc.
- A very limited selection of TikZ libraries are automatically detected
  and added to the preamble.

Fixed
~~~~~
- TikZCoordinate subtraction now produces the right result.
- TikZNode now produces valid output when position argument is supplied.

0.1 - 2020-01-27
-------------------
Initial version split from PyLaTeX fork.

