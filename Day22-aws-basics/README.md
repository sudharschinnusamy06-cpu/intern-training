# Day 22 - AWS Basics

## What I learned
- Cloud computing basics - renting compute/storage instead of owning servers
- Why IAM users are used instead of root account (least privilege, security)
- EC2 - virtual servers in the cloud
- S3 - object/file storage service
- Free tier limits (750 hrs/month for t2/t3.micro instances)
- Security groups - firewall rules controlling access to EC2 instances

## Steps completed

### 1. IAM User Setup
- Created IAM user: `sudhars-dev`
- Permissions attached: AmazonEC2FullAccess, AmazonS3FullAccess, IAMReadOnlyAccess
- Reason: Root account has unlimited access: IAM user limits risk if credentials are ever compromised
- Logged in via account sign-in URL instead of using root for daily work

### 2. EC2 Instance Launched
- Name: task-api-server
- AMI: Ubuntu (free tier eligible)
- Instance type: t3.micro (free tier eligible)
- Region: Asia Pacific (Sydney) - ap-southeast-2
- Key pair created: task-api-key.pem (saved locally, not committed to GitHub)
- Security group rules: SSH (22), HTTP (80), HTTPS (443) allowed
- Instance stopped after testing (to avoid unnecessary free-tier hour usage)

### 3. S3 Bucket Created
- Bucket name: sudhars-intern-training-day22
- Region: ap-southeast-2 (same as EC2, for consistency)
- Block Public Access: enabled (default, secure)
- ACLs: disabled (recommended, access via policies only)
- Versioning: disabled (not needed for this test)
- Uploaded 1 test file successfully (6.2 KB, PDF)

## Key concept
- Root account = master key (unlimited access, high risk if compromised)
- IAM user = limited keycard (only what's needed for the job)
- EC2 = rented virtual server
- S3 = cloud file storage (bucket = container, object = file)
- Free tier = 750 hrs/month free for small instances, first 12 months

## Note
No passwords, keys, or .pem files are stored in this repo - kept locally only.