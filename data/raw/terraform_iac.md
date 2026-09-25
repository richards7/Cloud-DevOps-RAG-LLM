# Terraform (Infrastructure as Code)

Terraform lets you define cloud infrastructure in declarative configuration files
(HCL — HashiCorp Configuration Language), then plan and apply changes safely and
repeatably across AWS, Azure, GCP, and many other providers.

## Core concepts
- **Provider**: the plugin that talks to a specific cloud/API (aws, google, azurerm).
- **Resource**: a piece of infrastructure to create (e.g. `aws_instance`, `google_storage_bucket`).
- **State**: Terraform tracks what it created in a state file (`terraform.tfstate`) so
  it knows what to change on the next apply. State should be stored remotely (e.g. an
  S3 bucket + DynamoDB lock table) for team use, never just committed to Git.
- **Module**: a reusable, packaged set of resources — like a function for infrastructure.

## Basic example
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

## Core workflow
```bash
terraform init      # download providers, set up backend
terraform plan       # show what WOULD change, without changing anything
terraform apply      # apply the changes (asks for confirmation)
terraform destroy    # tear down everything Terraform manages
```

## Why IaC matters (interview-relevant)
- **Repeatability**: the same config produces the same infrastructure every time,
  eliminating "it worked when I clicked it manually" drift.
- **Version control**: infrastructure changes go through Git history, code review,
  and PRs — just like application code.
- **Plan before apply**: `terraform plan` shows exactly what will change before it
  happens, reducing the risk of surprise deletions/modifications.

## Common errors & fixes
- **"Error acquiring the state lock"**: another `apply`/`plan` is in progress, or a
  previous run crashed without releasing the lock — check the lock table (e.g.
  DynamoDB) and use `terraform force-unlock <lock-id>` only if you're sure no other
  process is running.
- **State drift** (resource changed manually outside Terraform): run `terraform plan`
  to see the diff, and either update the config to match reality or `terraform apply`
  to force it back to the declared state.
- **"Resource already exists"**: someone created the resource outside Terraform, or a
  previous apply partially failed — use `terraform import` to bring an existing
  resource under Terraform's management instead of recreating it.
- **Provider authentication errors**: check environment variables/credentials file for
  the target cloud are set correctly (e.g. `AWS_ACCESS_KEY_ID`, or `gcloud auth
  application-default login` for GCP).
