#!/bin/sh
source ".local/bin/activate"

cd todo-list-aws/test/integration
pytest -s --gateway rogwj4tu2m TestIntegration.py

if [[ $? -ne 0 ]]
then
    exit 1
fi