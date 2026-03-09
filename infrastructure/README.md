# AWS Infrastructure for Cafe-Lumiere

This directory contains Terraform configuration to build a simple AWS environment matching the user's request:

- **Region**: `us-east-1`
- **VPC**: new VPC with a single public subnet in `us-east-1a`
- **Internet access**: Internet Gateway, route table, association
- **Security Group**: allows all ingress/egress (0.0.0.0/0)
- **EC2 Instances**: 3 `t3.medium` instances with public IP, all in the same subnet

## Usage

1. Install [Terraform](https://www.terraform.io/).
2. Configure AWS credentials (e.g. via `~/.aws/credentials` or environment variables).
3. Initialize and apply configuration:

   ```sh
   cd infrastructure
   terraform init
   terraform apply -var "key_name=YOUR_KEY_PAIR_NAME"
   ```

   Replace `YOUR_KEY_PAIR_NAME` with the name of an existing EC2 key pair in the region.

4. After apply completes, Terraform will output the public IPs of the instances and the VPC ID.

5. Tear down when finished:

   ```sh
   terraform destroy -var "key_name=YOUR_KEY_PAIR_NAME"
   ```


> ⚠️ **Note:** The security group currently allows all traffic; restrict it appropriately before deploying real workloads.  For Jenkins/SonarQube, consider separate instances or groups as needed.
