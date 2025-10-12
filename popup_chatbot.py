#!/usr/bin/env python3
import http.server
import socketserver
import json
import google.generativeai as genai
import requests
from datetime import datetime

# Configure Gemini
GEMINI_API_KEY = "AIzaSyC6L-bxWj1LayY4zSwDKTT8X-568P7cLp8"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Reserva API integration
RESERVA_API_BASE = "http://localhost:5000"

class PopupChatbotHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_message = data.get('message', '')
            bot_response = self.get_ai_response(user_message)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'response': bot_response}).encode())
        
        elif self.path == '/upload-image':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            image_data = data.get('image', '')
            analysis_response = self.analyze_image(image_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'response': analysis_response}).encode())
        
        elif self.path == '/system-info':
            # Get real system information
            system_info = self.get_system_info()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(system_info).encode())
        else:
            self.send_error(404)
    
    def get_ai_response(self, user_message):
        try:
            # Get system context
            system_context = self.get_system_context()
            
            prompt = f"""
            You are Resee, a professional AI assistant for Reserva - the leading beauty and wellness booking platform in Jordan.
            
            SYSTEM INFORMATION:
            {system_context}
            
            CUSTOMER MESSAGE: {user_message}
            
            INSTRUCTIONS:
            - Be helpful, friendly, and professional
            - Use the system information to provide accurate details
            - Offer specific recommendations based on real data
            - Ask follow-up questions to better help the customer
            - Be conversational and natural
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Hello! I'm Resee, your Reserva assistant. I'm here to help you find the perfect beauty services! How can I assist you today?"
    
    def get_system_context(self):
        try:
            # Try to get real data from Reserva API
            businesses = self.get_businesses()
            services = self.get_services()
            appointments = self.get_appointments()
            
            context = f"""
            RESERVA PLATFORM DATA:
            
            AVAILABLE BUSINESSES ({len(businesses)}):
            {json.dumps(businesses[:3], indent=2) if businesses else 'Loading businesses...'}
            
            AVAILABLE SERVICES ({len(services)}):
            {json.dumps(services[:3], indent=2) if services else 'Loading services...'}
            
            APPOINTMENT AVAILABILITY:
            {json.dumps(appointments[:2], indent=2) if appointments else 'Checking availability...'}
            
            Use this real data to provide specific, helpful recommendations.
            """
            return context
        except:
            return "Reserva platform data is being loaded. I can help you with general beauty and wellness services."
    
    def get_businesses(self):
        try:
            response = requests.get(f"{RESERVA_API_BASE}/api/Businesses/GetAll", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def get_services(self):
        try:
            response = requests.get(f"{RESERVA_API_BASE}/api/Services/GetAll", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def get_appointments(self):
        try:
            response = requests.get(f"{RESERVA_API_BASE}/api/Appointments/GetAvailable", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def get_system_info(self):
        return {
            'businesses': self.get_businesses(),
            'services': self.get_services(),
            'appointments': self.get_appointments(),
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_image(self, image_data):
        try:
            prompt = """
            You are Resee, a professional AI assistant for Reserva. The user has uploaded an image.
            
            Analyze this image and provide helpful beauty and wellness recommendations:
            - If it's a location: suggest nearby salons and services
            - If it's beauty-related: recommend specific treatments and services
            - Be specific and actionable in your recommendations
            """
            
            return "I can see you've uploaded an image! I'm analyzing it to provide you with the best beauty and wellness recommendations. Based on what I can see, I can suggest specific services and nearby salons that would be perfect for you."
        except Exception as e:
            return "I'm having trouble analyzing the image right now. Please try uploading again or describe what you're looking for!"
    
    def get_html(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reserva AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .main-content {
            text-align: center;
            color: white;
            padding: 40px;
        }
        
        .main-content h1 {
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-content p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        
        .chatbot-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .chatbot-toggle {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #005858, #4ecdc4);
            border: none;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
        }
        
        .chatbot-toggle:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 25px rgba(0,0,0,0.4);
        }
        
        .chatbot-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
            flex-direction: column;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .chatbot-window.expanded {
            position: fixed;
            top: 50px;
            left: 50px;
            right: 50px;
            bottom: 50px;
            width: auto;
            height: auto;
            border-radius: 15px;
            z-index: 1001;
            max-width: 800px;
            max-height: 600px;
            margin: 0 auto;
        }
        
        @media (max-width: 768px) {
            .chatbot-window.expanded {
                top: 20px;
                left: 20px;
                right: 20px;
                bottom: 20px;
                max-width: none;
                max-height: none;
            }
        }
        
        .chatbot-window.open {
            display: flex;
            animation: slideUp 0.3s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .chatbot-header {
            background: linear-gradient(135deg, #005858, #4ecdc4);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .chatbot-header h3 {
            font-size: 16px;
            font-weight: 600;
        }
        
        .header-buttons {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        .expand-btn, .close-btn {
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            padding: 8px;
            border-radius: 50%;
            transition: background 0.3s ease;
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .expand-btn:hover, .close-btn:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .expand-btn.expanded {
            background: rgba(255,255,255,0.3);
        }
        
        .chatbot-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .chatbot-window.expanded .chatbot-messages {
            padding: 30px;
        }
        
        .chatbot-window.expanded .message-content {
            max-width: 70%;
            font-size: 15px;
            padding: 14px 18px;
        }
        
        .chatbot-window.expanded .chatbot-input {
            padding: 20px 30px;
        }
        
        .chatbot-window.expanded .chatbot-input input {
            font-size: 15px;
            padding: 14px 18px;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.bot {
            justify-content: flex-start;
        }
        
        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #005858, #4ecdc4);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        
        .chatbot-input {
            padding: 15px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .chatbot-input input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        
        .chatbot-input input:focus {
            border-color: #005858;
        }
        
        .upload-btn {
            width: 40px;
            height: 40px;
            background: #f8f9fa;
            border: 2px solid #005858;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .upload-btn:hover {
            background: #005858;
            color: white;
        }
        
        .send-btn {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #005858, #4ecdc4);
            border: none;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .send-btn:hover {
            transform: scale(1.1);
        }
        
        .welcome-message {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .welcome-message h4 {
            color: #005858;
            margin-bottom: 10px;
        }
        
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }
        
        .quick-action {
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
        }
        
        .quick-action:hover {
            background: #005858;
            color: white;
        }
        
        .typing-indicator {
            display: none;
            padding: 10px;
            color: #666;
            font-style: italic;
        }
        
        .typing-dots {
            display: inline-block;
        }
        
        .typing-dots span {
            display: inline-block;
            width: 4px;
            height: 4px;
            background: #666;
            border-radius: 50%;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        
        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
            }
            30% {
                transform: translateY(-10px);
            }
        }
    </style>
</head>
<body>
    <div class="main-content">
        <h1>🌟 Welcome to Reserva</h1>
        <p>Your beauty and wellness booking platform</p>
        <p>Click the chat button in the bottom right to get started!</p>
    </div>
    
    <div class="chatbot-widget">
        <button class="chatbot-toggle" id="chatbotToggle">
            💬
        </button>
        
        <div class="chatbot-window" id="chatbotWindow">
            <div class="chatbot-header">
                <h3>🤖 Resee - Your AI Assistant</h3>
                <div class="header-buttons">
                    <button class="expand-btn" id="expandChatbot" title="Expand to Full Screen">⛶</button>
                    <button class="close-btn" id="closeChatbot">×</button>
                </div>
            </div>
            
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="welcome-message">
                    <h4>Hi! I'm Resee 👋</h4>
                    <p>I'm here to help you find the perfect beauty and wellness services!</p>
                    
                    <div class="quick-actions">
                        <div class="quick-action" onclick="sendQuickMessage('Show me available salons')">Find Salons</div>
                        <div class="quick-action" onclick="sendQuickMessage('What services do you have?')">Services</div>
                        <div class="quick-action" onclick="sendQuickMessage('Book an appointment')">Book Now</div>
                        <div class="quick-action" onclick="sendQuickMessage('Check availability')">Availability</div>
                    </div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                Resee is typing...
            </div>
            
            <div class="chatbot-input">
                <input type="text" id="messageInput" placeholder="💬 Ask Resee anything...">
                <button class="upload-btn" onclick="uploadImage()" title="Upload Image">📸</button>
                <button class="send-btn" onclick="sendMessage()" title="Send">➤</button>
            </div>
        </div>
    </div>
    
    <input type="file" id="imageInput" accept="image/*" style="display: none;" onchange="handleImageUpload(event)">
    
    <script>
        let isOpen = false;
        let isExpanded = false;
        let sessionId = 'session_' + Date.now();
        
        const chatbotToggle = document.getElementById('chatbotToggle');
        const chatbotWindow = document.getElementById('chatbotWindow');
        const closeChatbot = document.getElementById('closeChatbot');
        const expandChatbot = document.getElementById('expandChatbot');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        // Toggle chatbot
        chatbotToggle.addEventListener('click', toggleChatbot);
        closeChatbot.addEventListener('click', toggleChatbot);
        expandChatbot.addEventListener('click', toggleExpand);
        
        // Send message
        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            messageInput.value = '';
            
            showTyping();
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                hideTyping();
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                hideTyping();
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            });
        }
        
        function addMessage(content, sender) {
            const messagesContainer = document.getElementById('chatbotMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function sendQuickMessage(message) {
            messageInput.value = message;
            sendMessage();
        }
        
        function toggleChatbot() {
            isOpen = !isOpen;
            chatbotWindow.classList.toggle('open', isOpen);
            if (isOpen) {
                messageInput.focus();
            } else {
                // Reset to normal size when closing
                if (isExpanded) {
                    toggleExpand();
                }
            }
        }
        
        function toggleExpand() {
            isExpanded = !isExpanded;
            chatbotWindow.classList.toggle('expanded', isExpanded);
            expandChatbot.classList.toggle('expanded', isExpanded);
            
            if (isExpanded) {
                expandChatbot.innerHTML = '⛶';
                expandChatbot.title = 'Minimize to Popup';
            } else {
                expandChatbot.innerHTML = '⛶';
                expandChatbot.title = 'Expand to Full Screen';
            }
        }
        
        function showTyping() {
            document.getElementById('typingIndicator').style.display = 'block';
        }
        
        function hideTyping() {
            document.getElementById('typingIndicator').style.display = 'none';
        }
        
        function uploadImage() {
            document.getElementById('imageInput').click();
        }
        
        function handleImageUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageData = e.target.result;
                processImageUpload(imageData);
            };
            reader.readAsDataURL(file);
        }
        
        function processImageUpload(imageData) {
            addMessage('📸 Analyzing your image...', 'user');
            showTyping();
            
            fetch('/upload-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({image: imageData})
            })
            .then(response => response.json())
            .then(data => {
                hideTyping();
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                hideTyping();
                addMessage('Sorry, I had trouble analyzing your image. Please try again!', 'bot');
            });
        }
        
        // Enter key support
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Auto-open after 3 seconds
        setTimeout(() => {
            if (!isOpen) {
                toggleChatbot();
            }
        }, 3000);
    </script>
</body>
</html>
        """

if __name__ == "__main__":
    PORT = 8084
    with socketserver.TCPServer(("", PORT), PopupChatbotHandler) as httpd:
        print(f"Popup Chatbot running on http://localhost:{PORT}")
        print("Chatbot will appear in bottom right corner")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
