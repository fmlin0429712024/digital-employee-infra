#!/bin/bash
source .env

echo ">>> Waiting for vLLM to be ready..."
for i in {1..30}; do
    if curl -s -f -o /dev/null -H "Authorization: Bearer $VLLM_API_KEY" http://localhost:8000/v1/models; then
        echo ">>> vLLM is healthy!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 10
done

echo ">>> Testing Chat Completion..."
curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Authorization: Bearer $VLLM_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "messages": [
            {"role": "user", "content": "What implies that the deployment is successful?"}
        ],
        "max_tokens": 50
    }'

echo ""
echo ">>> Validation Finished."
