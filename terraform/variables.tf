variable "ami_id" {
  default = "ami-0c429fe566b360025"
}

variable "myip" {
  description = "A continuación indicar la IP desde donde se va a conectar al servidor web y la instancia ec2. Revisar en https://www.cualesmiip.com/"
}

variable "instance_type" {
  description = "Tipo de instancia a levantar en AWS. Por defecto es t2.micro. Si se quedase corta, se podría ampliar a t2.small o t2.medium"
  default     = "t2.small"
}