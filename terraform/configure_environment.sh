#!/usr/bin/env bash


# Download terraform 
wget https://releases.hashicorp.com/terraform/0.14.3/terraform_0.14.3_linux_amd64.zip
# Unzip terraform
unzip terraform_0.14.3_linux_amd64.zip
# remove terraform zip
rm -f terraform_0.14.3_linux_amd64.zip

# Set permissions properly
chmod +x terraform
chmod +x resources/get-ssh-key.sh
# terraform init
./terraform init
# terraform validate
./terraform validate
# terraform plan -out plan
./terraform plan -out=plan
# terraform apply plan
yes | ./terraform apply plan

# clean wokspace
rm -rf .terraform