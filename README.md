# LLM Chat - Llama 3.2 1B Local Chat Interface

A beautiful, mobile-responsive chat interface for running the **unsloth/Llama-3.2-1B-bnb-4bit** model locally on your device. Optimized for iOS Safari with PWA support for a native app-like experience.

## ✨ Features

- 🤖 **Local LLM**: Chat with Llama 3.2 1B running entirely on your machine
- 📱 **iOS Optimized**: Responsive design that works beautifully on iPhone
- 🔒 **Privacy First**: All conversations stay on your device
- ⚡ **4-bit Quantization**: Efficient memory usage with BitsAndBytes
- 💾 **Message History**: Automatic chat history saving in browser storage
- ⚙️ **Customizable**: Adjust temperature, max length, and top-p parameters
- 📲 **PWA Support**: Install as an app on your iPhone home screen
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- At least 4GB RAM (8GB+ recommended)
- GPU support optional but recommended for faster inference

### Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application:**
   ```bash
   python run.py
   ```

4. **Access on your iPhone:**
   - Make sure your phone and computer are on the same Wi-Fi network
   - Open Safari on your iPhone
   - Go to the Network URL shown in the terminal (e.g., `http://192.168.1.100:8000`)
   - For best experience: Tap Share → "Add to Home Screen"

## 📋 Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
transformers==4.36.0
torch==2.1.0
accelerate==0.24.1
bitsandbytes==0.41.3
pydantic==2.5.0
python-multipart==0.0.6
jinja2==3.1.2
aiofiles==23.2.0
```

## 🛠️ Manual Setup

If you prefer to start manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser to `http://localhost:8000`

## 📱 iPhone Setup

### Adding to Home Screen

1. Open Safari on your iPhone
2. Navigate to your local server URL
3. Tap the Share button (square with arrow up)
4. Scroll down and tap "Add to Home Screen"
5. Customize the name if desired and tap "Add"

The app will now appear on your home screen and behave like a native app!

### Features on iOS

- ✅ Full-screen app experience (no browser UI)
- ✅ Touch-optimized interface
- ✅ Prevented zoom on double-tap
- ✅ Smooth scrolling and animations
- ✅ iOS-style keyboard handling
- ✅ Automatic message history saving

## ⚙️ Configuration

The chat interface includes a settings panel where you can adjust:

- **Temperature** (0.1 - 1.0): Controls response creativity
- **Max Response Length** (50 - 1000): Maximum tokens in response
- **Top P** (0.1 - 1.0): Controls response diversity

## 🔧 Troubleshooting

### Model Loading Issues

If the model fails to load:
1. Ensure you have sufficient RAM (4GB minimum)
2. Check your internet connection for initial model download
3. Verify all dependencies are installed correctly

### iPhone Access Issues

If you can't access from iPhone:
1. Confirm both devices are on the same Wi-Fi network
2. Check if your firewall is blocking port 8000
3. Try disabling any VPN on either device
4. Use the exact Network URL shown in the terminal

### Performance Issues

For better performance:
- Close unnecessary applications to free up RAM
- Consider using a machine with GPU support
- Reduce max response length in settings

## 🎯 Model Information

This chat interface uses the **unsloth/Llama-3.2-1B-bnb-4bit** model:
- **Size**: ~1 billion parameters
- **Quantization**: 4-bit using BitsAndBytes
- **Memory Usage**: ~2-3GB RAM
- **Speed**: Fast inference on modern CPUs

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: The first time you run the application, it will download the model from Hugging Face (approximately 1-2GB). Subsequent runs will use the cached model and start much faster.