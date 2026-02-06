# 12 - GPU VM Provisioning Guide

This document provides step-by-step instructions for provisioning a GPU-enabled GCP VM for local LLM inference.

---

## Overview

This guide will help you create a **production-ready GPU VM** for running local language models with vLLM. This is separate from your main `openclaw-desktop` VM and dedicated to GPU workloads.

| Aspect | Details |
|--------|---------|
| **Purpose** | GPU-accelerated LLM inference (vLLM + DeepSeek R1) |
| **Recommended GPU** | NVIDIA L4 (24GB VRAM) |
| **Recommended Disk** | 500GB SSD (for model weights) |
| **OS** | Ubuntu 22.04 LTS with NVIDIA drivers |
| **Cost** | ~$360-400/month (24/7) or ~$0.50/hour (on-demand) |

---

## Prerequisites

Before starting, ensure you have:

- ✅ GCP account with billing enabled
- ✅ GCP credits or budget allocated (~$400/month)
- ✅ `gcloud` CLI installed and configured
- ✅ Basic familiarity with terminal/SSH
- ✅ Project ID (e.g., `linkhealth-care-2024`)

---

## Step 1: Check GPU Quota

GPU resources require quota approval in GCP.

### Check Current Quota

```bash
gcloud compute project-info describe --project=YOUR_PROJECT_ID \
  | grep -A 5 "NVIDIA_L4"
```

### Request Quota Increase (if needed)

1. Go to: https://console.cloud.google.com/iam-admin/quotas
2. Search for: `NVIDIA L4 GPUs`
3. Select your region (e.g., `us-central1`)
4. Click "EDIT QUOTAS"
5. Request at least **1 GPU**
6. Wait for approval (usually 1-2 business days)

**Tip**: Start with `us-central1` - it has good GPU availability and pricing.

---

## Step 2: Create GPU VM

### Option A: Using gcloud CLI (Recommended)

```bash
# Set variables
PROJECT_ID="linkhealth-care-2024"
VM_NAME="gpu-llm-01"
ZONE="us-central1-a"
GPU_TYPE="nvidia-l4"
GPU_COUNT=1
MACHINE_TYPE="g2-standard-4"  # 4 vCPU, 16GB RAM, optimized for L4
DISK_SIZE="500GB"

# Create VM with GPU
gcloud compute instances create $VM_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --accelerator=type=$GPU_TYPE,count=$GPU_COUNT \
    --maintenance-policy=TERMINATE \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=$DISK_SIZE \
    --boot-disk-type=pd-ssd \
    --scopes=cloud-platform \
    --metadata=install-nvidia-driver=True
```

