#!/bin/bash
# Start Public Tunnel for Blockchain Fraud Detection AI
# Using Cloudflare Tunnel (no password required)

echo "🚀 Starting Blockchain Fraud Detection Tunnel..."
nohup cloudflared tunnel --url http://localhost:3000 > /tmp/tunnel.log 2>&1 &

sleep 5
echo ""
echo "✅ Tunnel started!"
echo ""
echo "🔗 Your public URL:"
grep -oP 'https://[^\s]+\.trycloudflare\.com' /tmp/tunnel.log | head -1
echo ""
echo "📝 Log file: /tmp/tunnel.log"
echo "🛑 To stop: pkill -f cloudflared"
echo ""
echo "✨ No password required - just open the URL!"
