# Command Cheatsheet

## Daily Operations

### Connect
```bash
gcloud compute ssh openclaw-desktop --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

### Status Checks
```bash
systemctl --user status openclaw-gateway
openclaw models status
openclaw gateway status
```

### Restart
```bash
systemctl --user restart openclaw-gateway
```

### View Logs
```bash
# Live logs
journalctl --user -u openclaw-gateway -f

# Last 50 lines
journalctl --user -u openclaw-gateway -n 50

# Today's log file
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

## Configuration

### Backup Config
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)
```

### Edit Config
```bash
nano ~/.openclaw/openclaw.json

# Validate JSON
cat ~/.openclaw/openclaw.json | jq '.'
```

### View Current Model
```bash
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model'
```

---

## File Operations

### Upload to VM
```bash
gcloud compute scp LOCAL_FILE openclaw-desktop:~/.openclaw/ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

### Download from VM
```bash
gcloud compute scp openclaw-desktop:~/.openclaw/FILE ./ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

### Backup Keys
```bash
gcloud compute scp --recurse openclaw-desktop:~/.openclaw/keys/ ./backup/ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

---

## Monitoring

### Check Costs (GCP Console)
```
https://console.cloud.google.com/billing
→ linkhealth-care-2024
→ Reports
→ Filter: Vertex AI
```

### Resource Usage
```bash
# RAM
free -h

# Disk
df -h /

# CPU
top
```

### Ollama (if installed)
```bash
# Status
sudo systemctl status ollama

# List models
ollama list

# Test
ollama run llama3.2:1b "test"
```

---

## Emergency

### Stop Gateway
```bash
systemctl --user stop openclaw-gateway
```

### Restore Config
```bash
cp ~/.openclaw/openclaw.json.backup.YYYYMMDD ~/.openclaw/openclaw.json
systemctl --user restart openclaw-gateway
```

### Check VM from Local
```bash
gcloud compute instances describe openclaw-desktop \
  --zone=us-central1-a \
  --format="get(status)"
```
