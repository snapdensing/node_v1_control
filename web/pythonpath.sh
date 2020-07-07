#!/bin/bash
export CURDIR=$(pwd)
cd ..
export ROOTPYTHON=$(pwd)
cd $CURDIR
export PYTHONPATH=$PYTHONPATH:$ROOTPYTHON
