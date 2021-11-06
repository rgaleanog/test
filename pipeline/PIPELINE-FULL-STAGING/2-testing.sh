#!/bin/sh
source ".local/bin/activate"

flake8 "todo-list-aws/src"
if [[ $? -ne 0 ]]
then
    exit 1
fi

radon cc todo-list-aws/src -n A -x C -a
if [[ $? -ne 0 ]]
then
    exit 1
fi

bandit -r todo-list-aws/src
if [[ $? -ne 0 ]]
then
    exit 1
fi

cd todo-list-aws/test/unit
coverage run TestToDoTableClass.py
if [[ $? -ne 0 ]]
then
    exit 1
fi