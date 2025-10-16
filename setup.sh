#!/usr/bin/env bash
set -euo pipefail

# Colab thường không cần sudo, nhưng để phổ quát thì giữ lại:
sudo apt-get update -qq
sudo apt-get install -y graphviz

# Cài Python deps
pip install -r requirements.txt

# Kiểm tra graphviz đã có
which dot || true
dot -V || true
