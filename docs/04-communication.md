# 04 - Communication Channels

## Overview

The Digital Employee is accessible via multiple channels, each optimized for different use cases.

| Channel | Codename | Best For |
|---------|----------|----------|
| **Telegram** | "Pet" | Quick commands, real-time alerts, voice |
| **WhatsApp** | "Mirror" | Deep thinking, complex reasoning |
| **Voice** | - | Hands-free interaction |

---

## Telegram ("Pet")

Fast, lightweight interactions for quick tasks.

### Features

- Real-time streaming responses
- Voice note support (send and receive)
- Rich formatting (markdown)
- Bot commands

### Configuration

In `~/.openclaw/openclaw.json`:

```json
{
  "telegram": {
    "enabled": true,
    "dmPolicy": "pairing",
    "groupPolicy": "allowlist",
    "streamMode": "partial"
  }
}
```

### Environment Variable

In systemd service override:

```ini
Environment="TELEGRAM_BOT_TOKEN=<your-bot-token>"
```

### Setup Steps

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create new bot with `/newbot`
3. Copy the token
4. Add to systemd environment
5. Restart gateway

---

## WhatsApp ("Mirror")

Thoughtful, deep-thinking interactions.

### Features

- End-to-end encryption
- Voice replies (sending)
- Rich media support

### Configuration

```json
{
  "whatsapp": {
    "enabled": true
  }
}
```

### Known Limitations

| Feature | Status |
|---------|--------|
| Receive voice notes | ⚠️ 0-byte bug in Baileys library |
| Send voice replies | ✅ Works |

**Workaround**: Use Telegram for voice interactions.

---

## Voice Integration

Full voice pipeline at **$0 cost**.

### How It Works

```
📱 User sends voice note
    ↓
🎤 Whisper transcribes to text (local, free)
    ↓
🤖 AI processes and generates response
    ↓
🔊 edge-tts converts to speech (free)
    ↓
📱 User receives voice reply
```

### Speech-to-Text (STT)

| Attribute | Value |
|-----------|-------|
| **Engine** | OpenAI Whisper |
| **Model** | `base` |
| **Cost** | FREE (runs locally) |
| **Platforms** | Telegram ✅, WhatsApp ⚠️ |

### Text-to-Speech (TTS)

| Attribute | Value |
|-----------|-------|
| **Engine** | edge-tts (Microsoft) |
| **Voice** | `en-US-AriaNeural` |
| **Cost** | FREE (unlimited) |
| **Output** | MP3 voice notes |

### Configuration

In `~/.openclaw/openclaw.json`:

```json
{
  "messages": {
    "tts": {
      "enabled": true,
      "engine": "edge-tts",
      "voice": "en-US-AriaNeural"
    }
  },
  "tools": {
    "media": {
      "audio": {
        "transcription": {
          "enabled": true,
          "engine": "whisper",
          "model": "base"
        }
      }
    }
  }
}
```

### Available Voices

| Voice | Language |
|-------|----------|
| `en-US-AriaNeural` | English (US, Female) |
| `en-US-GuyNeural` | English (US, Male) |
| `en-GB-SoniaNeural` | English (UK, Female) |
| `zh-CN-XiaoxiaoNeural` | Chinese (Female) |

List all voices:

```bash
edge-tts --list-voices
```

### Dependencies

```bash
pip install edge-tts openai-whisper
```

FFmpeg is also required (pre-installed on most systems).

---

## Channel Comparison

| Feature | Telegram | WhatsApp |
|---------|----------|----------|
| **Response Speed** | Fast (streaming) | Slower (complete) |
| **Voice Input** | ✅ Full support | ⚠️ Limited |
| **Voice Output** | ✅ Full support | ✅ Full support |
| **Best For** | Quick tasks | Complex discussions |
| **Privacy** | Standard | End-to-end encrypted |

---

## Navigation

- Previous: [03-ai-providers.md](03-ai-providers.md)
- Next: [05-capabilities.md](05-capabilities.md)
