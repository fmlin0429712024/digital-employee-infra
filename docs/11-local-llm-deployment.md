# 11 - Local LLM Deployment (GPU Infrastructure)

This document covers the local LLM deployment infrastructure that supports private, on-premises AI inference for the digital employee system.

---

## Overview

The Local LLM Deployment provides GPU-accelerated inference capabilities for running private language models within your own infrastructure, complementing the cloud-based AI providers documented in [03-ai-providers.md](03-ai-providers.md).

| Aspect | Details |
|--------|---------|
| **Purpose** | Private, self-hosted LLM inference for sensitive workloads |
| **Model** | DeepSeek R1 Distill Llama 8B (reasoning-optimized) |
| **Inference Engine** | vLLM (OpenAI-compatible API) |
| **Interface** | Open WebUI (ChatGPT-like UI) |
| **Hardware** | NVIDIA L4 GPU (24GB VRAM) on GCP |
| **Deployment** | Docker Compose orchestration |

---

## Architecture Integration

### How It Fits Into Digital Employee Infrastructure

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIGITAL EMPLOYEE ECOSYSTEM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Cloud AI Providers (03-ai-providers.md)                        │
│  ├── Antigravity (Free) → AI Studio → Vertex AI                 │
│  ├── Google AI Studio API (OpenCode)                            │
│  └── Claude, GPT (Optional)                                     │
│                                                                  │
│  Local GPU Infrastructure (THIS DOCUMENT)                       │
│  └── vLLM + DeepSeek R1 (Private/Sensitive workloads)          │
│      ├── OpenAI-compatible API                                  │
│      ├── Open WebUI interface                                   │
│      └── Cloudflare Tunnel (HTTPS access)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Use Cases for Local LLM

| Use Case | Why Local? |
|----------|------------|
| **PHI/PII Processing** | HIPAA compliance - data never leaves VPC |
| **Proprietary Business Logic** | Audit rules, clinical protocols stay private |
| **Fine-Tuning** | Train on domain-specific data (e.g., medical auditing) |
| **Cost Control** | Fixed GPU cost vs. variable API costs |
| **Offline Operation** | No internet dependency for critical workflows |

---

## Deployment Details

### Infrastructure Location

The LLM deployment code is maintained in:
- **Repository**: `LLM-Local-Deployment/` subdirectory
- **Full Documentation**: See `LLM-Local-Deployment/README.md`
- **Walkthrough**: See `LLM-Local-Deployment/WALKTHROUGH.md`
- **GPU VM Setup**: See [12-gpu-vm-provisioning.md](12-gpu-vm-provisioning.md) for creating a new GPU VM

### Quick Start

```bash
cd LLM-Local-Deployment
chmod +x setup.sh
./setup.sh
```

### Architecture Diagram

