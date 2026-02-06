#!/bin/bash
set -e

DOMAIN="ai.35.238.78.4.nip.io"

echo ">>> Installing Nginx and Certbot..."
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx

echo ">>> Stopping Nginx temporarily..."
sudo systemctl stop nginx

echo ">>> Creating initial Nginx configuration..."
sudo tee /etc/nginx/sites-available/nip-io > /dev/null <<EOF
server {
    listen 80;
    server_name ai.35.238.78.4.nip.io;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

echo ">>> Enabling site..."
sudo ln -sf /etc/nginx/sites-available/nip-io /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo ">>> Testing Nginx configuration..."
sudo nginx -t

echo ">>> Starting Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

echo ">>> Obtaining SSL certificate..."
sudo certbot --nginx -d ai.35.238.78.4.nip.io --non-interactive --agree-tos --email fmlin0429712024@gmail.com --redirect

echo ">>> SSL Setup Complete!"
echo "Your site is now available at https://ai.35.238.78.4.nip.io"
