#!/usr/bin/env bash
set -euo pipefail
if [ "${ALLOW_LOCAL_MODEL_DOWNLOAD:-false}" != "true" ]; then
  echo "Refusing to start Transformers baseline without ALLOW_LOCAL_MODEL_DOWNLOAD=true."
  exit 1
fi
docker build -t transformers-qwen3-vl-baseline -f serving/transformers_qwen3_vl/Dockerfile .
docker run --gpus all -p 127.0.0.1:8002:8002 -e ALLOW_LOCAL_MODEL_DOWNLOAD=true transformers-qwen3-vl-baseline

