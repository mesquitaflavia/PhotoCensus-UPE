#!/usr/bin/env bash
# PhotoCensus installer for Linux and macOS
# Usage:  bash install_linux_mac.sh
cd "$(dirname "$0")"
if command -v python3 > /dev/null 2>&1; then
    python3 install.py
else
    python install.py
fi
