#!/usr/bin/env bash
set -euo pipefail
export MODEL_NAME="${MODEL_NAME:-Qwen/Qwen3-VL-8B-Instruct}"
export PORT="${PORT:-8001}"
export HF_HOME="${HF_HOME:-/models/hf}"
cd "$(dirname "$0")/../serving/vllm_qwen3_vl"
docker compose -f docker-compose.vllm.qwen3vl.yml up -d

