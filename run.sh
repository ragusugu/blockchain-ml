#!/bin/bash

# Infinite loop to run the fetch_and_store.py script every 30 minutes
while true; do
    echo "Starting data fetch at $(date)"
    python fetch_and_store.py
    echo "Data fetch completed at $(date). Sleeping for 30 minutes..."
    sleep 1800  # 30 minutes = 1800 seconds
done