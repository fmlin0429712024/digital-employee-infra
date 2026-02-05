# Voice Integration

## Overview

Full voice pipeline at **$0 cost**:

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

## Speech-to-Text (STT)

| Attribute | Value |
|-----------|-------|
| **Engine** | OpenAI Whisper |
| **Model** | `base` |
| **Cost** | FREE (runs locally) |
| **Platforms** | Telegram ✅, WhatsApp ⚠️ |

## Text-to-Speech (TTS)

| Attribute | Value |
|-----------|-------|
| **Engine** | edge-tts (Microsoft) |
| **Voice** | `en-US-AriaNeural` |
| **Cost** | FREE (unlimited) |
| **Output** | MP3 voice notes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

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

## Available Voices

edge-tts supports many voices. Examples:

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

## Known Limitations

- **WhatsApp voice notes**: Baileys library downloads 0-byte files
- **Workaround**: Use Telegram for voice interactions

## Dependencies

Installed on VM:

```bash
pip install edge-tts openai-whisper
```

Whisper also requires FFmpeg (pre-installed).
