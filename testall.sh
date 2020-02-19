#!/usr/bin/env bash
# This script runs flake8 to test for pep8 compliance and executes all the examples and tests
# run as: testall.sh [-p COMMAND] [clean]
# Optional positional arguments
#      -c: cleans up the latex files generated
# Optional named arguments:
#      -p COMMAND: the python command that should be used, e.g. ./testall.sh -p python3
#

# Default values
python="python"
main_folder=.

# Check if a command line argument was provided as an input argument.
while getopts ":p:cdh" opt; do
  case $opt in
    p)
      python=$OPTARG
      ;;
    c)
      clean_flag=TRUE
      ;;
    d)
      nodoc=TRUE
      ;;
    h)
      echo This runs all the tests and examples and checks for pep8 compliance
      echo
      echo Options:
      echo '   -c            cleans up the latex and pdf files generated'
      echo '   -p COMMAND    the python command that should be used to run the tests'
      echo "   -d            don't execute the doc tests, they can take long"
      exit 0
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

#hack to get pythonpath and modules to behave (used to work without this)
#export PYTHONPATH=$PYTHONPATH:$PWD (doing a pip install -e . removes this need)

# Run the examples and tests
python_version=$($python --version |& sed 's|Python \(.\).*|\1|g' | head -n 1)

# Run the examples and tests
python_version_long=$($python --version |& sed 's|Python \(.*\)|\1|g' | head -n 1)

if [ "$python_version" = '3' ]; then
    # Check code guidelines
    echo -e '\e[32mChecking for code style errors \e[0m'
    if ! flake8 pythontikz examples tests; then
		echo -e '\e[31mCode style tests failed. Tests Aborted. \e[0m'
        exit 1
    fi
fi


if [ "$python_version" = '2' ]; then
	echo -e '\e[31mPython 2 is unsupported. Tests Aborted. \e[0m'
    exit 1
fi

echo -e '\e[32mTesting tests directory\e[0m'
# Setup: Building test versions of examples
cd "$main_folder"/tests/ # avoids confusing back and forth
$python build_test_examples.py
cd ../"$main_folder"

if ! coverage run --source="$main_folder"/pythontikz -m pytest -v tests/*; then
  echo -e '\e[32mCoverage Report:\e[0m'
  coverage report;
	echo -e '\e[31mUnit Tests Failed. Tests Aborted. \e[0m'
    exit 1
fi
echo -e '\e[32mCoverage Report:\e[0m'
coverage report;
mv .coverage{,.tests}


count=0
echo -e '\e[32mTesting example scripts\e[0m'
cd "$main_folder"/examples
for f in ./*.py; do
    echo -e '\e[32m\t '"$f"'\e[0m'
    # primitive check that file doesn't crash check
    if ! coverage run --source=pythontikz "$f" > /dev/null; then
		echo -e '\e[31mTesting '"$f"' Failed. Tests Aborted. \e[0m'
        exit 1
    fi
    # clean up files
#    f_no_ext=${f%.py}
#    rm -rf "$f_no_ext"'.tex'
#    rm -rf "$f_no_ext"'.pdf'
    ((count ++))
    mv .coverage .coverage.example$count
done
cd ..

coverage combine

if [ "$clean_flag" = 'TRUE' ]; then
    rm -- *.pdf *.log *.aux *.tex *.fls *.fdb_latexmk > /dev/null
fi


if [[ "$nodoc" != 'TRUE' && "$python_version" == "3" && "$python_version_long" != 3.3.* && "$python_version_long" != 3.4.* ]]; then
    echo -e '\e[32mChecking for errors in docs and docstrings: Examples\e[0m'
    cd doc_building
    set -e
    ./create_doc_files.sh -p "$python"
    make clean
    set +e
    echo -e '\e[32mChecking for errors in docs and docstrings: Codebase\e[0m'
    if ! $python "$(command -v sphinx-build)" -b html -d build/doctrees/ source build/html -nW; then
		echo -e '\e[31mSphinx Build Tests Failed. Tests Aborted. \e[0m'
        exit 1
    fi
    # documentation is built into doc_building/build
    # copy to docs so that gh pages can find it




fi