# Turtle 🐢

> *"Slow and steady wins the race"* - Building an AI-powered Digital Employee, one day at a time.

My personal journey documenting the creation of an autonomous AI agent infrastructure - a 24/7 "Digital Employee" accessible from anywhere.

---

## The Vision

Build a self-healing, always-available AI assistant that:
- **Never sleeps** - 24/7 availability via cloud infrastructure
- **Multi-channel** - Accessible via Telegram, WhatsApp, and voice
- **Self-healing** - Automatic failover between AI providers
- **Cost-optimized** - Free tiers first, paid as backup
- **Web-aware** - Real-time information via search integration

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         COMMAND CENTER                               │
│                                                                      │
│     📱 Telegram          📱 WhatsApp           🎤 Voice             │
│       "Pet"                "Mirror"           (FFmpeg)              │
│    Quick commands       Deep thinking       Voice notes             │
│                                                                      │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     🦞 OPENCLAW GATEWAY                      │   │
│  │                      (2026 Core Engine)                      │   │
│  │                  24/7 Persistent Agent Host                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│              ┌───────────────┼───────────────┐                      │
│              ▼               ▼               ▼                      │
│  ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐           │
│  │   TIER 1: FREE  │ │ TIER 2: FREE│ │  TIER 3: PAID   │           │
│  │   Antigravity   │ │  AI Studio  │ │   Vertex AI     │           │
│  │  Claude/Gemini  │ │   Gemini    │ │ $18K Credits    │           │
│  │   (Primary)     │ │  (Backup)   │ │ (Safety Net)    │           │
│  └─────────────────┘ └─────────────┘ └─────────────────┘           │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    🔍 BRAVE SEARCH                           │   │
│  │               Real-time Web Intelligence                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  ☁️ GCP COMPUTE ENGINE                       │   │
│  │              n2-standard-4 • us-central1-a                   │   │
│  │                  "openclaw-desktop"                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Current Stack

| Layer | Component | Technology | Status |
|-------|-----------|------------|--------|
| **Infrastructure** | Cloud Host | GCP n2-standard-4 | ✅ Live |
| **Orchestrator** | Agent Host | OpenClaw 2026 Core | ✅ Running |
| **Primary AI** | Antigravity | Claude/Gemini (FREE) | ✅ Active |
| **Backup AI** | AI Studio | Gemini 1.5 Pro (FREE) | ✅ Ready |
| **Safety Net** | Vertex AI | Gemini 2.x ($18K credits) | ✅ Configured |
| **Messaging** | Telegram | "Pet" - Quick commands | ✅ Connected |
| **Messaging** | WhatsApp | "Mirror" - Deep thinking | ✅ Connected |
| **Search** | Web Intelligence | Brave Search API | ✅ Enabled |
| **Voice STT** | Speech-to-Text | Whisper (local) | ✅ Active |
| **Voice TTS** | Text-to-Speech | edge-tts (Microsoft) | ✅ Active |

---

## Model Fallback Strategy

```
┌─────────────────────────────────────────────────────────────┐
│  Priority 1: Antigravity (FREE)                             │
│  └─ gemini-3-pro-low → gemini-3-flash → gemini-3-pro-high  │
│                                                             │
│  ↓ If quota exhausted (5hr reset)                          │
│                                                             │
│  Priority 2: Vertex AI (PAID - Cheapest First)             │
│  └─ gemini-2.0-flash → gemini-2.5-flash → gemini-1.5-pro   │
│                                                             │
│  Cost: $0.10-$1.25 per 1M input tokens                     │
│  Budget: $18,000 GCP credits                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Documentation

| Topic | Description |
|-------|-------------|
| [Infrastructure Setup](docs/infrastructure.md) | GCP VM, OpenClaw gateway, systemd configuration |
| [AI Providers](docs/ai-providers.md) | Antigravity, AI Studio, Vertex AI fallback chain |
| [Messaging Channels](docs/messaging.md) | Telegram & WhatsApp integration |
| [Voice Integration](docs/voice.md) | Whisper STT + edge-tts TTS setup |

---

## Quick Reference

### Connect to VM
```bash
gcloud compute ssh --zone "us-central1-a" "openclaw-desktop" --project "linkhealth-care-2024"
```

### Check Status
```bash
openclaw gateway status    # Gateway health
openclaw models status     # Model configuration
```

### Switch Models
```bash
# Via CLI
openclaw models set google-vertex/gemini-2.5-pro

# Via Telegram/WhatsApp
"Switch to gemini-2.5-pro"
"Use Claude Sonnet"
```

---

## Key Locations

| Resource | Location |
|----------|----------|
| **GCP Console** | https://console.cloud.google.com/ |
| **GCP Project** | linkhealth-care-2024 |
| **VM Instance** | openclaw-desktop (us-central1-a) |
| **Gateway Port** | 127.0.0.1:18789 |
| **Config File** | `~/.openclaw/openclaw.json` |
| **Logs** | `/tmp/openclaw/openclaw-*.log` |

---

## Repository Structure

```
turtle/
├── README.md                    # Project overview
└── docs/                        # Topic-based documentation
    ├── infrastructure.md       # GCP VM, systemd, gateway
    ├── ai-providers.md         # Model fallback strategy
    ├── messaging.md            # Telegram & WhatsApp
    └── voice.md                # STT & TTS configuration
```

---

## Philosophy

**Why "Turtle"?**

Building reliable AI infrastructure isn't about speed - it's about consistency, reliability, and steady progress. Like the turtle in the fable, this project prioritizes:

- 🐢 **Stability** over velocity
- 🐢 **Reliability** over features
- 🐢 **Cost-efficiency** over power
- 🐢 **Documentation** over memory

Each iteration adds another layer, another backup, another safeguard - until the system is truly unbreakable.