**Important Flags**:
- `--maintenance-policy=TERMINATE` - Required for GPU VMs (can't live migrate)
- `--metadata=install-nvidia-driver=True` - Auto-installs NVIDIA drivers
- `--scopes=cloud-platform` - Full GCP API access

### Option B: Using GCP Console

1. Go to: https://console.cloud.google.com/compute/instances
2. Click **"CREATE INSTANCE"**
3. Configure:
   - **Name**: `gpu-llm-01`
   - **Region**: `us-central1`
   - **Zone**: `us-central1-a`
   - **Machine type**: `g2-standard-4` (under GPU section)
   - **GPU**: NVIDIA L4 x 1
   - **Boot disk**: Ubuntu 22.04 LTS, 500GB SSD
   - **Firewall**: Allow HTTP/HTTPS traffic (optional)
4. Click **"CREATE"**

---

## Step 3: Initial VM Setup

### Connect to VM

```bash
gcloud compute ssh gpu-llm-01 \
    --zone=us-central1-a \
    --project=linkhealth-care-2024 \
    --tunnel-through-iap
```

**Pro tip**: Add an alias to `~/.bashrc`:
```bash
alias gpu-ssh='gcloud compute ssh gpu-llm-01 --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap'
```

### Verify GPU Installation

```bash
# Check NVIDIA driver
nvidia-smi

# Expected output:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.2    |
# |-------------------------------+----------------------+----------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  NVIDIA L4           Off  | 00000000:00:03.0 Off |                    0 |
# | N/A   38C    P8    15W /  72W |      0MiB / 23034MiB |      0%      Default |
# +-------------------------------+----------------------+----------------------+
```

If `nvidia-smi` doesn't work, see [Troubleshooting](#troubleshooting) section.

---

## Step 4: Install Docker & NVIDIA Container Toolkit

### Install Docker

```bash
# Update package list
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group (no sudo needed)
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify Docker installation
docker --version
docker compose version
```

### Install NVIDIA Container Toolkit

```bash
# Add NVIDIA Container Toolkit repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker
sudo systemctl restart docker

# Verify GPU access from Docker
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

**Expected output**: Should show the same GPU info as the host `nvidia-smi`.

---

## Step 5: Deploy LLM Stack

### Clone Repository

```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone the digital employee infrastructure repo
git clone https://github.com/fmlin0429712024/digital-employee-infra.git
cd digital-employee-infra/LLM-Local-Deployment
```

### Deploy vLLM + Open WebUI

```bash
# Make scripts executable
chmod +x setup.sh validate.sh setup-cloudflare.sh

# Run deployment
./setup.sh
```

**What this does**:
1. Generates secure API key
2. Creates `.env` file
3. Pulls Docker images (vLLM + Open WebUI)
4. Starts services
5. Downloads DeepSeek R1 model (~15GB)

**Expected output**:
```
✅ vLLM service started
✅ Open WebUI started
✅ Services are healthy

Access Open WebUI at: http://localhost:3000
API endpoint: http://localhost:8000/v1
```

### Verify Deployment

```bash
# Run validation script
./validate.sh

# Check running containers
docker ps

# Check GPU usage
nvidia-smi

# View logs
docker logs vllm-service
docker logs open-webui
```

---

## Step 6: Access Methods

### Option A: SSH Tunnel (Secure, Recommended)

From your **local machine**:

```bash
# Create SSH tunnel for Open WebUI
gcloud compute ssh gpu-llm-01 \
    --project=linkhealth-care-2024 \
    --zone=us-central1-a \
    --tunnel-through-iap \
    -- -L 3000:localhost:3000 -N
```

Then open in browser: http://localhost:3000

### Option B: Cloudflare Tunnel (Public HTTPS)

On the **GPU VM**:

```bash
cd ~/projects/digital-employee-infra/LLM-Local-Deployment
./setup-cloudflare.sh
```

This creates a free public HTTPS URL (e.g., `https://random-name.trycloudflare.com`)

**Note**: URL changes on restart. For permanent URL, use paid Cloudflare account.

### Option C: Direct IP (Not Recommended)

Only use for testing. Requires firewall rule:

```bash
# Open port 3000 (temporary)
gcloud compute firewall-rules create allow-webui \
    --project=linkhealth-care-2024 \
    --allow=tcp:3000 \
    --source-ranges=YOUR_IP_ADDRESS/32 \
    --target-tags=gpu-llm

# Tag the VM
gcloud compute instances add-tags gpu-llm-01 \
    --zone=us-central1-a \
    --tags=gpu-llm
```

Then access: `http://EXTERNAL_IP:3000`

---

## Step 7: First-Time Setup

### Create Admin Account

1. Open Open WebUI (via SSH tunnel or Cloudflare)
2. Click **"Sign up"**
3. Create account (first user becomes admin)
4. **Important**: Disable public signups
   - Go to **Admin Panel** → **Settings** → **General**
   - Toggle off **"Enable Signup"**

### Configure Model

1. Go to **Settings** → **Models**
2. Verify model is available: `deepseek-ai/DeepSeek-R1-Distill-Llama-8B`
3. Test with a simple prompt

---

## Cost Management

### Pricing Breakdown (us-central1)

| Component | Cost |
|-----------|------|
| **g2-standard-4 VM** | ~$0.35/hour |
| **NVIDIA L4 GPU** | ~$0.50/hour |
| **500GB SSD** | ~$85/month |
| **Network Egress** | ~$0.12/GB |
| **Total (24/7)** | **~$360-400/month** |

### Cost Optimization Strategies

#### 1. Stop VM When Not in Use

```bash
# Stop VM (keeps disk, no compute charges)
gcloud compute instances stop gpu-llm-01 --zone=us-central1-a

# Start VM
gcloud compute instances start gpu-llm-01 --zone=us-central1-a
```

**Savings**: Only pay for storage (~$85/month) when stopped.

#### 2. Use Preemptible/Spot VMs

Add `--preemptible` or `--provisioning-model=SPOT` to creation command.

**Savings**: ~70% discount, but VM can be terminated anytime.

#### 3. Schedule Auto-Shutdown

```bash
# Create shutdown script
cat > ~/auto-shutdown.sh << 'EOF'
#!/bin/bash
# Shutdown VM at 6 PM daily
sudo shutdown -h now
EOF

chmod +x ~/auto-shutdown.sh

# Add to crontab
crontab -e
# Add line: 0 18 * * * /home/YOUR_USERNAME/auto-shutdown.sh
```

#### 4. Use Committed Use Discounts

For 1-year or 3-year commitments, get up to 57% discount.

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check GPU utilization
nvidia-smi

# Check Docker containers
docker ps

# Check disk space
df -h

# Check memory
free -h

# View vLLM logs
docker logs vllm-service --tail 100 -f
```

### Auto-Restart on Reboot

```bash
# Docker containers auto-restart by default (restart: unless-stopped)
# Verify in docker-compose.yml

# To manually restart after VM reboot
cd ~/projects/digital-employee-infra/LLM-Local-Deployment
docker compose up -d
```

### Backup Important Data

```bash
# Backup Open WebUI data (user accounts, chat history)
docker run --rm -v open-webui-data:/data -v $(pwd):/backup \
    ubuntu tar czf /backup/open-webui-backup.tar.gz /data

# Backup to GCS
gsutil cp open-webui-backup.tar.gz gs://YOUR_BUCKET/backups/
```

---

## Troubleshooting

### GPU Not Detected

**Issue**: `nvidia-smi` command not found or shows no GPU.

**Solution**:
```bash
# Check if driver installation is pending
sudo journalctl -u google-startup-scripts.service

# Manually install NVIDIA driver
sudo apt-get update
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall
sudo reboot

# After reboot, verify
nvidia-smi
```

### Docker Can't Access GPU

**Issue**: `docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]]`

**Solution**:
```bash
# Reinstall NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test again
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

