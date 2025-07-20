// static/script.js
function copyText() {
    const text = document.getElementById('translated-text').innerText;
    if (text && text !== '') {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Text copied to clipboard!', 'success');
        });
    }
}

function speakText() {
    const text = document.getElementById('translated-text').innerText;
    if (text && text !== '') {
        const utterance = new SpeechSynthesisUtterance(text);
        const targetLang = document.getElementById('target').value;
        utterance.lang = targetLang;
        speechSynthesis.speak(utterance);
        showNotification('Reading text aloud...', 'info');
    }
}

function swapLanguages() {
    const source = document.getElementById('source');
    const target = document.getElementById('target');
    const temp = source.value;
    source.value = target.value;
    target.value = temp;
    
    // Add visual feedback
    const swapBtn = document.querySelector('.swap-btn');
    swapBtn.style.transform = 'scale(1.1) rotate(180deg)';
    setTimeout(() => {
        swapBtn.style.transform = '';
    }, 300);
}

function clearAll() {
    document.getElementById('text').value = '';
    document.getElementById('translated-text').innerText = '';
    showNotification('Content cleared', 'info');
}

function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Set background color based on type
    const colors = {
        success: '#48bb78',
        error: '#f56565',
        info: '#4299e1'
    };
    notification.style.background = colors[type] || colors.success;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Add loading animation to translate button
function addLoadingToTranslateButton() {
    const form = document.getElementById('translateForm');
    const translateBtn = document.querySelector('.translate-btn');
    
    if (form && translateBtn) {
        form.addEventListener('submit', function() {
            translateBtn.classList.add('loading');
            translateBtn.textContent = 'Translating...';
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    addLoadingToTranslateButton();
    
    // Auto-translate on language change
    const sourceSelect = document.getElementById('source');
    const targetSelect = document.getElementById('target');
    const textArea = document.getElementById('text');
    const form = document.getElementById('translateForm');
    
    if (sourceSelect && targetSelect && textArea && form) {
        sourceSelect.addEventListener('change', function() {
            if (textArea.value.trim()) {
                form.submit();
            }
        });

        targetSelect.addEventListener('change', function() {
            if (textArea.value.trim()) {
                form.submit();
            }
        });
    }
});
