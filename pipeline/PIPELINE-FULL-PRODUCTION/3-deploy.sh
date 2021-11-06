#!/bin/sh
source ".local/bin/activate"

cd todo-list-aws
yes|sam deploy --config-env production