```
┌─────────────────────────────────────────────┐
│           GCP VM (isaac-sim-01)             │
│  ┌───────────────────────────────────────┐  │
│  │      Docker Compose Network           │  │
│  │                                       │  │
│  │  ┌─────────────┐   ┌──────────────┐  │  │
│  │  │   vLLM      │   │  Open WebUI  │  │  │
│  │  │  (Port 8000)│◄──┤  (Port 3000) │  │  │
│  │  │             │   │              │  │  │
│  │  │ DeepSeek R1 │   │   SQLite DB  │  │  │
│  │  │   (15GB)    │   │              │  │  │
│  │  └─────────────┘   └──────────────┘  │  │
│  │                          ▲            │  │
│  └──────────────────────────┼────────────┘  │
└─────────────────────────────┼────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │ Cloudflare Tunnel │
                    │   (HTTPS/SSL)     │
                    └─────────┬─────────┘
                              │
                          ┌───┴───┐
                          │ Users │
                          └───────┘
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **OpenAI-Compatible API** | Drop-in replacement for OpenAI API endpoints |
| **GPU Acceleration** | NVIDIA L4 with 90% memory utilization (~21.6GB) |
| **Secure Access** | HTTPS via Cloudflare Tunnel (free) |
| **Data Persistence** | Docker volumes for user data and chat history |
| **Cost-Effective** | ~$360-400/month for 24/7 operation |

---

## Integration with OpenClaw/OpenCode

### Current Integration Status

| Component | Integration Level |
|-----------|------------------|
| **OpenClaw** | ⚠️ Not yet integrated (uses Antigravity) |
| **OpenCode** | ⚠️ Not yet integrated (uses AI Studio) |
| **Standalone** | ✅ Fully operational via Open WebUI |

### Future Integration Path

To integrate local LLM with OpenClaw/OpenCode:

1. **OpenCode Integration**
   ```json
   // ~/.config/opencode/opencode.json
   {
     "model": "openai/deepseek-r1-distill-llama-8b",
     "baseURL": "http://localhost:8000/v1"
   }
   ```

2. **OpenClaw Integration**
   - Configure LiteLLM to route specific requests to local vLLM
   - Use for sensitive/private tasks only
   - Keep Antigravity for general communication

---

## Cost Comparison

### Local GPU vs Cloud APIs

| Scenario | Local GPU (L4) | Cloud API (Gemini) |
|----------|----------------|-------------------|
| **Fixed Cost** | $360-400/month | $0/month base |
| **Per 1M Tokens** | $0 (included) | $0.15-1.25 |
| **Break-Even** | ~300M tokens/month | N/A |
| **PHI Compliance** | ✅ Native | ⚠️ Requires BAA |
| **Fine-Tuning** | ✅ Yes | ❌ No |

**Recommendation**: Use local GPU for high-volume, sensitive workloads; use cloud APIs for general tasks.

---

## Security & Compliance

### Data Privacy

| Aspect | Implementation |
|--------|---------------|
| **Network Isolation** | Private Docker bridge network |
| **API Authentication** | 32-character secure API key |
| **HTTPS** | Automatic via Cloudflare Tunnel |
| **User Management** | First user = admin; disable public signups |
| **Data Residency** | All data stays on VM (no external API calls) |

### HIPAA Considerations

✅ **Compliant for PHI Processing**:
- Data never leaves your VPC
- No third-party API calls
- Full audit trail via Docker logs
- Encrypted in transit (HTTPS)

---

## Monitoring & Maintenance

### Health Checks

```bash
cd LLM-Local-Deployment
chmod +x validate.sh
./validate.sh
```

### Common Operations

| Task | Command |
|------|---------|
| **Start Services** | `docker compose up -d` |
| **Stop Services** | `docker compose down` |
| **View Logs** | `docker logs vllm-service` |
| **Check GPU** | `nvidia-smi` |
| **Restart** | `docker compose restart` |

---

## Relationship to Agent Framework Vision

This local LLM deployment is a **foundational component** for the [10-agent-framework-vision.md](10-agent-framework-vision.md) architecture:

| Vision Component | Local LLM Role |
|------------------|----------------|
| **Audit Agent Layer** | Provides the inference engine (vLLM) |
| **Local Model** | DeepSeek R1 (current), fine-tunable for auditing |
| **Data Sovereignty** | Ensures PHI never leaves VPC |
| **Fine-Tuning Pipeline** | Foundation for domain-specific training |

---

## File Locations

| File | Purpose |
|------|---------|
| `LLM-Local-Deployment/docker-compose.yml` | Container orchestration |
| `LLM-Local-Deployment/setup.sh` | Initial deployment script |
| `LLM-Local-Deployment/validate.sh` | Health check script |
| `LLM-Local-Deployment/setup-cloudflare.sh` | Public HTTPS setup |
| `LLM-Local-Deployment/README.md` | Detailed deployment guide |
| `LLM-Local-Deployment/WALKTHROUGH.md` | Step-by-step walkthrough |

---

## Next Steps

1. **Test Integration**: Configure OpenCode to use local vLLM endpoint
2. **Fine-Tuning**: Prepare domain-specific training data
3. **Production Hardening**: Add monitoring, alerting, backups
4. **Cost Optimization**: Implement auto-shutdown for non-business hours

---

## Navigation

- Previous: [10-agent-framework-vision.md](10-agent-framework-vision.md)
- Next: [12-gpu-vm-provisioning.md](12-gpu-vm-provisioning.md)
- Related: [03-ai-providers.md](03-ai-providers.md)
- Start: [01-overview.md](01-overview.md)