### Model Download Fails

**Issue**: vLLM can't download model from Hugging Face.

**Solution**:
```bash
# Check disk space
df -h

# If disk full, resize boot disk
gcloud compute disks resize gpu-llm-01 \
    --size=1000GB \
    --zone=us-central1-a

# Then resize filesystem
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1

# Restart vLLM
cd ~/projects/digital-employee-infra/LLM-Local-Deployment
docker compose restart vllm-service
```

### Out of Memory (OOM)

**Issue**: vLLM crashes with CUDA out of memory error.

**Solution**:
```bash
# Reduce GPU memory utilization in docker-compose.yml
# Change: --gpu-memory-utilization 0.90
# To:     --gpu-memory-utilization 0.80

# Restart
docker compose restart vllm-service
```

### Can't Access Open WebUI

**Issue**: Connection refused or timeout.

**Solution**:
```bash
# Check if containers are running
docker ps

# Check logs
docker logs open-webui

# Verify ports
sudo netstat -tulpn | grep -E '3000|8000'

# Restart services
docker compose restart
```

---

## Security Best Practices

### 1. Restrict SSH Access

```bash
# Only allow IAP tunnel (already configured)
# Verify firewall rules
gcloud compute firewall-rules list --project=linkhealth-care-2024
```

### 2. Disable Public Signups

In Open WebUI Admin Panel → Settings → Disable "Enable Signup"

### 3. Use Strong API Keys

```bash
# Regenerate API key if compromised
openssl rand -hex 32 > .env
sed -i 's/VLLM_API_KEY=.*/VLLM_API_KEY='$(cat .env)'/' .env
docker compose restart vllm-service
```

### 4. Enable Firewall

```bash
# Enable UFW (Ubuntu Firewall)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

### 5. Regular Updates

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Docker images
cd ~/projects/digital-employee-infra/LLM-Local-Deployment
docker compose pull
docker compose up -d
```

---

## Integration with OpenClaw/OpenCode

### Configure OpenCode to Use Local vLLM

On your **openclaw-desktop** VM:

```bash
# Edit OpenCode config
nano ~/.config/opencode/opencode.json
```

Add:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openai/deepseek-r1-distill-llama-8b",
  "baseURL": "http://GPU_VM_INTERNAL_IP:8000/v1",
  "apiKey": "YOUR_VLLM_API_KEY"
}
```

**Get Internal IP**:
```bash
gcloud compute instances describe gpu-llm-01 \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].networkIP)'
```

---

## Next Steps

1. ✅ **Test the deployment** - Create a test chat in Open WebUI
2. ✅ **Set up monitoring** - Configure alerts for GPU usage
3. ✅ **Integrate with OpenCode** - Configure local model for coding tasks
4. ✅ **Fine-tune model** - Prepare domain-specific training data
5. ✅ **Implement backups** - Schedule regular data backups to GCS

---

## Related Documentation

- [02 - Infrastructure Setup](02-infrastructure.md) - Main OpenClaw VM setup
- [11 - Local LLM Deployment](11-local-llm-deployment.md) - Architecture overview
- [10 - Agent Framework Vision](10-agent-framework-vision.md) - Future integration plans
- [LLM-Local-Deployment/README.md](../LLM-Local-Deployment/README.md) - Deployment scripts

---

## Quick Reference

### Common Commands

```bash
# Connect to GPU VM
gcloud compute ssh gpu-llm-01 --zone=us-central1-a --tunnel-through-iap

# Check GPU
nvidia-smi

# Check containers
docker ps

# View logs
docker logs vllm-service -f

# Restart services
cd ~/projects/digital-employee-infra/LLM-Local-Deployment
docker compose restart

# Stop VM (save costs)
gcloud compute instances stop gpu-llm-01 --zone=us-central1-a

# Start VM
gcloud compute instances start gpu-llm-01 --zone=us-central1-a
```

---

## Navigation

- Previous: [11-local-llm-deployment.md](11-local-llm-deployment.md)
- Related: [02-infrastructure.md](02-infrastructure.md)
- Start: [01-overview.md](01-overview.md)
