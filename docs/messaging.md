# Messaging Channels

## Overview

| Channel | Codename | Purpose |
|---------|----------|---------|
| **Telegram** | "Pet" | Quick commands, real-time alerts |
| **WhatsApp** | "Mirror" | Deep thinking, complex reasoning |

## Telegram ("Pet")

Fast, lightweight interactions for quick tasks.

### Configuration

```yaml
telegram:
  enabled: true
  dmPolicy: pairing
  groupPolicy: allowlist
  streamMode: partial
```

### Environment Variable

Must be set in systemd service override:

```ini
Environment="TELEGRAM_BOT_TOKEN=<your-bot-token>"
```

## WhatsApp ("Mirror")

Thoughtful, deep-thinking interactions.

### Configuration

```yaml
whatsapp:
  enabled: true
```

### Known Limitations

- **Voice notes**: Baileys library downloads 0-byte files (upstream bug)
- Use Telegram for voice interactions instead

## Voice Support

Both channels support voice interactions:

| Feature | Telegram | WhatsApp |
|---------|----------|----------|
| **Receive voice notes** | ✅ Works | ⚠️ 0-byte bug |
| **Send voice replies** | ✅ Works | ✅ Works |

See [Voice Integration](voice.md) for configuration details.
