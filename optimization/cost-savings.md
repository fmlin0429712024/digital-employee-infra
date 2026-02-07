# Token Optimization

**Date:** February 7, 2026  
**Status:** ✅ Implemented  
**Savings:** 33% cost reduction on Vertex AI

---

## What We Did

### 1. Model Optimization
**Changed primary model to cheaper option:**
- **Before:** `gemini-2.5-flash` ($0.15/1M input)
- **After:** `gemini-2.0-flash` ($0.10/1M input)
- **Savings:** 33% on input tokens

### 2. Fallback Chain Optimized
**Reordered to use cheapest first:**
1. Antigravity gemini-3-flash (FREE)
2. Vertex gemini-2.5-flash ($0.15/1M)
3. Antigravity gemini-3-pro-high (FREE)
4. Vertex gemini-1.5-pro ($1.25/1M)

### 3. Ollama Installed (Not Integrated)
- ✅ Installed: llama3.2:1b model
- ❌ Not used for heartbeats (OpenClaw doesn't support config)
- Available for future use

---

## Cost Impact

### Per Request
| Tokens | Before | After | Savings |
|--------|--------|-------|---------|
| 10K | $0.0015 | $0.0010 | 33% |
| 100K | $0.015 | $0.010 | 33% |
| 1M | $0.15 | $0.10 | 33% |

### Monthly Projection
**Conservative (100 requests/day, 5K tokens avg):**
- Before: $2.25/month
- After: $1.50/month
- **Savings: $0.75/month**

**High Usage (1M tokens/month):**
- Before: $150/month
- After: $100/month
- **Savings: $50/month**

---

## Implementation Commands

### Backup Config
```bash
ssh openclaw-desktop
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)
```

### Change Model
```python
# Edit config
import json
with open("~/.openclaw/openclaw.json", "r") as f:
    config = json.load(f)

config["agents"]["defaults"]["model"]["primary"] = "google-vertex/gemini-2.0-flash"

with open("~/.openclaw/openclaw.json", "w") as f:
    json.dump(config, f, indent=2)
```

### Restart Gateway
```bash
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway
```

### Verify
```bash
journalctl --user -u openclaw-gateway -n 20 | grep "agent model"
# Should show: google-vertex/gemini-2.0-flash
```

---

## Monitoring

### Check Current Model
```bash
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model.primary'
```

### View Costs (GCP Console)
```
https://console.cloud.google.com/billing
→ linkhealth-care-2024
→ Reports → Filter: Vertex AI
→ Group by: SKU
```

### Compare Before/After
- Track daily costs starting Feb 7, 2026
- Should see ~33% reduction in Vertex AI input token costs

---

## What Didn't Work

### Attempted but OpenClaw Doesn't Support:
- ❌ Context management config
- ❌ Rate limiting config
- ❌ Prompt caching config
- ❌ Ollama for heartbeats config

**Reason:** OpenClaw's config schema doesn't expose these settings.

---

## Rollback

### If Issues Occur
```bash
# Restore backup
cp ~/.openclaw/openclaw.json.backup.20260207 ~/.openclaw/openclaw.json

# Restart
systemctl --user restart openclaw-gateway
```

---

## Files

- `config-templates/openclaw-optimized.json` - Optimized config template
- Backup: `~/.openclaw/openclaw.json.backup.20260207-102008`
