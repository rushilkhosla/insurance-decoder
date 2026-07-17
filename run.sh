#!/bin/zsh
# Start Insurance Decoder and open it in the browser
cd "$(dirname "$0")"
if [ ! -d venv ]; then
  python3 -m venv venv
  ./venv/bin/pip install --quiet flask pypdf anthropic
fi
./venv/bin/python app.py &
sleep 1
open http://127.0.0.1:8523
wait
