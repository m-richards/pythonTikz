# -*- coding: utf-8 -*-
"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os
import subprocess
import errno
from .base_classes import Command, Container, LatexObject
import pylatex
from pylatex import Package
from pylatex.errors import CompilerError
from pylatex.utils import rm_temp_dir
import pylatex.config as cf


class Document(pylatex.Document):
    r"""
    A class that contains a full LaTeX document.

    If needed, you can append stuff to the preamble or the packages.
    For instance, if you need to use ``\maketitle`` you can add the title,
    author and date commands to the preamble to make it work.

    """

    def __init__(self, default_filepath='default_filepath', *,
                 documentclass='article', document_options=None, fontenc=None,
                 inputenc=None, font_size=None, lmodern=None,
                 textcomp=None, microtype=None, page_numbers=None, indent=None,
                 geometry_options=None, data=None):
        r"""
        Args
        ----
        default_filepath: str
            The default path to save files.
        documentclass: str or `~pylatex.base_classes.command.Command`
            The LaTeX class of the document.
        document_options: str or `list`
            The options to supply to the documentclass
        fontenc: str
            The option for the fontenc package. If it is `None`, the fontenc
            package will not be loaded at all.
        inputenc: str
            The option for the inputenc package. If it is `None`, the inputenc
            package will not be loaded at all.
        font_size: str
            The font size to declare as normalsize
        lmodern: bool
            Use the Latin Modern font. This is a font that contains more glyphs
            than the standard LaTeX font.
        textcomp: bool
            Adds even more glyphs, for instance the Euro (€) sign.
        page_numbers: bool
            Adds the ability to add the last page to the document.
        indent: bool
            Determines whether or not the document requires indentation. If it
            is `None` it will use the value from the active config. Which is
            `True` by default.
        geometry_options: str or list
            The options to supply to the geometry package
        data: list
            Initial content of the document.
        """
        # preserve old default values for non standalone
        if documentclass != 'standalone':
            fontenc = 'T1' if fontenc is None else fontenc
            inputenc = 'utf8' if inputenc is None else inputenc
            lmodern = True if lmodern is None else lmodern
            textcomp = True if textcomp is None else textcomp
            page_numbers = True if page_numbers is None else page_numbers
            font_size = 'normalsize' if font_size is None else font_size

        self.default_filepath = default_filepath

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command('documentclass',
                                         arguments=documentclass,
                                         options=document_options)
        if indent is None:
            indent = cf.active.indent
        if microtype is None:
            microtype = cf.active.microtype

        # These variables are used by the __repr__ method
        self._fontenc = fontenc
        self._inputenc = inputenc
        self._lmodern = lmodern
        self._indent = indent
        self._microtype = microtype

        packages = []

        if fontenc is not None:
            packages.append(Package('fontenc', options=fontenc))
        if inputenc is not None:
            packages.append(Package('inputenc', options=inputenc))
        if lmodern:
            packages.append(Package('lmodern'))
        if textcomp:
            packages.append(Package('textcomp'))
        if page_numbers:
            packages.append(Package('lastpage'))
        if not indent:
            packages.append(Package('parskip'))
        if microtype:
            packages.append(Package('microtype'))

        if geometry_options is not None:
            packages.append(Package('geometry', options=geometry_options))

        super().__init__(data=data)

        # Usually the name is the class name, but if we create our own
        # document class, \begin{document} gets messed up.
        self._latex_name = 'document'

        self.packages |= packages
        self.variables = []

        self.preamble = []

        if not page_numbers:
            self.change_document_style("empty")

        # No colors have been added to the document yet
        self.color = False
        self.meta_data = False
        if font_size is not None:
            self.append(Command(command=font_size))

    def _propagate_packages(self):
        r"""Propogate packages.

        Make sure that all the packages included in the previous containers
        are part of the full list of packages.
        """

        super()._propagate_packages()

        for item in self.preamble:
            if isinstance(item, LatexObject):
                if isinstance(item, Container):
                    item._propagate_packages()
                for p in item.packages:
                    self.packages.add(p)

    def generate_pdf(self, filepath=None, *, clean=True, clean_tex=True,
                     compiler=None, compiler_args=None, silent=True):
        """Generate a pdf file from the document.

        Args
        ----
        filepath: str
            The name of the file (without .pdf), if it is `None` the
            ``default_filepath`` attribute will be used.
        clean: bool
            Whether non-pdf files created that are created during compilation
            should be removed.
        clean_tex: bool
            Also remove the generated tex file.
        compiler: `str` or `None`
            The name of the LaTeX compiler to use. If it is None, PyLaTeX will
            choose a fitting one on its own. Starting with ``latexmk`` and then
            ``pdflatex``.
        compiler_args: `list` or `None`
            Extra arguments that should be passed to the LaTeX compiler. If
            this is None it defaults to an empty list.
        silent: bool
            Whether to hide compiler output
        """

        if compiler_args is None:
            compiler_args = []

        filepath = self._select_filepath(filepath)
        filepath = os.path.join('.', filepath)

        cur_dir = os.getcwd()
        dest_dir = os.path.dirname(filepath)
        basename = os.path.basename(filepath)

        if basename == '':
            basename = 'default_basename'

        os.chdir(dest_dir)

        self.generate_tex(basename)

        if compiler is not None:
            compilers = ((compiler, []),)
        else:
            latexmk_args = ['--pdf']

            compilers = (
                ('latexmk', latexmk_args),
                ('pdflatex', [])
            )

        main_arguments = ['--interaction=nonstopmode', basename + '.tex']

        os_error = None

        for compiler, arguments in compilers:
            command = [compiler] + arguments + compiler_args + main_arguments

            try:
                output = subprocess.check_output(command,
                                                 stderr=subprocess.STDOUT)
            except (OSError, IOError) as e:
                # Use FileNotFoundError when python 2 is dropped
                os_error = e

                if os_error.errno == errno.ENOENT:
                    # If compiler does not exist, try next in the list
                    continue
                raise
            except subprocess.CalledProcessError as e:
                # For all other errors print the output and raise the error
                # try to catch windows 'perl.exe' not found so that we can
                # try pdflatex instead rather than just crashing
                output = str(e.output.decode())
                import re
                import sys
                output = re.sub(r'\s+', '', output)
                if "couldnotfindthescriptengine'perl.exe'" in output:
                    print("ERROR: Compiler latexmk failed since the dependency"
                          " 'perl.exe' was not found. Trying alternative "
                          "compilers. Specify the compiler in future to avoid"
                          " this check if not using latexmk.",
                          file=sys.stderr)
                    continue
                else:
                    print(e.output.decode())
                    raise e
            else:
                if not silent:
                    print(output.decode())

            if clean:
                try:
                    # Try latexmk cleaning first
                    subprocess.check_output(['latexmk', '-c', basename],
                                            stderr=subprocess.STDOUT)
                except (OSError, IOError, subprocess.CalledProcessError):
                    # Otherwise just remove some file extensions.
                    extensions = ['aux', 'log', 'out', 'fls',
                                  'fdb_latexmk']

                    for ext in extensions:
                        try:
                            os.remove(basename + '.' + ext)
                        except (OSError, IOError) as e:
                            # Use FileNotFoundError when python 2 is dropped
                            if e.errno != errno.ENOENT:
                                raise
                rm_temp_dir()

            if clean_tex:
                os.remove(basename + '.tex')  # Remove generated tex file

            # Compilation has finished, so no further compilers have to be
            # tried
            break

        else:
            # Notify user that none of the compilers worked.
            raise (CompilerError(
                'No LaTex compiler was found\n'
                'Either specify a LaTex compiler '
                'or make sure you have latexmk or pdfLaTex installed.'
            ))

        os.chdir(cur_dir)
