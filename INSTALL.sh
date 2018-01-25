#!/bin/bash 

# Source directory:
DIR=`dirname $0`

# Install directory:
PREFIX=$DIR

# Any location provided?
if [ "$1" != "" ]; then
    PREFIX=$1
fi

BIN=$PREFIX/bin
LIB=$PREFIX/lib

# Create directories if needed:
mkdir -p "$PREFIX"/{bin,lib}

# Create Python virtual environment:
VENV=$LIB/rarefaction
virtualenv $VENV
. $VENV/bin/activate

# PIP
pip install --upgrade pip

# RAREFACTION
pip install $DIR/

# BIN
cp $DIR/install/rarefaction $BIN/rarefaction


