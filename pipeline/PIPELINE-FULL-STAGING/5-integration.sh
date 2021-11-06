#!/bin/sh
source ".local/bin/activate"

cd todo-list-aws/test/integration
pytest -s --gateway z9fedswxh3 TestIntegration.py
if [[ $? -ne 0 ]]
then
    exit 1
fi