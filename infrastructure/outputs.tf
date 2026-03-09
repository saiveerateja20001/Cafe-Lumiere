output "public_ips" {
  description = "Public IPs of the instances"
  value       = aws_instance.app.*.public_ip
}

output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.this.id
}
