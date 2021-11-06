#create a new instance of the latest Ubuntu 20.04 on an
# t3.micro node with an AWS Tag naming it "HelloWorld"
provider "aws" {
  region  = "us-east-1"
  profile = "default"
}


resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_default_vpc.default.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "http" "myip" {
  url = "http://ipv4.icanhazip.com"
}

resource "aws_default_subnet" "default_az1" {
  availability_zone = "us-east-1a"

  tags = {
    Name = "Default subnet for us-east-1a"
  }
}

resource "aws_security_group" "allow_all" {
  name        = "es-unir-ec2-jenkins-all-traffic-${random_integer.server.result}"
  description = "Allow all inbound traffic"


  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["${chomp(data.http.myip.body)}/32", "${var.myip}/32"]
    security_groups = [aws_default_security_group.default.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = aws_default_vpc.default.id

  tags = {
    Name        = "es-unir-ec2-production-jenkins-server-securityGroup"
    Country     = "es"
    Team        = "unir"
    Environment = "production"
  }
}

resource "tls_private_key" "this" {
  algorithm = "RSA"
}

module "key_pair" {
  source = "terraform-aws-modules/key-pair/aws"

  key_name   = "es-unir-keypair-${random_integer.server.result}"
  public_key = tls_private_key.this.public_key_openssh
}


resource "aws_instance" "jenkins" {
  ami           = var.ami_id # us-east-1
  instance_type = var.instance_type
  key_name      = module.key_pair.key_pair_key_name

  security_groups = [aws_security_group.allow_all.name]
  tags = {
    "Name" = "es-unir-ec2-production-jenkins-server-${random_integer.server.result}"
  }
}

resource "aws_s3_bucket" "s3_bucket_staging" {
  bucket = "es-unir-staging-s3-${random_integer.server.result}-artifacts"
  acl    = "private"

  tags = {
    Name        = "es-unir-staging-s3-${random_integer.server.result}-artifacts"
    Country     = "es"
    Team        = "unir"
    Environment = "staging"
  }

  depends_on = [random_integer.server]
}


resource "aws_s3_bucket" "s3_bucket_production" {
  bucket = "es-unir-production-s3-${random_integer.server.result}-artifacts"
  acl    = "private"

  tags = {
    Name        = "es-unir-production-s3-${random_integer.server.result}-artifacts"
    Country     = "es"
    Team        = "unir"
    Environment = "production"
  }

  depends_on = [random_integer.server]

}

resource "random_integer" "server" {
  min = 10000
  max = 99999
  keepers = {
    # Generate a new id each time we switch to a new AMI id
    ami_id = var.ami_id
  }
}

resource "null_resource" "super_secret" {
  # triggers = {
  #   hash_super_secret = sha256(tls_private_key.this.private_key_pem)
  # }

  triggers = {
    always_run = timestamp()
  }


  provisioner "local-exec" {
    command = "echo $SUPER_SECRET > key_pem "
    environment = {
      SUPER_SECRET = tls_private_key.this.private_key_pem
    }
  }
}

resource "null_resource" "create_pem" {
  # triggers = {
  #   hash_super_secret = sha256(tls_private_key.this.private_key_pem)
  # }

  triggers = {
    always_run = timestamp()
  }


  provisioner "local-exec" {
    command = "resources/get-ssh-key.sh"
  }

  depends_on = [null_resource.super_secret]
}