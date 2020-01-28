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

# Check if a command line argument was provided as an input argument.
while getopts ":p:cdh" opt; do
  case $opt in
    p)
      python=$OPTARG
      ;;
    c)
      clean=TRUE
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
export PYTHONPATH=$PYTHONPATH:$PWD

# Run the examples and tests
python_version=$($python --version |& sed 's|Python \(.\).*|\1|g' | head -n 1)

# Run the examples and tests
python_version_long=$($python --version |& sed 's|Python \(.*\)|\1|g' | head -n 1)

if [ "$python_version" = '3' ]; then
    # Check code guidelines
    echo -e '\e[32mChecking for code style errors \e[0m'
    if ! flake8 pythontikz examples tests --exclude pythontikz/_version.py; then
		echo -e '\e[31mCode style tests failed. Tests Aborted. \e[0m'
        exit 1
    fi
fi


if [ "$python_version" = '2' ]; then
	echo -e '\e[31mPython 2 is unsupported. Tests Aborted. \e[0m'
    exit 1
else
    main_folder=.
fi

echo -e '\e[32mTesting tests directory\e[0m'
if ! $python "$(command -v nosetests)" --with-coverage tests/*; then
	echo -e '\e[31mNose Unit Tests Failed. Tests Aborted. \e[0m'
    exit 1
fi
mv .coverage{,.tests}

if [ "$python_version" = '2' ]; then
    cd ..
fi


count=0
echo -e '\e[32mTesting example scripts'"$f"'\e[0m'
for f in "$main_folder"/examples/*.py; do
    echo -e '\e[32m\t '"$f"'\e[0m'
    if ! $python "$(command -v coverage)" run "$f"; then
		echo -e '\e[31mTesting '"$f"' Failed. Tests Aborted. \e[0m'
        exit 1
    fi
    ((count ++))
    mv .coverage .coverage.example$count
done

coverage combine

if [ "$clean" = 'TRUE' ]; then
    rm -- *.pdf *.log *.aux *.tex *.fls *.fdb_latexmk > /dev/null
fi


if [[ "$nodoc" != 'TRUE' && "$python_version" == "3" && "$python_version_long" != 3.3.* && "$python_version_long" != 3.4.* ]]; then
    echo -e '\e[32mChecking for errors in docs and docstrings: Examples\e[0m'
    cd docs
    set -e
    ./create_doc_files.sh -p "$python"
    make clean
    set +e
    echo -e '\e[32mChecking for errors in docs and docstrings: Codebase\e[0m'
    if ! $python "$(command -v sphinx-build)" -b html -d build/doctrees/ source build/html -nW; then
		echo -e '\e[31mSphinx Build Tests Failed. Tests Aborted. \e[0m'
        exit 1
    fi
fi