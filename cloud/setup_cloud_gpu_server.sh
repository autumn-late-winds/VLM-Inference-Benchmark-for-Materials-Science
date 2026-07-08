#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y git curl python3-venv docker.io
sudo mkdir -p /models/hf /models/torch
sudo chown -R "$USER":"$USER" /models
echo 'export HF_HOME=/models/hf' >> ~/.bashrc
echo 'export TRANSFORMERS_CACHE=/models/hf' >> ~/.bashrc
echo "Install NVIDIA Container Toolkit according to your cloud image documentation if it is not already present."

