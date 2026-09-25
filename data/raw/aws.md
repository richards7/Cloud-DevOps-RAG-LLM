# AWS (Amazon Web Services)

## Core compute
- **EC2**: virtual machines. Instance types (t3, m5, c5...) trade off CPU/RAM/network.
  Launch: choose AMI, instance type, key pair, security group, subnet.
- **Lambda**: serverless functions, billed per invocation/duration, max 15 min runtime.
- **ECS/Fargate**: run containers without managing servers (Fargate) or on managed EC2 (ECS).
- **Auto Scaling Groups**: automatically add/remove EC2 instances based on load.

## Storage
- **S3**: object storage. Buckets are globally unique. Storage classes: Standard, IA
  (Infrequent Access), Glacier (archive, cheap, slow retrieval).
- **EBS**: block storage attached to a single EC2 instance (like a virtual hard disk).
- **EFS**: shared file storage, mountable by multiple EC2 instances at once.

## Databases
- **RDS**: managed relational DB (MySQL, PostgreSQL, etc.) — handles backups, patching.
- **DynamoDB**: managed NoSQL, key-value/document store, single-digit ms latency.

## Networking
- **VPC**: your isolated network. Subnets (public/private), route tables, internet gateway.
- **Security Groups**: instance-level firewall (stateful — allow reply traffic automatically).
- **NACLs**: subnet-level firewall (stateless — must allow both directions explicitly).
- **ALB/NLB**: Application Load Balancer (HTTP/HTTPS, layer 7) vs Network Load Balancer
  (TCP/UDP, layer 4, higher throughput).

## IAM
- **Users/Groups/Roles**: roles are assumed by services (e.g. an EC2 instance) instead of
  using long-lived credentials — the preferred, more secure pattern.
- **Policies**: JSON documents defining allowed/denied actions on resources.

## Messaging/eventing
- **SNS**: pub/sub notifications (fan-out to multiple subscribers).
- **SQS**: message queue, decouples producers/consumers.

## CLI basics
```bash
aws configure                         # set access key, secret, region
aws s3 ls                             # list buckets
aws s3 cp file.txt s3://mybucket/     # upload
aws ec2 describe-instances
aws logs tail /aws/lambda/my-fn --follow
```

## Common errors & fixes
- **"Access Denied" (S3/IAM)**: check the IAM policy attached to the user/role has the
  specific action (e.g. `s3:GetObject`) and resource ARN allowed — a missing bucket
  policy or an explicit `Deny` elsewhere overrides an `Allow`.
- **EC2 instance unreachable**: check security group inbound rules (port + source IP),
  confirm the instance has a public IP if accessed from the internet, and check the
  route table has a route to an Internet Gateway for public subnets.
- **"InvalidClientTokenId"**: credentials are wrong/expired — re-run `aws configure` or
  check the instance's IAM role if running from EC2.
- **Lambda timeout**: default is 3s; check `--timeout` setting, and check downstream
  calls (DB, API) aren't the actual bottleneck via CloudWatch Logs.
