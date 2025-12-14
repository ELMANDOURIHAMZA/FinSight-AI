// Chatbot Widget JavaScript

let chatbotOpen = false;
let isLoading = false;

function toggleChatbot() {
    const window = document.getElementById('chatbot-window');
    const button = document.getElementById('chatbot-button');
    
    chatbotOpen = !chatbotOpen;
    
    if (chatbotOpen) {
        window.style.display = 'flex';
        button.classList.add('active');
        // Focus on input when opening
        setTimeout(() => {
            document.getElementById('chatbot-input').focus();
        }, 100);
    } else {
        window.style.display = 'none';
        button.classList.remove('active');
    }
}

function useExample(question) {
    const input = document.getElementById('chatbot-input');
    input.value = question;
    input.style.height = 'auto';
    input.style.height = input.scrollHeight + 'px';
    input.focus();
}

function handleChatbotKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendChatbotMessage();
    } else {
        // Auto-resize textarea
        const input = event.target;
        input.style.height = 'auto';
        input.style.height = input.scrollHeight + 'px';
    }
}

async function sendChatbotMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    // Get ticker from session or input
    const ticker = await getCurrentTicker();
    if (!ticker) {
        addChatbotMessage('Veuillez d\'abord sélectionner un symbole boursier dans la sidebar et lancer l\'analyse.', 'error');
        return;
    }
    
    // Add user message to chat
    addChatbotMessage(message, 'user');
    input.value = '';
    input.style.height = 'auto';
    
    // Show loading indicator
    isLoading = true;
    const loadingId = addChatbotLoadingMessage();
    
    // Disable send button
    const sendBtn = document.getElementById('chatbot-send');
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    
    try {
        const response = await fetch('/api/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                ticker: ticker
            })
        });
        
        const data = await response.json();
        
        // Remove loading message
        removeChatbotLoadingMessage(loadingId);
        
        if (data.error) {
            // Show user-friendly error message
            addChatbotMessage(data.response || data.error || 'Une erreur est survenue', 'error');
        } else {
            addChatbotMessage(data.response, 'assistant');
        }
    } catch (error) {
        removeChatbotLoadingMessage(loadingId);
        addChatbotMessage('Erreur de connexion: ' + error.message + '. Vérifiez votre connexion Internet.', 'error');
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        sendBtn.classList.remove('loading');
    }
}

function addChatbotMessage(content, type = 'assistant') {
    const messagesContainer = document.getElementById('chatbot-messages');
    
    // Remove welcome message if it exists
    const welcome = messagesContainer.querySelector('.chatbot-welcome');
    if (welcome) {
        welcome.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message chatbot-message-${type}`;
    
    const time = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="chatbot-message-content">
            ${formatChatbotMessage(content)}
        </div>
        <div class="chatbot-message-time">${time}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addChatbotLoadingMessage() {
    const messagesContainer = document.getElementById('chatbot-messages');
    const loadingId = 'loading-' + Date.now();
    
    const messageDiv = document.createElement('div');
    messageDiv.id = loadingId;
    messageDiv.className = 'chatbot-message chatbot-message-assistant chatbot-loading';
    
    messageDiv.innerHTML = `
        <div class="chatbot-message-content">
            <div class="chatbot-typing">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return loadingId;
}

function removeChatbotLoadingMessage(loadingId) {
    const loading = document.getElementById(loadingId);
    if (loading) {
        loading.remove();
    }
}

function formatChatbotMessage(content) {
    // Simple markdown-like formatting
    let formatted = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    return formatted;
}

async function getCurrentTicker() {
    // Try to get ticker from input
    const tickerInput = document.getElementById('ticker-input');
    if (tickerInput && tickerInput.value && tickerInput.value.trim()) {
        return tickerInput.value.toUpperCase().trim();
    }
    
    // Try to get from session via API
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        if (data.ticker) {
            return data.ticker.toUpperCase();
        }
    } catch (error) {
        console.log('Could not fetch ticker from session');
    }
    
    return null; // Return null if no ticker found
}

// Initialize chatbot on page load
document.addEventListener('DOMContentLoaded', function() {
    // Make sure chatbot is closed initially
    const window = document.getElementById('chatbot-window');
    if (window) {
        window.style.display = 'none';
    }
});

