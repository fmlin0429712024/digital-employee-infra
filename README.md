# Turtle 🐢 - Digital Employee

> *"Slow and steady wins the race"*

24/7 AI-powered assistant running on GCP with OpenClaw.

---

## Quick Navigation

| File | What's Inside |
|------|---------------|
| **[setup/quickstart.md](setup/quickstart.md)** | Deploy & manage commands |
| **[setup/commands.md](setup/commands.md)** | Daily command cheatsheet |
| **[security/best-practices.md](security/best-practices.md)** | Security & backups |
| **[security/credentials.md](security/credentials.md)** | Where keys are stored |
| **[optimization/cost-savings.md](optimization/cost-savings.md)** | 33% cost reduction |
| **[architecture/system-overview.md](architecture/system-overview.md)** | Current system design |
| **[architecture/model-strategy.md](architecture/model-strategy.md)** | Fallback chain |
| **[skills/overview.md](skills/overview.md)** | **SKILLS system (core automation)** |
| **[skills/current-skills.md](skills/current-skills.md)** | **Active SKILLS inventory** |

---

## Current Status (Feb 2026)

✅ **Running**: openclaw-desktop (n2-standard-4, us-central1-a)  
✅ **Model**: gemini-2.0-flash (optimized for cost)  
✅ **Channels**: Telegram, WhatsApp, Voice  
✅ **Savings**: 33% reduction on Vertex AI costs

---

## Quick Start

### Connect to VM
```bash
gcloud compute ssh openclaw-desktop \
  --zone=us-central1-a \
  --project=linkhealth-care-2024 \
  --tunnel-through-iap
```

### Check Status
```bash
systemctl --user status openclaw-gateway
openclaw models status
```

### View Logs
```bash
journalctl --user -u openclaw-gateway -f
```

---

## Key Resources

| Resource | Location |
|----------|----------|
| **GCP Console** | https://console.cloud.google.com/ |
| **Project** | linkhealth-care-2024 |
| **VM** | openclaw-desktop (us-central1-a) |
| **Gateway Port** | 127.0.0.1:18789 |

---

## Philosophy

Building reliable AI infrastructure through:
- 🐢 **Stability** over velocity
- 🐢 **Reliability** over features
- 🐢 **Cost-efficiency** over power
- 🐢 **Documentation** over memory

Each iteration adds another layer, another backup, another safeguard.

---

## Learn More

Start with **[setup/quickstart.md](setup/quickstart.md)** for deployment guide.
