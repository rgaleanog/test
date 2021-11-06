#!/bin/sh
source ".local/bin/activate"

cd todo-list-aws
sam validate --template template.yaml
sam build --use-container