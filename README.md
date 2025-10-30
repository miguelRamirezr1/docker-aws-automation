# Docker AWS Automation

Automated deployment of several Docker services (Orion-LD, QuantumLeap, MongoDB, CrateDB, Grafana, and Streamlit Frontend) on AWS EC2 using Terraform.

## Architecture

This project deploys a complete IoT/Data platform with the following services:
- **Orion-LD**: FIWARE Context Broker for managing context information
- **QuantumLeap**: Time-series data storage for context data
- **MongoDB**: Database for Orion-LD
- **CrateDB**: Time-series database for QuantumLeap
- **Grafana**: Visualization and monitoring dashboard
- **Frontend**: Streamlit web application for user interface

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured with credentials
- Terraform >= 1.0
- SSH key pair created in AWS (default name: `docker-automation-key`)

## Project Structure

```
.
main.tf                 # Terraform configuration for AWS infrastructure
docker-compose.yml      # Docker Compose configuration for all services
frontend/               # Frontend application
	dockerfile         # Dockerfile for frontend
	requirements.txt   # Python dependencies
	src/              # Source code
		Home.py       # Main application entry
		pages/        # Additional pages
README.md             # This file
```

## Infrastructure Components

### AWS Resources Created:
- **EC2 Instance**: t3.medium Ubuntu 22.04 server
- **Security Group**: With ingress rules for all services
- **Elastic IP**: Static public IP address
- **VPC**: Uses default VPC

### Security Group Rules:
- Port 22: SSH
- Port 1026: Orion-LD API
- Port 8668: QuantumLeap API
- Port 27017: MongoDB
- Port 4200: CrateDB Admin UI
- Port 5432: CrateDB PostgreSQL
- Port 4300: CrateDB Transport
- Port 3000: Grafana
- Port 8501: Frontend (Streamlit)
- Port 80/443: HTTP/HTTPS

## Deployment Instructions

### 1. Configure Variables (Optional)

Edit `main.tf` to customize:
```hcl
variable "instance_type" {
  default = "t3.medium"  # Change instance size if needed
}

variable "key_name" {
  default = "docker-automation-key"  # Change to your SSH key name
}
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. Plan the Deployment

```bash
terraform plan
```

### 4. Deploy Infrastructure

```bash
terraform apply
```

Review the plan and type `yes` to confirm.

### 5. Get Connection Information

After deployment, Terraform will output:
- Instance ID
- Public IP address
- Public DNS name
- SSH command
- Service URLs

Example output:
```
instance_public_ip = "54.123.45.67"
ssh_command = "ssh -i docker-automation-key.pem ubuntu@54.123.45.67"
service_urls = {
  "orion" = "http://54.123.45.67:1026"
  "quantumleap" = "http://54.123.45.67:8668"
  "crate_ui" = "http://54.123.45.67:4200"
  "grafana" = "http://54.123.45.67:3000"
  "frontend" = "http://54.123.45.67:8501"
}
```

### 6. Connect to EC2 Instance

```bash
ssh -i your-key.pem ubuntu@<public-ip>
```

### 7. Deploy Docker Services

On the EC2 instance:

```bash
# Clone this repository
cd /home/ubuntu/app
git clone <your-repo-url> .

# Start all services
docker-compose up -d

# Or use the provided script
/home/ubuntu/start-services.sh
```

### 8. Verify Services

Check service status:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f
```

## Accessing Services

After deployment, access services at:
- **Frontend**: http://\<public-ip\>:8501
- **Grafana**: http://\<public-ip\>:3000 (default: admin/admin)
- **CrateDB UI**: http://\<public-ip\>:4200
- **Orion-LD**: http://\<public-ip\>:1026/version
- **QuantumLeap**: http://\<public-ip\>:8668/version

## Management Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### Restart services
```bash
docker-compose restart
```

### View logs
```bash
docker-compose logs -f [service-name]
```

### Update services
```bash
git pull
docker-compose down
docker-compose up -d --build
```

## Cleanup

To destroy all AWS resources:

```bash
terraform destroy
```

Type `yes` to confirm.

## Cost Estimation

- EC2 t3.medium: ~$0.0416/hour (~$30/month)
- EBS Storage (30GB): ~$3/month
- Data Transfer: Variable
- Elastic IP: Free while attached

**Estimated monthly cost**: $35-50 USD

## Troubleshooting

### Services not starting
```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check memory
free -h
```

### Cannot connect to instance
- Verify security group rules allow your IP
- Check SSH key permissions: `chmod 400 your-key.pem`
- Verify instance is running in AWS Console

### Docker issues
```bash
# Restart Docker daemon
sudo systemctl restart docker

# Check Docker status
sudo systemctl status docker
```

## Security Notes

- Change default passwords for Grafana
- Consider restricting security group rules to specific IP ranges
- Enable AWS CloudWatch monitoring for production
- Implement backup strategies for data volumes
- Use AWS Secrets Manager for sensitive credentials
