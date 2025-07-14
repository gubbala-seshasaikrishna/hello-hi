# Llama 3.2 Chat Interface

A mobile-friendly web chat interface for the unsloth/Llama-3.2-1B-bnb-4bit model that you can access from your iOS phone.

## Features

- 🦙 Powered by Llama 3.2 1B (4-bit quantized)
- 📱 Mobile-optimized interface for iOS
- 💬 Real-time chat with conversation history
- 🚀 Lightweight and fast responses
- 🌐 Local hosting with network access

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will:
- Start loading the model in the background
- Launch a web server on `http://0.0.0.0:5000`
- Be accessible from any device on your local network

### 3. Access from iOS

1. Find your computer's local IP address:
   ```bash
   ip addr show | grep inet
   ```
   Look for something like `192.168.1.100`

2. On your iPhone, open Safari and go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   For example: `http://192.168.1.100:5000`

3. For the best experience, add it to your home screen:
   - Tap the share button in Safari
   - Select "Add to Home Screen"

## System Requirements

- **RAM**: At least 4GB recommended (model uses ~2GB)
- **GPU**: CUDA-compatible GPU recommended but not required
- **Python**: 3.8 or higher
- **Network**: Both devices on the same local network

## Model Details

This chat interface uses the `unsloth/Llama-3.2-1B-bnb-4bit` model:
- **Size**: ~1 billion parameters
- **Quantization**: 4-bit for efficient memory usage
- **Performance**: Optimized for fast inference on consumer hardware

## Troubleshooting

### Model Loading Issues
- Ensure you have sufficient RAM (4GB+)
- Check internet connection for initial model download
- Wait for "Model ready ✓" status before chatting

### Network Access Issues
- Ensure both devices are on the same WiFi network
- Check if your firewall allows connections on port 5000
- Try using your computer's actual IP address instead of localhost

### Performance Issues
- Close other memory-intensive applications
- Consider using a GPU if available
- Restart the application if responses become slow

## Configuration

You can modify these settings in `app.py`:

- **Port**: Change `port=5000` to use a different port
- **Host**: Change `host='0.0.0.0'` to restrict access
- **Generation settings**: Adjust `temperature`, `max_new_tokens`, etc.

## Security Note

This application runs locally and is intended for personal use. It binds to all network interfaces (`0.0.0.0`) to allow access from your phone. Only run this on trusted networks.