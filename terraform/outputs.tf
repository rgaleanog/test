output "key_pair" {
  value = tls_private_key.this.private_key_pem
}

output "s3_bucket_production" {
  value = aws_s3_bucket.s3_bucket_production.id
}

output "s3_bucket_staging" {
  value = aws_s3_bucket.s3_bucket_staging.id
}

output "jenkins_instance_id" {
  value = aws_instance.jenkins.id
}

output "jenkins_instance_security_group_id" {
  value = aws_security_group.allow_all.id
}
output "ssh_connection" {
  value = "ssh -i resources/key.pem ec2-user@${aws_instance.jenkins.public_ip}"
}
output "jenkins_url" {
  value = "http://${aws_instance.jenkins.public_ip}:8080"
}

output "public_ip" {
  value = aws_instance.jenkins.public_ip
}
