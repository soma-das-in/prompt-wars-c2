/**
 * VoteAssist Frontend Application
 * Handles chat interactions, voice assistance, and eligibility checks.
 */
'use strict';

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const loadingIndicator = document.getElementById('loading-indicator');
    const faqButtonsContainer = document.getElementById('faq-buttons');
    const eligibilityForm = document.getElementById('eligibility-form');
    const eligibilityResult = document.getElementById('eligibility-result');
    const micBtn = document.getElementById('mic-btn');
    const ttsAudio = document.getElementById('tts-audio');

    // --- State & Config ---
    let speechRecognition;

    /**
     * App Initialization
     */
    const init = () => {
        loadFAQs();
        setupSpeechRecognition();
        attachEventListeners();
    };

    /**
     * Fetches suggested questions from the backend
     */
    async function loadFAQs() {
        try {
            const response = await fetch('/api/static-content');
            const data = await response.json();
            
            faqButtonsContainer.innerHTML = '';
            const faqs = (data.faqs && data.faqs.length > 0) 
                ? data.faqs.map(f => f.question)
                : ["How to register?", "Am I eligible?", "When is the election?"];

            faqs.forEach(text => {
                const btn = document.createElement('button');
                btn.className = 'suggested-btn';
                btn.textContent = text;
                btn.addEventListener('click', () => {
                    chatInput.value = text;
                    handleChatSubmit();
                });
                faqButtonsContainer.appendChild(btn);
            });
        } catch (err) {
            console.error("Failed to load FAQs:", err);
        }
    }

    /**
     * Initializes browser-native Speech Recognition
     */
    function setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            micBtn.classList.add('hidden');
            return;
        }

        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = false;
        speechRecognition.lang = 'en-IN';

        speechRecognition.onstart = () => micBtn.classList.add('recording');
        speechRecognition.onend = () => micBtn.classList.remove('recording');
        speechRecognition.onresult = (event) => {
            chatInput.value = event.results[0][0].transcript;
            handleChatSubmit();
        };
        speechRecognition.onerror = (err) => {
            console.error("Speech recognition error:", err.error);
            micBtn.classList.remove('recording');
        };
    }

    /**
     * Handles Text-to-Speech playback
     */
    async function playTTS(text) {
        try {
            const response = await fetch('/api/tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                ttsAudio.src = URL.createObjectURL(blob);
                ttsAudio.play();
            }
        } catch (err) {
            console.error("TTS playback failed:", err);
        }
    }

    /**
     * Formats assistant message (markdown-like bold and lists)
     */
    function formatMessage(text) {
        const escapeHTML = (str) => {
            const p = document.createElement('p');
            p.textContent = str;
            return p.innerHTML;
        };

        let formatted = escapeHTML(text);
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

        const lines = formatted.split('\n');
        let htmlResult = '';
        let listType = null; // 'ul' or 'ol'

        const closeList = () => {
            if (listType) {
                htmlResult += `</${listType}>`;
                listType = null;
            }
        };

        lines.forEach(line => {
            const trimmed = line.trim();
            if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
                if (listType !== 'ul') { closeList(); htmlResult += '<ul>'; listType = 'ul'; }
                htmlResult += `<li>${trimmed.substring(2)}</li>`;
            } else if (trimmed.match(/^\d+\.\s/)) {
                if (listType !== 'ol') { closeList(); htmlResult += '<ol>'; listType = 'ol'; }
                htmlResult += `<li>${trimmed.replace(/^\d+\.\s/, '')}</li>`;
            } else {
                closeList();
                if (trimmed) htmlResult += `<p>${trimmed}</p>`;
            }
        });
        closeList();
        return htmlResult;
    }

    /**
     * Appends a message to the chat window
     */
    function appendMessage(text, isUser) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
        
        if (isUser) {
            msgDiv.textContent = text;
        } else {
            msgDiv.innerHTML = formatMessage(text);
        }
        
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    /**
     * Handles the chat form submission
     */
    async function handleChatSubmit(e) {
        if (e) e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage(message, true);
        chatInput.value = '';
        loadingIndicator.classList.remove('hidden');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            if (!response.ok) throw new Error("Server Error");

            const data = await response.json();
            appendMessage(data.reply, false);
            
            // Clean markdown for TTS
            playTTS(data.reply.replace(/\*\*/g, ''));
            
        } catch (error) {
            appendMessage("Sorry, I encountered an error. Please try again later.", false);
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    }

    /**
     * Attaches all event listeners
     */
    function attachEventListeners() {
        chatForm.addEventListener('submit', handleChatSubmit);

        micBtn.addEventListener('click', () => {
            if (!speechRecognition) return;
            if (micBtn.classList.contains('recording')) {
                speechRecognition.stop();
            } else {
                speechRecognition.start();
            }
        });

        eligibilityForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const age = parseInt(document.getElementById('age').value, 10);
            const isCitizen = document.getElementById('citizen').checked;

            try {
                const response = await fetch('/api/eligibility', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ age, is_citizen: isCitizen })
                });
                const data = await response.json();
                
                eligibilityResult.textContent = data.message;
                eligibilityResult.className = `result-display ${data.status === 'eligible' ? 'result-eligible' : 'result-ineligible'}`;
                eligibilityResult.classList.remove('hidden');
            } catch (error) {
                eligibilityResult.textContent = "Error checking eligibility. Please try again.";
                eligibilityResult.className = 'result-display result-ineligible';
                eligibilityResult.classList.remove('hidden');
            }
        });
    }

    // Run Init
    init();
});
