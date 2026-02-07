# Model Fallback Strategy

## Overview

Multi-tier strategy to ensure 24/7 availability while minimizing costs.

---

## Tier 1: Antigravity (FREE)

**Provider:** google-antigravity  
**Cost:** FREE  
**Quota:** Resets every 5 hours  

### Models
- `gemini-3-pro-low`
- `gemini-3-flash`
- `gemini-3-pro-high`
- `claude-sonnet-4-5`
- `claude-opus-4-5`

### Use Case
- Primary for day-to-day tasks
- No cost, generous quota
- Multiple model options

---

## Tier 2: Vertex AI (PAID)

**Provider:** google-vertex  
**Cost:** Pay per token  
**Budget:** $18,000 GCP credits  

### Models (Ordered by Cost)

| Model | Input Cost | Output Cost | Use Case |
|-------|------------|-------------|----------|
| **gemini-2.0-flash** | $0.10/1M | $0.40/1M | **Default** (optimized) |
| gemini-2.5-flash | $0.15/1M | $0.60/1M | Balanced performance |
| gemini-1.5-pro | $1.25/1M | $5.00/1M | Complex reasoning only |

### Use Case
- Automatic fallback when Antigravity exhausted
- Guaranteed availability (no quota limits)
- Safety net for production use

---

## Fallback Flow

```
Request comes in
    ↓
Try: Antigravity gemini-3-flash (FREE)
    ↓ (if quota exhausted)
Try: Vertex gemini-2.0-flash ($0.10/1M)
    ↓ (if fails)
Try: Vertex gemini-2.5-flash ($0.15/1M)
    ↓ (if fails)
Try: Antigravity gemini-3-pro-high (FREE)
    ↓ (if quota exhausted)
Try: Vertex gemini-1.5-pro ($1.25/1M)
```

**Result:** Always available, cost-optimized.

---

## Configuration

### Current Setup
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google-vertex/gemini-2.0-flash",
        "fallbacks": [
          "google-antigravity/gemini-3-flash",
          "google-vertex/gemini-2.5-flash",
          "google-antigravity/gemini-3-pro-high",
          "google-vertex/gemini-1.5-pro"
        ]
      }
    }
  }
}
```

### Why This Order?
1. **Primary = Vertex 2.0-flash**: Reliable, cheap ($0.10/1M)
2. **Fallback 1 = Antigravity**: Try free tier
3. **Fallback 2 = Vertex 2.5-flash**: Slightly more expensive
4. **Fallback 3 = Antigravity Pro**: Free but may be quota-limited
5. **Last Resort = Vertex Pro**: Most expensive ($1.25/1M)

---

## Cost Optimization

### Before Optimization
- Primary: `gemini-2.5-flash` ($0.15/1M)
- Monthly: ~$150 for 1M tokens

### After Optimization
- Primary: `gemini-2.0-flash` ($0.10/1M)
- Monthly: ~$100 for 1M tokens
- **Savings: 33%**

---

## Monitoring

### Check Current Model
```bash
journalctl --user -u openclaw-gateway -n 20 | grep "agent model"
```

### View Fallback Chain
```bash
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.model'
```

### Track Costs
```
GCP Console → Billing → Reports
→ Filter: Vertex AI
→ Group by: SKU
```

---

## When to Change Models

### Use Cheaper Model (2.0-flash)
- ✅ Routine tasks
- ✅ Simple queries
- ✅ Status checks
- ✅ Quick commands

### Use Expensive Model (1.5-pro)
- ⚠️ Complex reasoning
- ⚠️ Multi-step analysis
- ⚠️ Architecture decisions
- ⚠️ Code refactoring

**Manual Override:**
```bash
# Via Telegram/WhatsApp
"Switch to Pro"
"Use gemini-1.5-pro"
```

---

## Troubleshooting

### All Models Failing
```bash
# Check Antigravity auth
cat ~/.openclaw/openclaw.json | jq '.auth.profiles."google-antigravity"'

# Check Vertex AI permissions
gcloud projects get-iam-policy linkhealth-care-2024 | grep aiplatform

# Check gateway logs
journalctl --user -u openclaw-gateway -n 50
```

### High Costs
```bash
# Verify using cheap model
journalctl --user -u openclaw-gateway | grep "agent model" | tail -20

# Should mostly show: gemini-2.0-flash
# If seeing: gemini-1.5-pro → investigate why
```
