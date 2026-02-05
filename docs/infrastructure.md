# Infrastructure

## GCP Compute Engine

| Attribute | Value |
|-----------|-------|
| **Instance** | openclaw-desktop |
| **Type** | n2-standard-4 (4 vCPU, 16GB RAM) |
| **Region** | us-central1-a |
| **Project** | linkhealth-care-2024 |
| **Credits** | $18,000 startup credits |

## Connect to VM

```bash
gcloud compute ssh --zone "us-central1-a" "openclaw-desktop" --project "linkhealth-care-2024"
```

## OpenClaw Gateway

| Attribute | Value |
|-----------|-------|
| **Port** | 18789 |
| **Bind** | 127.0.0.1 (loopback) |
| **Auth** | Token-based |

### Gateway Commands

```bash
openclaw gateway status    # Check health
openclaw gateway restart   # Restart gateway
```

### Systemd Service

The gateway runs as a user systemd service:

```bash
systemctl --user status openclaw-gateway
systemctl --user restart openclaw-gateway
systemctl --user enable openclaw-gateway   # Auto-start on boot
```

**Critical**: User linger must be enabled for 24/7 operation:

```bash
loginctl enable-linger $(whoami)
```

### Key Files

| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main configuration |
| `~/.openclaw/keys/vertex-auth.json` | Vertex AI service account |
| `~/.config/systemd/user/openclaw-gateway.service` | Systemd service |
| `~/.config/systemd/user/openclaw-gateway.service.d/vertex.conf` | Environment overrides |
| `/tmp/openclaw/openclaw-*.log` | Daily logs |

### Environment Variables (systemd override)

Located in `~/.config/systemd/user/openclaw-gateway.service.d/vertex.conf`:

```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/.../vertex-auth.json"
Environment="GOOGLE_CLOUD_PROJECT=linkhealth-care-2024"
Environment="GOOGLE_CLOUD_LOCATION=us-central1"
Environment="TELEGRAM_BOT_TOKEN=<token>"
```
