# VM Cheat Sheet

## 🚀 Connect
**1. Terminal Access:**
```bash
gcloud compute ssh openclaw-desktop --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

**2. Get Gateway Token:**
Run on VM to get your token:
```bash
cat ~/.openclaw/openclaw.json | grep "token"
```

**3. Web UI (Control Dashboard) Access:**
Run this locally to forward port 18789:
```bash
gcloud compute ssh openclaw-desktop --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap --ssh-flag="-L 18789:localhost:18789 -N"
```
*Then open in browser:* `http://localhost:18789/`

**4. Authenticate:**
- Paste your Gateway Token in the "Gateway Token" field
- Click **Connect**

---

## ⚙️ Setup Commands
| Command | Usage |
|---------|-------|
| `openclaw configure` | **Local Setup**: Interactively creates `openclaw.json` with API keys, model preferences, and paths. **Run this first.** |
| `openclaw onboard` | **Server Registration**: Connects/Registers the agent with the central control plane. **Run this to link to the server.** |

---

## 🔍 Status Checks
**Run these on the VM:**

### Gateway Status
```bash
systemctl --user status openclaw-gateway
```

### Model Status
```bash
openclaw models status
```

### View Logs (Live)
```bash
journalctl --user -u openclaw-gateway -f
```

---

## 📂 Key Locations
| Item | Path |
|------|------|
| **Config** | `~/.openclaw/openclaw.json` |
| **Logs** | `/tmp/openclaw/openclaw-*.log` |
| **Workspace**| `~/.openclaw/workspace/` |

---

## 🛠️ Troubleshooting
**Restart Gateway:**
```bash
systemctl --user restart openclaw-gateway
```

**Check Resources:**
```bash
free -h  # RAM
df -h    # Disk
```
