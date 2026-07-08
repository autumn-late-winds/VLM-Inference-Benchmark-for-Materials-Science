#!/usr/bin/env bash
set -euo pipefail
nvidia-smi || true
nvcc --version || true
docker --version || true
docker info | grep -i nvidia || true

