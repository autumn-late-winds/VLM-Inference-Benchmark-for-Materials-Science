# Transformers Qwen3-VL Baseline

This is an optional cloud-only baseline. It intentionally refuses inference unless `ALLOW_LOCAL_MODEL_DOWNLOAD=true`.

Use it only on a GPU server where downloading and caching large model weights is intentional. The MVP leaves actual model loading as a protected extension point so local development cannot accidentally trigger `from_pretrained` downloads.

