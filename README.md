# Llama-3.2-1B Local Chatbot

This mini-project lets you chat with the 1-billion-parameter **unsloth/Llama-3.2-1B-bnb-4bit** model from HuggingFace using nothing more than Python and a web browser.  The model is loaded with 4-bit quantised weights, so it can run on a single consumer GPU or even on CPU (slowly).

The web UI is powered by [Gradio](https://gradio.app/) and is reachable from any device on your local network – including your iOS phone – without exposing the server to the public internet.

---

## 1.  Setup (once)

```bash
# Clone / download this repo and cd into it

# 1.  Create & activate a Python 3.10+ virtual env (recommended)
python3 -m venv .venv
source .venv/bin/activate

# 2.  Install dependencies (≈ 1–2 min)
pip install -r requirements.txt
```

The first time you run the app, the model (~530 MB) will be downloaded from HuggingFace automatically and cached under `~/.cache/huggingface`.

---

## 2.  Launch the chat server

```bash
python chat_llama.py
```

By default the server binds to **`0.0.0.0:7860`**, making it reachable from any device on the same Wi-Fi/LAN.

* On the machine that runs the model, open:  <http://localhost:7860>
* On your iPhone (or any other device connected to the same network):
  1. Find the host machine’s local IP address, e.g. `192.168.1.42`.
  2. Open Safari and navigate to `http://192.168.1.42:7860`.

No internet connection is required once the model files are cached.

---

## 3.  Tips & troubleshooting

* **Memory usage** – The 1 B model in 4-bit uses ~2 GB of VRAM; on CPU it will occupy ~4 GB of RAM plus 1–2 GB for overhead.
* **Speed** – A recent NVIDIA GPU (RTX 20-series +) yields real-time responses.  CPU-only inference works but is much slower.
* **Custom ports / host** – Set the `PORT` environment variable before launching to change the port.  You can also pass the usual Gradio flags (e.g. `--share`) by editing `chat_llama.py`.
* **Updating packages** – If you encounter CUDA / PyTorch compatibility issues, ensure that the installed PyTorch build matches your local CUDA version.

---

### Uninstall / clean-up

```bash
rm -rf ~/.cache/huggingface/hub/models--unsloth*   # remove model weights (optional)
rm -rf .venv                                        # remove virtual environment (optional)
```

---

Enjoy chatting with your *on-premise* Llama-3 🤗