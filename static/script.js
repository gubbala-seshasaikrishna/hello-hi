class ChatApp {
    constructor() {
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.settingsPanel = document.getElementById('settingsPanel');
        
        this.isLoading = false;
        this.messages = [];
        
        this.init();
    }
    
    init() {
        // Auto-resize textarea
        this.messageInput.addEventListener('input', this.autoResize.bind(this));
        
        // Send on Enter (but allow Shift+Enter for new lines)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Handle touch events for better mobile experience
        this.sendButton.addEventListener('touchstart', this.handleTouchStart.bind(this));
        this.sendButton.addEventListener('touchend', this.handleTouchEnd.bind(this));
        
        // Check server status
        this.checkStatus();
        
        // Load saved messages from localStorage
        this.loadMessages();
        
        // Focus input on load
        setTimeout(() => {
            this.messageInput.focus();
        }, 100);
    }
    
    autoResize() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    handleTouchStart(e) {
        e.preventDefault();
        this.sendButton.style.transform = 'scale(0.95)';
    }
    
    handleTouchEnd(e) {
        e.preventDefault();
        this.sendButton.style.transform = 'scale(1)';
        this.sendMessage();
    }
    
    async checkStatus() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.model_loaded) {
                this.statusIndicator.style.background = '#10b981';
                this.statusIndicator.title = 'Model loaded and ready';
            } else {
                this.statusIndicator.style.background = '#f59e0b';
                this.statusIndicator.title = 'Model loading...';
            }
        } catch (error) {
            this.statusIndicator.style.background = '#ef4444';
            this.statusIndicator.title = 'Server disconnected';
            this.showError('Cannot connect to server. Please check if the backend is running.');
        }
    }
    
    async sendMessage() {
        if (this.isLoading) return;
        
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage('user', message);
        this.messageInput.value = '';
        this.autoResize();
        
        // Show loading indicator
        this.showLoading(true);
        
        try {
            const settings = this.getSettings();
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    temperature: settings.temperature,
                    max_length: settings.maxLength,
                    top_p: settings.topP
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('assistant', data.response);
            } else {
                this.showError(data.error || 'Unknown error occurred');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.showError('Failed to get response from the model. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        bubbleDiv.textContent = content;
        
        messageDiv.appendChild(bubbleDiv);
        this.messagesContainer.appendChild(messageDiv);
        
        // Save message
        this.messages.push({ role, content, timestamp: Date.now() });
        this.saveMessages();
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    showLoading(show) {
        this.isLoading = show;
        this.sendButton.disabled = show;
        
        // Remove existing loading indicator
        const existingLoading = this.messagesContainer.querySelector('.loading');
        if (existingLoading) {
            existingLoading.remove();
        }
        
        if (show) {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message assistant';
            loadingDiv.innerHTML = `
                <div class="loading">
                    <div class="loading-dots">
                        <div class="loading-dot"></div>
                        <div class="loading-dot"></div>
                        <div class="loading-dot"></div>
                    </div>
                </div>
            `;
            this.messagesContainer.appendChild(loadingDiv);
            this.scrollToBottom();
        }
    }
    
    showError(message) {
        // Remove existing error
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        this.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    getSettings() {
        return {
            temperature: parseFloat(document.getElementById('temperatureInput').value),
            maxLength: parseInt(document.getElementById('maxLengthInput').value),
            topP: parseFloat(document.getElementById('topPInput').value)
        };
    }
    
    saveMessages() {
        try {
            localStorage.setItem('chatMessages', JSON.stringify(this.messages));
        } catch (error) {
            console.warn('Could not save messages to localStorage:', error);
        }
    }
    
    loadMessages() {
        try {
            const saved = localStorage.getItem('chatMessages');
            if (saved) {
                this.messages = JSON.parse(saved);
                
                // Clear existing messages except the welcome message
                const messagesChildren = Array.from(this.messagesContainer.children);
                messagesChildren.slice(1).forEach(child => child.remove());
                
                // Restore messages
                this.messages.forEach(msg => {
                    this.addMessageWithoutSaving(msg.role, msg.content);
                });
            }
        } catch (error) {
            console.warn('Could not load messages from localStorage:', error);
        }
    }
    
    addMessageWithoutSaving(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        bubbleDiv.textContent = content;
        
        messageDiv.appendChild(bubbleDiv);
        this.messagesContainer.appendChild(messageDiv);
    }
    
    clearChat() {
        // Keep only the welcome message
        const messagesChildren = Array.from(this.messagesContainer.children);
        messagesChildren.slice(1).forEach(child => child.remove());
        
        this.messages = [];
        this.saveMessages();
        
        // Close settings panel
        this.toggleSettings();
    }
    
    toggleSettings() {
        this.settingsPanel.classList.toggle('open');
    }
}

// Global functions for HTML onclick handlers
function sendMessage() {
    window.chatApp.sendMessage();
}

function toggleSettings() {
    window.chatApp.toggleSettings();
}

function clearChat() {
    if (confirm('Are you sure you want to clear all chat history?')) {
        window.chatApp.clearChat();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApp();
});

// Prevent zoom on double-tap for iOS
let lastTouchEnd = 0;
document.addEventListener('touchend', function (event) {
    const now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);

// Handle viewport changes on iOS
function handleViewportChange() {
    const viewport = document.querySelector('meta[name=viewport]');
    if (viewport) {
        viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, user-scalable=no');
    }
}

window.addEventListener('resize', handleViewportChange);
window.addEventListener('orientationchange', handleViewportChange);