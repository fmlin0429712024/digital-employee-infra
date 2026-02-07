# Setup Guide

## Quick Start

### 1. Connect to VM
```bash
gcloud compute ssh openclaw-desktop \
  --zone=us-central1-a \
  --project=linkhealth-care-2024 \
  --tunnel-through-iap
```

### 2. Check Status
```bash
# Gateway
systemctl --user status openclaw-gateway

# Models
openclaw models status

# Current model
journalctl --user -u openclaw-gateway -n 20 | grep "agent model"
```

### 3. Restart Gateway
```bash
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway
```

---

## Initial Setup (One-Time)

### Create VM
```bash
gcloud compute instances create openclaw-desktop \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=100GB \
  --scopes=cloud-platform
```

### Install OpenClaw
```bash
# Node.js
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# OpenClaw
npm i -g openclaw@latest

# Configure
openclaw configure
```

### Grant Vertex AI Access
```bash
# Get VM service account
gcloud compute instances describe openclaw-desktop \
  --zone=us-central1-a \
  --format="get(serviceAccounts[0].email)"

# Grant role
gcloud projects add-iam-policy-binding linkhealth-care-2024 \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/aiplatform.user"
```

---

## Key Locations

| Resource | Path |
|----------|------|
| Config | `~/.openclaw/openclaw.json` |
| Keys | `~/.openclaw/keys/` |
| Logs | `/tmp/openclaw/openclaw-*.log` |
| Workspace | `~/.openclaw/workspace/` |

---

## Troubleshooting

### Gateway Won't Start
```bash
# Check logs
journalctl --user -u openclaw-gateway -n 50

# Validate config
cat ~/.openclaw/openclaw.json | jq '.'

# Restore backup
cp ~/.openclaw/openclaw.json.backup.* ~/.openclaw/openclaw.json
```

### Check Resources
```bash
# RAM
free -h

# Disk
df -h

# CPU
nproc
```
