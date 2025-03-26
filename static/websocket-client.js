class SDLAgentChatClient {
    constructor(websocketUrl = 'ws://localhost:8765') {
        this.websocketUrl = websocketUrl;
        this.ws = null;
        this.connected = false;
        this.messageCallbacks = {
            'init': [],
            'agent_message': [],
            'human_input_request': [],
            'human_input_received': [],
            'chat_update': [],
            'status': [],
            'file_uploaded': [],
            'pong': []
        };
        this.connectionCallbacks = {
            'open': [],
            'close': [],
            'error': []
        };
        
        // Reconnection settings
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000; // 3 seconds initial delay
        
        // Keep alive settings
        this.pingInterval = 30000; // 30 seconds
        this.pingIntervalId = null;
    }
    
    // Connect to the WebSocket server
    connect() {
        this.ws = new WebSocket(this.websocketUrl);
        
        this.ws.addEventListener('open', (event) => {
            console.log(`Connected to WebSocket server at ${this.websocketUrl}`);
            this.connected = true;
            this.reconnectAttempts = 0;
            
            // Start keep-alive pings
            this.startPingInterval();
            
            // Call all registered open callbacks
            this.connectionCallbacks['open'].forEach(callback => callback(event));
        });
        
        this.ws.addEventListener('message', (event) => {
            try {
                const data = JSON.parse(event.data);
                const messageType = data.type || 'unknown';
                
                // Log received messages
                console.log(`Received message of type: ${messageType}`, data);
                
                // Call all registered callbacks for this message type
                if (this.messageCallbacks[messageType]) {
                    this.messageCallbacks[messageType].forEach(callback => callback(data));
                }
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        });
        
        this.ws.addEventListener('close', (event) => {
            console.log('Disconnected from WebSocket server');
            this.connected = false;
            
            // Stop ping interval
            this.stopPingInterval();
            
            // Call all registered close callbacks
            this.connectionCallbacks['close'].forEach(callback => callback(event));
            
            // Attempt to reconnect
            this.attemptReconnect();
        });
        
        this.ws.addEventListener('error', (event) => {
            console.error('WebSocket error:', event);
            
            // Call all registered error callbacks
            this.connectionCallbacks['error'].forEach(callback => callback(event));
        });
    }
    
    // Attempt to reconnect to the WebSocket server
    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.log('Maximum reconnection attempts reached. Giving up.');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);
        
        console.log(`Attempting to reconnect in ${delay/1000} seconds... (Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        
        setTimeout(() => {
            console.log('Reconnecting...');
            this.connect();
        }, delay);
    }
    
    // Start keep-alive ping interval
    startPingInterval() {
        this.stopPingInterval(); // Clear any existing interval
        
        this.pingIntervalId = setInterval(() => {
            if (this.connected && this.ws.readyState === WebSocket.OPEN) {
                this.send('ping', {});
            }
        }, this.pingInterval);
    }
    
    // Stop keep-alive ping interval
    stopPingInterval() {
        if (this.pingIntervalId) {
            clearInterval(this.pingIntervalId);
            this.pingIntervalId = null;
        }
    }
    
    // Send a message to the WebSocket server
    send(type, data = {}) {
        if (!this.connected || this.ws.readyState !== WebSocket.OPEN) {
            console.error('Cannot send message, WebSocket is not connected');
            return false;
        }
        
        const message = {
            type: type,
            ...data
        };
        
        try {
            this.ws.send(JSON.stringify(message));
            return true;
        } catch (error) {
            console.error('Error sending WebSocket message:', error);
            return false;
        }
    }
    
    // Send a user message
    sendUserMessage(content) {
        return this.send('user_message', { content });
    }
    
    // Send a response to a human input request
    sendHumanInputResponse(response) {
        return this.send('human_input_response', { response });
    }
    
    // Register a callback for a specific message type
    onMessage(type, callback) {
        if (!this.messageCallbacks[type]) {
            this.messageCallbacks[type] = [];
        }
        
        this.messageCallbacks[type].push(callback);
    }
    
    // Register a callback for connection events
    onConnection(event, callback) {
        if (!this.connectionCallbacks[event]) {
            this.connectionCallbacks[event] = [];
        }
        
        this.connectionCallbacks[event].push(callback);
    }
    
    // Disconnect from the WebSocket server
    disconnect() {
        if (this.connected && this.ws) {
            this.ws.close();
        }
        
        this.stopPingInterval();
    }
}

// Export the client class
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = SDLAgentChatClient;
} else {
    window.SDLAgentChatClient = SDLAgentChatClient;
}

// Example usage with default DOM elements
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're in a page with the expected elements
    const chatContainer = document.getElementById('chat-container');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const statusElement = document.getElementById('status');
    
    if (chatContainer && messageInput && sendButton && statusElement) {
        // Initialize the client
        const client = new SDLAgentChatClient('ws://localhost:8765');
        
        // Update status on connection events
        client.onConnection('open', () => {
            statusElement.textContent = 'Connected';
            statusElement.className = 'status-connected';
        });
        
        client.onConnection('close', () => {
            statusElement.textContent = 'Disconnected';
            statusElement.className = 'status-disconnected';
        });
        
        client.onConnection('error', () => {
            statusElement.textContent = 'Error';
            statusElement.className = 'status-error';
        });
        
        // Handle incoming messages
        client.onMessage('chat_update', (data) => {
            // Clear the chat container
            chatContainer.innerHTML = '';
            
            // Add each message to the chat
            data.history.forEach(([user, agent]) => {
                const userDiv = document.createElement('div');
                userDiv.className = 'user-message';
                userDiv.textContent = user;
                
                const agentDiv = document.createElement('div');
                agentDiv.className = 'agent-message';
                agentDiv.textContent = agent;
                
                chatContainer.appendChild(userDiv);
                chatContainer.appendChild(agentDiv);
            });
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        });
        
        // Handle human input requests
        client.onMessage('human_input_request', (data) => {
            messageInput.placeholder = `Reply to: ${data.prompt}`;
            messageInput.focus();
        });
        
        // Send message when button is clicked
        sendButton.addEventListener('click', () => {
            const message = messageInput.value.trim();
            if (message) {
                client.sendUserMessage(message);
                messageInput.value = '';
            }
        });
        
        // Send message when Enter is pressed
        messageInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendButton.click();
            }
        });
        
        // Connect to the server
        client.connect();
    }
});