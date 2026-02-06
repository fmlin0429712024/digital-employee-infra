#!/bin/bash
set -e

echo ">>> Installing Cloudflare Tunnel (cloudflared)..."
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
rm cloudflared-linux-amd64.deb

echo ">>> Starting Cloudflare Tunnel..."
echo ""
echo "IMPORTANT: This will create a temporary public URL."
echo "The URL will be displayed below and will look like:"
echo "  https://random-name.trycloudflare.com"
echo ""
echo "This tunnel will run in the background."
echo "To stop it later, run: sudo pkill cloudflared"
echo ""

# Run cloudflared tunnel in background and capture output
nohup cloudflared tunnel --url http://localhost:3000 > /tmp/cloudflared.log 2>&1 &

# Wait for tunnel to start and extract URL
echo ">>> Waiting for tunnel to initialize..."
sleep 5

# Extract and display the URL
TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' /tmp/cloudflared.log | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo ">>> Checking logs for URL..."
    sleep 5
    TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' /tmp/cloudflared.log | head -1)
fi

if [ -n "$TUNNEL_URL" ]; then
    echo ""
    echo "=========================================="
    echo "✅ Cloudflare Tunnel is LIVE!"
    echo "=========================================="
    echo ""
    echo "Your LLM is now accessible at:"
    echo "  $TUNNEL_URL"
    echo ""
    echo "This URL has automatic HTTPS encryption."
    echo "=========================================="
else
    echo ">>> Could not extract URL. Check logs:"
    tail -20 /tmp/cloudflared.log
fi
