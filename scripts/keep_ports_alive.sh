#!/bin/bash

# Monitor and restart port-forwards if they die
# Run this in background: nohup ./keep_ports_alive.sh > /tmp/port_monitor.log 2>&1 &

set +e

while true; do
  # Check if port-forwards are alive
  if ! pgrep -f "kubectl port-forward.*frontend.*3000" > /dev/null; then
    echo "[$(date)] 🔄 Frontend port-forward died, restarting..."
    pkill -9 -f "kubectl port-forward.*frontend" 2>/dev/null
    kubectl port-forward -n blockchain-ml service/frontend 3000:3000 > /dev/null 2>&1 &
  fi

  if ! pgrep -f "kubectl port-forward.*backend.*5000" > /dev/null; then
    echo "[$(date)] 🔄 Backend port-forward died, restarting..."
    pkill -9 -f "kubectl port-forward.*backend" 2>/dev/null
    kubectl port-forward -n blockchain-ml service/backend 5000:5000 > /dev/null 2>&1 &
  fi

  sleep 5
done
