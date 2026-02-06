# 02 - Infrastructure Setup

## Overview

The Digital Employee runs on a GCP Compute Engine VM with the OpenClaw agent framework.

---

## GCP Compute Engine

### VM Specifications

| Attribute | Value |
|-----------|-------|
| **Instance** | openclaw-desktop |
| **Type** | n2-standard-4 (4 vCPU, 16GB RAM) |
| **Region** | us-central1-a |
| **Project** | linkhealth-care-2024 |
| **OS** | Ubuntu 22.04 LTS |
| **Disk** | 100GB SSD |
| **Credits** | $18,000 startup credits |

### Create VM (New Setup)

```bash
gcloud compute instances create openclaw-desktop \
    --zone=us-central1-a \
    --machine-type=n2-standard-4 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=100GB \
    --scopes=cloud-platform
```

### VM Access Methods

The VM is secured with IAP-only SSH access. Direct SSH from the internet is blocked.

#### Option 1: Local Terminal (Recommended)

```bash
# SSH via IAP tunnel
gcloud compute ssh openclaw-desktop \
    --zone=us-central1-a \
    --project=linkhealth-care-2024 \
    --tunnel-through-iap
```

**Pro tip:** Add an alias to `~/.bashrc` or `~/.zshrc`:
```bash
alias openclaw-ssh='gcloud compute ssh openclaw-desktop --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap'
```

#### Option 2: GCP Cloud Shell

1. Open GCP Console: https://console.cloud.google.com
2. Click the `>_` Cloud Shell icon (top-right)
3. Run:
   ```bash
   gcloud compute ssh openclaw-desktop --zone=us-central1-a --tunnel-through-iap
   ```

#### Option 3: Chrome Remote Desktop (GUI)

For graphical desktop access (OAuth flows, debugging, etc.):

1. Go to: https://remotedesktop.google.com/access
2. Select "openclaw-desktop"
3. Enter PIN when prompted

**Note:** CRD uses outbound HTTPS, no firewall rules needed.

#### What Doesn't Work

| Method | Status | Reason |
|--------|--------|--------|
| GCP Console "SSH" button | ❌ Blocked | Uses direct SSH to external IP |
| Direct SSH to 34.66.121.98 | ❌ Blocked | Firewall only allows IAP range |
| RDP (port 3389) | ❌ Deleted | Rule removed for security |

---

## Security Configuration

### Firewall Rules

| Rule | Ports | Source | Purpose |
|------|-------|--------|---------|
| allow-ssh-iap | 22 | 35.235.240.0/20 | SSH via IAP only |
| allow-openclaw-access | 80, 443 | 0.0.0.0/0 | Web access (if needed) |
| default-allow-internal | all | 10.128.0.0/9 | GCP internal traffic |

### Brute Force Protection

The VM runs fail2ban to block repeated failed SSH attempts:

```bash
# Check fail2ban status
sudo fail2ban-client status sshd

# View banned IPs
sudo fail2ban-client status sshd | grep "Banned IP"
```

### Credential Security

All sensitive files have restricted permissions (600/700):

```bash
# Verify permissions
ls -la ~/.openclaw/keys/
```

---

## Environment Setup

### Node.js

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### npm Global Path

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
echo 'export NODE_PATH="$HOME/.npm-global/lib/node_modules"' >> ~/.bashrc
source ~/.bashrc
```

### Python Path

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## GitHub Access

### Generate SSH Key

```bash
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""
chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub  # Copy this to GitHub
```

### Add Key to GitHub

```bash
# From local machine with gh CLI
gh ssh-key add - --title "openclaw-desktop-gcp" <<< "YOUR_PUBLIC_KEY"
```

### Configure Git

```bash
git config --global user.name "your-username"
git config --global user.email "your-email@example.com"
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts
```

---

## OpenClaw Gateway

### Overview

| Attribute | Value |
|-----------|-------|
| **Port** | 18789 |
| **Bind** | 127.0.0.1 (loopback) |
| **Auth** | Token-based |

### Gateway Commands

```bash
openclaw gateway status    # Check health
openclaw gateway restart   # Restart gateway
openclaw models status     # Model configuration
```

### Systemd Service

```bash
# Check status
systemctl --user status openclaw-gateway

# Restart
systemctl --user restart openclaw-gateway

# Enable auto-start
systemctl --user enable openclaw-gateway
```

**Critical**: Enable user linger for 24/7 operation:

```bash
loginctl enable-linger $(whoami)
```

---

## Key Files

| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main configuration |
| `~/.openclaw/keys/vertex-auth.json` | Vertex AI service account |
| `~/.openclaw/keys/oauth-credentials.json` | Google OAuth credentials |
| `~/.openclaw/keys/gmail-token.pickle` | Gmail API token |
| `~/.openclaw/keys/calendar-token.pickle` | Calendar API token |
| `~/.openclaw/data/memory.db` | SQLite memory database |
| `~/.openclaw/scripts/` | Helper scripts |
| `~/.config/systemd/user/openclaw-gateway.service` | Systemd service |
| `/tmp/openclaw/openclaw-*.log` | Daily logs |

---

## Environment Variables

Located in `~/.config/systemd/user/openclaw-gateway.service.d/vertex.conf`:

```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/USER/.openclaw/keys/vertex-auth.json"
Environment="GOOGLE_CLOUD_PROJECT=linkhealth-care-2024"
Environment="GOOGLE_CLOUD_LOCATION=us-central1"
Environment="TELEGRAM_BOT_TOKEN=<token>"
```

After changes:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

---

## Navigation

- Previous: [01-overview.md](01-overview.md)
- Next: [03-ai-providers.md](03-ai-providers.md)
