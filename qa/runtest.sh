#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

pushd "${SCRIPT_DIR}/.." > /dev/null

# fail if smth fails
# the whole env will be running if test suite fails so you can debug
set -e

# for debugging this script, b/c I sometimes get
# unable to prepare context: The Dockerfile (Dockerfile.tests) must be within the build context (.)
set -x

# test coverage threshold
COVERAGE_THRESHOLD=50

export TERM=xterm
TERM=${TERM:-xterm}

# set up terminal colors
NORMAL=$(tput sgr0)
RED=$(tput bold && tput setaf 1)
GREEN=$(tput bold && tput setaf 2)
YELLOW=$(tput bold && tput setaf 3)

printf "%sCreate Virtualenv for Python deps ..." "${NORMAL}"

check_python_version() {
    python3 tools/check_python_version.py 3 6
}

function prepare_venv() {
    VIRTUALENV=$(which virtualenv)
    if [ $? -eq 1 ]
    then
        # python36 which is in CentOS does not have virtualenv binary
        VIRTUALENV=$(which virtualenv-3)
    fi

    ${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 "$(which pip3)" install -r requirements.txt && python3 "$(which pip3)" install -r test_requirements.txt
    if [ $? -ne 0 ]
    then
        printf "%sPython virtual environment can't be initialized%s" "${RED}" "${NORMAL}"
        exit 1
    fi
    printf "%sPython virtual environment initialized%s\n" "${YELLOW}" "${NORMAL}"
}

check_python_version

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

here=$(pwd)

export PYTHONPATH=${here}/

# this script is copied by CI, we don't need it
rm -f env-toolkit

echo "*****************************************"
echo "*** Cyclomatic complexity measurement ***"
echo "*****************************************"
radon cc -s -a -i venv .

echo "*****************************************"
echo "*** Maintainability Index measurement ***"
echo "*****************************************"
radon mi -s -i venv .

echo "*****************************************"
echo "*** Unit tests ***"
echo "*****************************************"

echo "Starting test suite"
DISABLE_AUTHENTICATION=1 PYTHONDONTWRITEBYTECODE=1 python3 "$(which pytest)" --cov=gateway/ --cov-report term-missing --cov-fail-under=$COVERAGE_THRESHOLD -vv tests
printf "%stests passed%s\n\n" "${GREEN}" "${NORMAL}"

`which codecov` --token=b2147eb8-2c22-486c-a417-220b36ceceb5

popd > /dev/null
