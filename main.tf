terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = "us-east-1"

  #IMPORTANTE para Learner Lab - ignorar tags requeridos
  default_tags {
    tags = {
      Project = "docker-aws-automation"
      Environment = "learner-lab"
    }
  }

  skip_credentials_validation = true
  skip_metadata_api_check     = true
}


# Variables
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
  default     = "docker-automation-key"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
  default     = "docker-aws-automation"
}

variable "git_repository_url" {
  description = "Git repository URL to clone (leave empty to skip)"
  type        = string
  default     = "https://github.com/miguelRamirezr1/docker-aws-automation.git"
}

# Data sources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

data "aws_vpc" "default" {
  default = true
}

# Security Group
resource "aws_security_group" "docker_services" {
  name        = "${var.project_name}-security-group"
  description = "Security group for Docker services on EC2"
  vpc_id      = data.aws_vpc.default.id

  # SSH
  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Orion Context Broker
  ingress {
    description = "Orion-LD API"
    from_port   = 1026
    to_port     = 1026
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # QuantumLeap
  ingress {
    description = "QuantumLeap API"
    from_port   = 8668
    to_port     = 8668
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # MongoDB
  ingress {
    description = "MongoDB"
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # CrateDB Admin UI
  ingress {
    description = "CrateDB Admin UI"
    from_port   = 4200
    to_port     = 4200
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # CrateDB PostgreSQL
  ingress {
    description = "CrateDB PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # CrateDB Transport
  ingress {
    description = "CrateDB Transport"
    from_port   = 4300
    to_port     = 4300
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Grafana
  ingress {
    description = "Grafana"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Frontend (Streamlit)
  ingress {
    description = "Frontend Streamlit"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress rules - Allow all outbound traffic
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description      = "Allow all outbound IPv6 traffic"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name        = "${var.project_name}-security-group"
    Project     = var.project_name
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# EC2 Instance
resource "aws_instance" "docker_host" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.docker_services.id]

  # Root block device configuration
  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true
  }

  # User data script to install Docker and Docker Compose
  user_data = <<-EOF
              #!/bin/bash
              set -e

              # Log function
              log() {
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/user-data.log
              }

              log "Starting user_data script..."

              # Update system
              log "Updating system packages..."
              apt-get update
              apt-get upgrade -y

              # Install dependencies
              log "Installing dependencies..."
              apt-get install -y \
                apt-transport-https \
                ca-certificates \
                curl \
                gnupg \
                lsb-release \
                git \
                unzip

              # Install Docker
              log "Installing Docker..."
              curl -fsSL https://get.docker.com -o get-docker.sh
              sh get-docker.sh
              rm get-docker.sh

              # Add ubuntu user to docker group
              log "Adding ubuntu user to docker group..."
              usermod -aG docker ubuntu

              # Install Docker Compose
              log "Installing Docker Compose..."
              DOCKER_COMPOSE_VERSION="v2.24.0"
              curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

              # Enable and start Docker
              log "Starting Docker service..."
              systemctl enable docker
              systemctl start docker

              # Wait for Docker to be ready
              log "Waiting for Docker to be ready..."
              sleep 5

              # Create application directory
              log "Creating application directory..."
              mkdir -p /home/ubuntu/app
              cd /home/ubuntu/app

              # Clone repository if URL is provided
              GIT_REPO_URL="${var.git_repository_url}"
              if [ -n "$GIT_REPO_URL" ]; then
                log "Cloning repository: $GIT_REPO_URL"
                git clone "$GIT_REPO_URL" /home/ubuntu/app || {
                  log "ERROR: Failed to clone repository"
                  log "Please manually clone: git clone $GIT_REPO_URL /home/ubuntu/app"
                }
              else
                log "No repository URL provided. Please manually clone your repository to /home/ubuntu/app"
              fi

              # Set ownership
              chown -R ubuntu:ubuntu /home/ubuntu/app

              #give time to clone the repository
              sleep 10

              # Create enhanced startup script
              log "Creating start-services.sh script..."
              cat > /home/ubuntu/start-services.sh <<'SCRIPT'
              #!/bin/bash
              set -e

              echo "=== Docker Services Management Script ==="
              echo "Started at: $(date)"
              echo ""

              # Navigate to app directory
              cd /home/ubuntu/app

              # Check if docker-compose.yml exists
              if [ ! -f "docker-compose.yml" ]; then
                echo "ERROR: docker-compose.yml not found in /home/ubuntu/app"
                echo "Please clone your repository first:"
                echo "  cd /home/ubuntu/app"
                echo "  git clone <your-repo-url> ."
                exit 1
              fi

              # Stop existing containers
              echo "Stopping existing containers..."
              docker-compose down || true

              # Pull latest images
              echo "Pulling latest Docker images..."
              docker-compose pull || true

              # Build custom images (like frontend)
              echo "Building custom images..."
              docker-compose build || true

              # Start services
              echo "Starting services..."
              docker-compose up -d

              # Show status
              echo ""
              echo "Services status:"
              docker-compose ps

              echo ""
              echo "=== Services started successfully! ==="
              echo "Finished at: $(date)"
              SCRIPT

              chmod +x /home/ubuntu/start-services.sh
              chown ubuntu:ubuntu /home/ubuntu/start-services.sh

              # Create stop-services.sh script
              log "Creating stop-services.sh script..."
              cat > /home/ubuntu/stop-services.sh <<'SCRIPT'
              #!/bin/bash
              set -e

              echo "=== Stopping Docker Services ==="
              cd /home/ubuntu/app

              if [ -f "docker-compose.yml" ]; then
                docker-compose down
                echo "Services stopped successfully!"
              else
                echo "ERROR: docker-compose.yml not found"
                exit 1
              fi
              SCRIPT

              chmod +x /home/ubuntu/stop-services.sh
              chown ubuntu:ubuntu /home/ubuntu/stop-services.sh

              # If repository was cloned and docker-compose.yml exists, start services
              if [ -f "/home/ubuntu/app/docker-compose.yml" ]; then
                log "docker-compose.yml found. Starting services..."

                # Pull and build images
                cd /home/ubuntu/app
                log "Pulling Docker images..."
                docker-compose pull || log "WARNING: Some images could not be pulled"

                log "Building custom images..."
                docker-compose build || log "WARNING: Build failed"

                log "Starting Docker Compose services..."
                docker-compose up -d || log "ERROR: Failed to start services"

                # Wait a bit and show status
                sleep 10
                log "Services status:"
                docker-compose ps | tee -a /var/log/user-data.log
              else
                log "docker-compose.yml not found. Services not started automatically."
                log "After cloning your repository, run: /home/ubuntu/start-services.sh"
              fi

              # Create status check script
              cat > /home/ubuntu/check-services.sh <<'SCRIPT'
              #!/bin/bash
              cd /home/ubuntu/app
              echo "=== Docker Services Status ==="
              docker-compose ps
              echo ""
              echo "=== Docker Images ==="
              docker images
              echo ""
              echo "=== System Resources ==="
              docker stats --no-stream
              SCRIPT

              chmod +x /home/ubuntu/check-services.sh
              chown ubuntu:ubuntu /home/ubuntu/check-services.sh

              log "User data script completed successfully!"
              log "Docker version: $(docker --version)"
              log "Docker Compose version: $(docker-compose --version)"
              EOF

  # Enable detailed monitoring
  monitoring = true

  # Instance metadata options
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
    instance_metadata_tags      = "enabled"
  }

  # Tags
  tags = {
    Name        = "${var.project_name}-instance"
    Project     = var.project_name
    Environment = "production"
    ManagedBy   = "terraform"
    Application = "docker-services"
    OS          = "Ubuntu 22.04"
  }

  # Volume tags
  volume_tags = {
    Name        = "${var.project_name}-volume"
    Project     = var.project_name
    Environment = "production"
  }

  # Lifecycle
  lifecycle {
    ignore_changes = [ami]
  }
}

# Elastic IP
resource "aws_eip" "docker_host" {
  instance = aws_instance.docker_host.id
  domain   = "vpc"

  tags = {
    Name        = "${var.project_name}-eip"
    Project     = var.project_name
    Environment = "production"
    ManagedBy   = "terraform"
  }

  depends_on = [aws_instance.docker_host]
}

# Outputs
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.docker_host.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.docker_host.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.docker_host.public_dns
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.docker_services.id
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_eip.docker_host.public_ip}"
}

output "service_urls" {
  description = "URLs for accessing the services"
  value = {
    orion       = "http://${aws_eip.docker_host.public_ip}:1026"
    quantumleap = "http://${aws_eip.docker_host.public_ip}:8668"
    crate_ui    = "http://${aws_eip.docker_host.public_ip}:4200"
    grafana     = "http://${aws_eip.docker_host.public_ip}:3000"
    frontend    = "http://${aws_eip.docker_host.public_ip}:8501"
  }
}
