# Private LLM Deployment on GCP

Deploy your own private ChatGPT-like interface powered by **DeepSeek R1 Distill 8B** on Google Cloud Platform with NVIDIA L4 GPU.

## 🚀 Features

- **DeepSeek R1 Distill 8B** - Reasoning-optimized 8B parameter model
- **vLLM** - High-performance inference engine with OpenAI-compatible API
- **Open WebUI** - Beautiful ChatGPT-like interface
- **HTTPS Access** - Secure public access via Cloudflare Tunnel
- **Docker Compose** - Simple orchestration and deployment
- **Cost-Effective** - Runs on a single NVIDIA L4 GPU (~$0.50/hour on GCP)

## 📋 Prerequisites

> **Need to create a GPU VM?** See [../docs/12-gpu-vm-provisioning.md](../docs/12-gpu-vm-provisioning.md) for complete setup instructions.

- Google Cloud Platform account with credits
- GCP VM with NVIDIA L4 GPU (or similar)
- Docker and Docker Compose installed on VM
- Basic familiarity with terminal/SSH

## 🏗️ Architecture

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

## 🛠️ Installation

### 1. Clone this repository

```bash
git clone https://github.com/fmlin0429712024/LLM-Local-Deployment.git
cd LLM-Local-Deployment
```

### 2. Deploy the stack

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Pull Docker images for vLLM and Open WebUI
- Generate a secure API key
- Start both services
- Display the local access URL

### 3. (Optional) Enable public access

```bash
chmod +x setup-cloudflare.sh
./setup-cloudflare.sh
```

This creates a free public HTTPS URL via Cloudflare Tunnel.

## 📁 Project Structure

```
.
├── docker-compose.yml      # Container orchestration
├── setup.sh               # Initial deployment script
├── validate.sh            # Health check script
├── setup-ssl.sh           # Nginx + SSL setup (alternative)
├── setup-cloudflare.sh    # Cloudflare Tunnel setup
├── nginx.conf             # Nginx reverse proxy config
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

The `setup.sh` script creates a `.env` file with:

- `VLLM_API_KEY` - Secure API key for vLLM
- `HUGGING_FACE_HUB_TOKEN` - (Optional) For gated models

### Docker Compose Services

#### vLLM Service
- **Model**: `deepseek-ai/DeepSeek-R1-Distill-Llama-8B`
- **GPU Memory**: 90% utilization (~21.6GB)
- **Max Context**: 8192 tokens
- **Port**: 8000

#### Open WebUI
- **Port**: 3000
- **Data**: Persisted in Docker volume `open-webui-data`
- **First user**: Becomes admin automatically

## 🌐 Access Methods

### Local Access (SSH Tunnel)
```bash
# From your local machine
gcloud compute ssh isaac-sim-01 --project YOUR_PROJECT --zone YOUR_ZONE -- -L 3000:localhost:3000 -N
```
Then open: http://localhost:3000

### Public Access (Cloudflare Tunnel)
Run `./setup-cloudflare.sh` and use the generated URL (e.g., `https://random-name.trycloudflare.com`)

## 🔐 Security

- **User Management**: First user is admin; disable public signups in Admin Panel
- **API Key**: Randomly generated 32-character key
- **HTTPS**: Automatic via Cloudflare Tunnel
- **Firewall**: Ports 80/443 opened only when needed

## 🧪 Validation

```bash
chmod +x validate.sh
./validate.sh
```

This script:
1. Waits for vLLM to initialize
2. Sends a test chat completion request
3. Displays the response

## 💰 Cost Estimation

**GCP Costs** (us-central1):
- NVIDIA L4 GPU: ~$0.50/hour
- 500GB SSD: ~$85/month
- Network egress: Variable

**Total**: ~$360-400/month if running 24/7

**Savings Tip**: Stop the VM when not in use to pay only for storage.

## 🐛 Troubleshooting

### Model won't load
- Check disk space: `df -h`
- Verify GPU: `nvidia-smi`
- Check logs: `docker logs vllm-service`

### Can't access WebUI
- Verify containers: `docker ps`
- Check firewall: `sudo ufw status`
- Restart services: `docker compose restart`

### Cloudflare Tunnel stopped
```bash
# Check if running
ps aux | grep cloudflared

# Restart
cd ~/deepseek-app && ./setup-cloudflare.sh
```

## 📚 Additional Resources

- [vLLM Documentation](https://docs.vllm.ai/)
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [DeepSeek Model Card](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📄 License

MIT License - feel free to use this for personal or commercial projects.

## 🙏 Acknowledgments

- **DeepSeek** for the R1 Distill models
- **vLLM** team for the inference engine
- **Open WebUI** community for the interface
- **Cloudflare** for free tunneling service
