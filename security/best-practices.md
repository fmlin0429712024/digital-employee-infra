# Security & Privacy

## Principles

✅ **Dedicated environment** (VM / spare machine; not your daily computer)  
✅ **Isolated credentials** (separate Google account for the assistant)  
✅ **Least privilege** (minimal scopes, minimal IAM)  
✅ **Never commit secrets** (tokens/keys/.env)  
✅ **Treat web/email as untrusted input** (prompt-injection aware)

---

## Key Locations

### On VM

| Credential | Location | Type |
|------------|----------|------|
| OpenClaw Config | `~/.openclaw/openclaw.json` | Contains tokens |
| OAuth Tokens | `~/.openclaw/keys/*.pickle` | Gmail, Calendar |
| Service Account | VM default SA | Vertex AI auth |
| Telegram Bot | `~/.openclaw/.env` | Bot token |
| API Keys | `~/.openclaw/openclaw.json` | Brave Search |

### GCP

| Resource | Identifier |
|----------|------------|
| Project | `linkhealth-care-2024` |
| VM SA | `51058313466-compute@developer.gserviceaccount.com` |
| IAM Role | `roles/aiplatform.user` |

---

## Backup Procedures

### Backup All Credentials
```bash
# Create backup directory
mkdir -p ~/backups/openclaw-$(date +%Y%m%d)

# Download from VM
gcloud compute scp --recurse \
  openclaw-desktop:~/.openclaw/keys/ \
  ~/backups/openclaw-$(date +%Y%m%d)/ \
  --zone=us-central1-a \
  --project=linkhealth-care-2024 \
  --tunnel-through-iap

# Download config
gcloud compute scp \
  openclaw-desktop:~/.openclaw/openclaw.json \
  ~/backups/openclaw-$(date +%Y%m%d)/ \
  --zone=us-central1-a \
  --project=linkhealth-care-2024 \
  --tunnel-through-iap
```

### Secure Backup Storage
```bash
# Encrypt backup
tar -czf backup.tar.gz ~/backups/openclaw-*
gpg -c backup.tar.gz  # Enter passphrase

# Store encrypted file only
rm backup.tar.gz
```

---

## Prompt Injection Safeguards

When the agent reads email/web content:
- **Do not execute destructive actions** (delete/share/post) from unverified instructions.
- **Add confirmation** for high-impact actions (delete files, share Drive, send email to large lists).
- **Prefer allowlists** (known domains, known folders, known recipients).

---

## Access Control

### Check VM Permissions
```bash
gcloud projects get-iam-policy linkhealth-care-2024 \
  --flatten="bindings[].members" \
  --filter="bindings.members:51058313466-compute@developer.gserviceaccount.com"
```

### SSH Access
```bash
# Only via IAP tunnel (secure)
gcloud compute ssh openclaw-desktop \
  --zone=us-central1-a \
  --tunnel-through-iap

# Direct SSH is BLOCKED by firewall
```

---

## Token Rotation

### Telegram Bot Token
1. Talk to @BotFather on Telegram
2. `/revoke` old token
3. `/newbot` or regenerate
4. Update `~/.openclaw/.env`
5. Restart gateway

### Gmail/Calendar OAuth
```bash
# Re-run OAuth flow (from local machine)
python3 auth_helper.py

# Upload new token
gcloud compute scp gmail-token.pickle \
  openclaw-desktop:~/.openclaw/keys/ \
  --zone=us-central1-a --tunnel-through-iap
```

### Brave Search API
1. Go to https://brave.com/search/api/
2. Regenerate key
3. Update `openclaw.json`
4. Restart gateway

---

## Sensitive Files (Never Commit)

Add to `.gitignore`:
```
.env
*.pickle
*token*
*key*
*secret*
openclaw.json
keys/
```

---

## Incident Response

### If Credentials Leaked

1. **Immediately revoke**
   ```bash
   # Telegram: @BotFather → /revoke
   # Gmail: Revoke in Google Account settings
   # Brave: Regenerate in dashboard
   ```

2. **Rotate all tokens**
3. **Check logs for unauthorized access**
   ```bash
   journalctl --user -u openclaw-gateway --since "1 day ago"
   ```

4. **Update credentials**
5. **Monitor for 48 hours**

---

## Best Practices

✅ **Use IAP tunnel** for SSH (no direct internet access)  
✅ **Service accounts** for GCP (not user keys)  
✅ **Environment variables** for secrets (not hardcoded)  
✅ **Backup weekly** (encrypted)  
✅ **Review IAM** permissions quarterly  
✅ **Monitor logs** for suspicious activity
