#!/bin/bash

# fail if smth fails
# the whole env will be running if test suite fails so you can debug
set -e

# for debugging this script, b/c I sometimes get
# unable to prepare context: The Dockerfile (Dockerfile.tests) must be within the build context (.)
set -x

echo "Create Virtualenv for Python deps ..."
function prepare_venv() {
    VIRTUALENV=`which virtualenv`
    if [ $? -eq 1 ]; then
        # python34 which is in CentOS does not have virtualenv binary
        VIRTUALENV=`which virtualenv-3`
    fi

    ${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt && python3 `which pip3` install -r test_requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

here=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

IMAGE_NAME=${IMAGE_NAME:-registry.devshift.net/fabric8-analytics/f8a-api-gateway}
TEST_IMAGE_NAME=${IMAGE_NAME}

TIMESTAMP="$(date +%F-%H-%M-%S)"
CONTAINER_NAME="api_gateway-${TIMESTAMP}"

gc() {
  retval=$?
  # FIXME: make this configurable
  echo "Stopping test containers"
  docker stop ${CONTAINER_NAME} || :
  echo "Removing test containers"
  docker rm -v ${CONTAINER_NAME} || :
  exit $retval
}

trap gc EXIT SIGINT

if [ "$REBUILD" == "1" ] || \
     !(docker inspect $IMAGE_NAME > /dev/null 2>&1); then
  echo "Building $IMAGE_NAME for testing"
  make fast-docker-build
fi

if [ "$REBUILD" == "1" ] || \
     !(docker inspect $TEST_IMAGE_NAME > /dev/null 2>&1); then
  echo "Building $TEST_IMAGE_NAME test image"
  make fast-docker-build-tests
fi

export PYTHONPATH=`pwd`/

echo "Starting test suite"
DISABLE_AUTHENTICATION=1 PYTHONDONTWRITEBYTECODE=1 python3 `which pytest` --cov=gateway/ --cov-report term-missing -vv tests
echo "Test suite passed \\o/"
