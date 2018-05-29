#!/bin/bash


autopep8 --diff $1
autopep8 --in-place --aggressive --aggressive $1
