'use strict';

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const loadingIndicator = document.getElementById('loading-indicator');
    const faqButtonsContainer = document.getElementById('faq-buttons');
    const eligibilityForm = document.getElementById('eligibility-form');
    const eligibilityResult = document.getElementById('eligibility-result');

    // Fetch static content (FAQs)
    fetch('/api/static-content')
        .then(res => res.json())
        .then(data => {
            if (data.faqs) {
                data.faqs.forEach(faq => {
                    const btn = document.createElement('button');
                    btn.className = 'suggested-btn';
                    btn.textContent = faq.question;
                    btn.addEventListener('click', () => {
                        chatInput.value = faq.question;
                        handleChatSubmit(new Event('submit'));
                    });
                    faqButtonsContainer.appendChild(btn);
                });
            }
        })
        .catch(err => console.error("Failed to load FAQs", err));

    function formatMessage(text) {
        // Escaping HTML to prevent XSS
        const escapeHTML = (str) => {
            const p = document.createElement('p');
            p.textContent = str;
            return p.innerHTML;
        };

        let formatted = escapeHTML(text);

        // Bold: **text** -> <b>text</b>
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

        // Lists: lines starting with * or -
        const lines = formatted.split('\n');
        let inList = false;
        let finalHtml = '';

        lines.forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine.startsWith('* ') || trimmedLine.startsWith('- ')) {
                if (!inList) {
                    finalHtml += '<ul>';
                    inList = true;
                }
                finalHtml += `<li>${trimmedLine.substring(2)}</li>`;
            } else if (trimmedLine.match(/^\d+\.\s/)) {
                // Numbered lists: 1. text
                if (!inList) {
                    finalHtml += '<ol>';
                    inList = true;
                }
                const content = trimmedLine.replace(/^\d+\.\s/, '');
                finalHtml += `<li>${content}</li>`;
            } else {
                if (inList) {
                    finalHtml += formatted.includes('* ') ? '</ul>' : '</ol>';
                    inList = false;
                }
                if (trimmedLine) {
                    finalHtml += `<p>${trimmedLine}</p>`;
                }
            }
        });

        if (inList) {
            finalHtml += formatted.includes('* ') ? '</ul>' : '</ol>';
        }

        return finalHtml;
    }

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
            
            if (!response.ok) {
                throw new Error("API Error");
            }

            const data = await response.json();
            appendMessage(data.reply, false);
        } catch (error) {
            appendMessage("Sorry, I encountered an error connecting to the server. Please try again later.", false);
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    }

    chatForm.addEventListener('submit', handleChatSubmit);

    // Eligibility check
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
            eligibilityResult.className = 'result-display ' + (data.status === 'eligible' ? 'result-eligible' : 'result-ineligible');
            eligibilityResult.classList.remove('hidden');
        } catch (error) {
            eligibilityResult.textContent = "Error checking eligibility. Please try again.";
            eligibilityResult.className = 'result-display result-ineligible';
            eligibilityResult.classList.remove('hidden');
        }
    });
});
