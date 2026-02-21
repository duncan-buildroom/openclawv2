#!/bin/bash
# Test rotation system without waiting for full cron

cd "$(dirname "$0")"

echo "=== Rotation State Tester ==="
echo

echo "1. Current state:"
python3 rotation_state.py status
echo

echo "2. Pick 5 communities for posts:"
python3 rotation_state.py pick 5 posts
echo

echo "3. Pick 5 communities for comments:"
python3 rotation_state.py pick 5 comments
echo

echo "4. State after picks:"
python3 rotation_state.py status
echo

echo "=== Test complete ==="
