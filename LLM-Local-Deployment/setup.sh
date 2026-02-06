#!/bin/bash
set -e

# Configuration
ENV_FILE=".env"
DEFAULT_MODEL="deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

echo ">>> Starting Private LLM Stack Setup..."

# Check requirements
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    exit 1
fi

if ! nvidia-smi &> /dev/null; then
    echo "Error: NVIDIA driver not detected."
    exit 1
fi

# Setup .env file
if [ -f "$ENV_FILE" ]; then
    echo ">>> Loading existing .env file..."
    source $ENV_FILE
else
    echo ">>> Creating new .env file..."
    touch $ENV_FILE
fi

# Handle HF Token
if [ -z "$HUGGING_FACE_HUB_TOKEN" ]; then
    read -p "Enter your Hugging Face Hub Token (required for gated models): " INPUT_HF_TOKEN
    if [ -z "$INPUT_HF_TOKEN" ]; then
        echo "Warning: No token provided. Public models only."
    else
        echo "HUGGING_FACE_HUB_TOKEN=$INPUT_HF_TOKEN" >> $ENV_FILE
        export HUGGING_FACE_HUB_TOKEN=$INPUT_HF_TOKEN
    fi
fi

# Handle API Key
if [ -z "$VLLM_API_KEY" ]; then
    GENERATED_KEY="sk-$(openssl rand -hex 16)"
    echo ">>> Generating new secure API Key: $GENERATED_KEY"
    echo "VLLM_API_KEY=$GENERATED_KEY" >> $ENV_FILE
    export VLLM_API_KEY=$GENERATED_KEY
fi

# Pull and Start
echo ">>> Pulling images..."
docker compose pull

echo ">>> Starting services..."
docker compose up -d

echo ">>> Setup Complete!"
echo "API Key: $VLLM_API_KEY"
echo "WebUI will be available at http://$(curl -s ifconfig.me):3000 (after brief initialization)"
