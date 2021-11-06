#/bin/sh
#python3 -m venv venv
#. ./venv/bin/activate
#pip install -r todo-list-aws/pipeline/PIPELINE-FULL-STAGING/requirements.txt


#pip install virtualenv --user
# Get an unique venv folder to using *inside* workspace
VENV=".local"

# Initialize new venv
python3 -m venv "$VENV"

# Update pip
PS1="${PS1:-}" source "$VENV/bin/activate"

python3 --version

pip3 install -r todo-list-aws/pipeline/PIPELINE-FULL-STAGING/requirements.txt
export AWS_DEFAULT_REGION=us-east-1

docker rm -f $(docker ps -a -q)
docker run -d -p 8000:8000 amazon/dynamodb-local
docker ps