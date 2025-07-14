from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import logging
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for model and tokenizer
model = None
tokenizer = None
model_loading = False
model_loaded = False

def load_model():
    """Load the model in a separate thread"""
    global model, tokenizer, model_loading, model_loaded
    
    try:
        model_loading = True
        logger.info("Loading model: unsloth/Llama-3.2-1B-bnb-4bit")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-1B-bnb-4bit")
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model with 4-bit quantization
        model = AutoModelForCausalLM.from_pretrained(
            "unsloth/Llama-3.2-1B-bnb-4bit",
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True,
            trust_remote_code=True
        )
        
        model_loaded = True
        model_loading = False
        logger.info("Model loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        model_loading = False
        model_loaded = False

@app.route('/')
def index():
    """Serve the chat interface"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Check if model is loaded"""
    return jsonify({
        'model_loaded': model_loaded,
        'model_loading': model_loading
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    global model, tokenizer
    
    if not model_loaded:
        return jsonify({'error': 'Model not loaded yet. Please wait.'}), 503
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get conversation history
        conversation_history = data.get('history', [])
        
        # Build the prompt with conversation history
        prompt = ""
        for msg in conversation_history[-5:]:  # Keep last 5 exchanges
            if msg['role'] == 'user':
                prompt += f"User: {msg['content']}\n"
            else:
                prompt += f"Assistant: {msg['content']}\n"
        
        prompt += f"User: {user_message}\nAssistant:"
        
        # Tokenize input
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the new response
        response = full_response[len(prompt):].strip()
        
        # Remove any remaining "User:" or "Assistant:" prefixes
        if response.startswith("User:") or response.startswith("Assistant:"):
            response = response.split(":", 1)[1].strip()
        
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({'error': f'Error generating response: {str(e)}'}), 500

if __name__ == '__main__':
    # Start model loading in background
    threading.Thread(target=load_model, daemon=True).start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)