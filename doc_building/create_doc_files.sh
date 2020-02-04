#!/usr/bin/env bash
# Script to generate the automodule sphinx contents for api documentation
# Note script must be run from directory above to work
# Optional named arguments:
#      -p COMMAND: the python command that should be used, e.g. -p python3

set -e

# Default values
python="python"

# Check if a command line argument was provided as an input argument.
while getopts "p:" opt; do
  case $opt in
    p)
      python=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

ARGS='--separate --force --no-headings --no-toc'

echo Cleaning pythontikz and examples
rm -rf source/pythontikz/*
rm -rf source/examples/*
rm -rf source/_static/examples/*

sphinx-apidoc -o source/pythontikz/ ../pythontikz/ $ARGS
echo Removing file source/pythontikz/pythontikz.rst
rm source/pythontikz/pythontikz.rst
echo Removing file source/pythontikz/pythontikz.base_classes.rst
rm source/pythontikz/pythontikz.base_classes.rst

for f in ../examples/*.py; do
    echo $f
    name=`echo $f | cut -d'/' -f3 | cut -d'.' -f1`
    echo $name
    rst=source/examples/${name}.rst
    $python gen_example_title.py "$name" > $rst
    echo Creating file ${rst}
    echo .. automodule:: examples.$name >> $rst
    echo >> $rst

    echo The code >> $rst
    echo -------- >> $rst
    echo ".. literalinclude:: /../$f" >> $rst
    echo "    :start-after: begin-doc-include" >> $rst
    echo >> $rst

    echo The generated files >> $rst
    echo ------------------- >> $rst
    # Compiling examples to png
    cd source/_static/examples
    echo $PWD
    echo $python ../../../$f
    $python ../../../$f > /dev/null
    rst=../../../$rst
    for pdf in ${name}*.pdf; do
        convert $pdf ${pdf}.png
        echo ".. literalinclude:: /_static/examples/${pdf%.pdf}.tex" >> $rst
        echo "    :language: latex" >> $rst
        echo "    :linenos:" >> $rst
        echo "    :caption: ${pdf%.pdf}.tex" >> $rst
        echo >> $rst
        echo "$pdf" >> $rst
        echo >> $rst
        for figure in ${pdf}*.png; do
            echo ".. figure:: /_static/examples/${figure}" >> $rst
        done
    done
    rm -f *.pdf *.aux *.log *.fls *.fdb_latexmk
    cd ../../..

done
