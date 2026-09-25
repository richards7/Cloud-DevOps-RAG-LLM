# Microsoft Azure

## Core compute
- **Virtual Machines**: Azure's equivalent of EC2. VM sizes (B, D, F series) map to
  general purpose, compute-optimized, etc.
- **App Service**: PaaS for hosting web apps without managing VMs (like a mix of Cloud
  Run and Elastic Beanstalk).
- **Azure Functions**: serverless compute, event-triggered, similar to AWS Lambda.
- **AKS (Azure Kubernetes Service)**: managed Kubernetes.

## Storage
- **Blob Storage**: object storage (Azure's S3 equivalent). Tiers: Hot, Cool, Archive.
- **Managed Disks**: block storage for VMs (like EBS).
- **Azure Files**: managed file shares over SMB/NFS.

## Databases
- **Azure SQL Database**: managed SQL Server.
- **Cosmos DB**: globally distributed, multi-model NoSQL database.

## Networking
- **VNet**: Azure's virtual network (equivalent to AWS VPC).
- **NSG (Network Security Group)**: firewall rules at subnet/NIC level.
- **Azure Load Balancer** (layer 4) and **Application Gateway** (layer 7, with WAF).

## Identity
- **Azure AD (Entra ID)**: identity and access management, integrates with
  organizational accounts — a key difference from AWS IAM, which is account-scoped.
- **RBAC**: role-based access control assigns roles to users/groups/service principals
  at a scope (subscription, resource group, or resource).

## Resource organization
- **Resource Groups**: logical containers for related resources — everything in Azure
  belongs to one, unlike AWS's flatter account structure.
- **Subscriptions**: billing and access boundary, roughly analogous to an AWS account.

## CLI basics
```bash
az login
az group create --name myRG --location eastus
az vm create --resource-group myRG --name myVM --image UbuntuLTS
az webapp list
az aks get-credentials --resource-group myRG --name myAKSCluster
```

## Common errors & fixes
- **"AuthorizationFailed"**: the signed-in identity lacks an RBAC role at the required
  scope — check role assignments with `az role assignment list`.
- **VM not accessible**: check the NSG allows the port/source, and confirm a Public IP
  is attached if needed.
- **Deployment stuck "Accepted"**: often a quota limit in that region — check
  `az vm list-usage --location <region>`.
- **"ResourceGroupNotFound"**: resource group name or subscription context is wrong —
  verify with `az account show` and `az group list`.
