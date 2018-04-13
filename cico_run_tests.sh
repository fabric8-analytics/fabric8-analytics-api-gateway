#!/bin/bash

set -ex

. cico_setup.sh

build_image
prep(){
	yum -y update
	yum install -y epel-release
	yum install -y gcc python34-pip python34-requests python34-devel
	yum clean all
	pip3 install -U pip
	pip3 install pytest
}

prep


make test

push_image
