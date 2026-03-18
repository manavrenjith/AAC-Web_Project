// State
let currentSentence = [];
let currentTypedWord = "";

// DOM Elements
const speechBar = document.getElementById('speech-bar');
const speakBtn = document.getElementById('speak-btn');
const clearBtn = document.getElementById('clear-btn');
const wordCards = document.querySelectorAll('.word-card');

// Keyboard Elements
const toggleGridBtn = document.getElementById('toggle-grid-btn');
const toggleKbBtn = document.getElementById('toggle-kb-btn');
const wordGrid = document.getElementById('word-grid');
const keyboardContainer = document.getElementById('keyboard-container');
const kbKeys = document.querySelectorAll('.kb-key');

// Native fallback if needed, but ResponsiveVoice is primary
const synth = window.speechSynthesis;

// Event Listeners for Grid
wordCards.forEach(card => {
    card.addEventListener('click', () => {
        const word = card.getAttribute('data-word');
        const englishWord = card.getAttribute('data-en');

        // Visual feedback
        card.classList.add('playing');
        setTimeout(() => card.classList.remove('playing'), 600);

        // Play individual word in Malayalam
        speakText(word, 'ml-IN');

        // Add to sentence
        currentSentence.push(word);
        renderSpeechBar();
    });
});

function renderSpeechBar() {
    if (!speechBar) return;

    speechBar.innerHTML = '';

    currentSentence.forEach(word => {
        const chip = document.createElement('div');
        chip.className = 'word-chip';
        chip.textContent = word;
        speechBar.appendChild(chip);
    });

    if (currentTypedWord) {
        const typeChip = document.createElement('div');
        typeChip.className = 'word-chip typing-chip';
        typeChip.textContent = currentTypedWord;
        speechBar.appendChild(typeChip);
    }
}

function speakText(text, lang='ml-IN') {
    if (text !== '') {
        // Cancel any existing native speech just in case
        if (synth && synth.speaking) synth.cancel();
        if (window.responsiveVoice && responsiveVoice.isPlaying()) responsiveVoice.cancel();

        // Use our robust backend proxy for guaranteed Google TTS
        // Pass language along if it's english
        let ttsUrl = '/tts?text=' + encodeURIComponent(text);
        if (lang === 'en-US') {
            ttsUrl += '&lang=en';
        }

        const audio = new Audio(ttsUrl);

        audio.play().catch(e => {
            console.warn("Backend Proxy TTS failed, falling back to native browser synthesis", e);

            // Native fallback as last resort
            const utterThis = new SpeechSynthesisUtterance(text);
            utterThis.lang = lang;

            const voices = synth.getVoices();
            const preferredVoice = voices.find(v => v.lang.includes(lang.split('-')[0]) || v.name.toLowerCase().includes(lang === 'en-US' ? 'english' : 'malayalam'));
            if (preferredVoice) {
                utterThis.voice = preferredVoice;
            }

            utterThis.pitch = 1.2;
            utterThis.rate = 0.9;

            synth.speak(utterThis);
        });
    }
}

function speakSentence() {
    let wordsToSpeak = [...currentSentence];
    if (currentTypedWord) {
        wordsToSpeak.push(currentTypedWord);
    }

    if (wordsToSpeak.length === 0) return;

    const sentenceText = wordsToSpeak.join(' ');
    // We will just speak the whole sentence using the default language context.
    // If it's a mix, ml-IN usually handles english words okay, or we can just send it raw.
    speakText(sentenceText, 'ml-IN');
}

function speakSentenceText(text) {
    speakText(text, 'ml-IN');
}

// Ensure the new dynamic category items can universally trigger TTS
window.speakWord = function(word) {
    // Try the robust fallback speakText first if it works well for the existing board, 
    // or just use SpeechSynthesis as requested. We'll use the browser synthesize API directly here.
    if (!word) return;
    try {
        let speech = new SpeechSynthesisUtterance(word);
        speech.lang = 'ml-IN'; // Default to Malayalam, handles English ok
        window.speechSynthesis.speak(speech);
    } catch (e) {
        console.error("speech error:", e);
    }
}

function clearSentence() {
    currentSentence = [];
    currentTypedWord = "";
    renderSpeechBar();
}

// Hook up buttons if they exist on the page
if (speakBtn) speakBtn.addEventListener('click', speakSentence);
if (clearBtn) clearBtn.addEventListener('click', clearSentence);

// Load voices async properly
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => synth.getVoices();
}

// View Toggling Logic
if (toggleGridBtn && toggleKbBtn) {
    toggleGridBtn.addEventListener('click', () => {
        wordGrid.style.display = 'grid';
        keyboardContainer.style.display = 'none';

        toggleGridBtn.style.background = 'var(--primary)';
        toggleGridBtn.style.color = 'white';
        toggleGridBtn.style.borderColor = 'var(--primary)';

        toggleKbBtn.style.background = 'white';
        toggleKbBtn.style.color = 'var(--text-main)';
        toggleKbBtn.style.borderColor = '#cbd5e1';
    });

    toggleKbBtn.addEventListener('click', () => {
        wordGrid.style.display = 'none';
        keyboardContainer.style.display = 'block';

        toggleKbBtn.style.background = 'var(--primary)';
        toggleKbBtn.style.color = 'white';
        toggleKbBtn.style.borderColor = 'var(--primary)';

        toggleGridBtn.style.background = 'white';
        toggleGridBtn.style.color = 'var(--text-main)';
        toggleGridBtn.style.borderColor = '#cbd5e1';
    });
}

// Digital Keyboard Logic (Sentence Builder)
kbKeys.forEach(btn => {
    btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-key');

        if (key === 'BACKSPACE') {
            if (currentTypedWord.length > 0) {
                currentTypedWord = currentTypedWord.slice(0, -1);
            } else if (currentSentence.length > 0) {
                currentSentence.pop(); // Remove last word
            }
        } else if (key === 'SPACE') {
            if (currentTypedWord.length > 0) {
                currentSentence.push(currentTypedWord);
                currentTypedWord = "";
            }
        } else {
            currentTypedWord += key;
        }

        renderSpeechBar();
    });
});

// Digital Keyboard Logic (Standalone TTS Page)
document.addEventListener('DOMContentLoaded', () => {
    const ttsKbKeys = document.querySelectorAll('.tts-kb-key');
    const ttsInput = document.getElementById('ttsInput');
    
    if(ttsKbKeys.length > 0 && ttsInput) {
        ttsKbKeys.forEach(btn => {
            // Apply standard keyboard styles dynamically if needed, 
            // but relying on existing CSS classes for now
            btn.classList.add('kb-key');
            
            btn.addEventListener('click', () => {
                const key = btn.getAttribute('data-key');
                let currentVal = ttsInput.value;
                
                if (key === 'BACKSPACE') {
                    if (currentVal.length > 0) {
                        ttsInput.value = currentVal.slice(0, -1);
                    }
                } else if (key === 'SPACE') {
                    ttsInput.value = currentVal + " ";
                } else {
                    ttsInput.value = currentVal + key;
                }
                
                ttsInput.focus();
            });
        });
    }
});

// Category Filtering Logic
window.filterCategory = function(category) {
    // Reveal grid if hidden by default
    const wordGrid = document.getElementById('word-grid');
    if (wordGrid) {
        wordGrid.style.display = 'grid';
    }

    const cards = document.querySelectorAll('.word-card');
    cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });

    // Close dropdown instantly when clicked
    const dropdownMenu = document.querySelector('.dropdown-menu');
    if(dropdownMenu) {
        dropdownMenu.style.display = 'none';
        setTimeout(() => dropdownMenu.style.display = '', 100);
    }
    
    // Switch to Grid view automatically if not already
    const toggleGridBtn = document.getElementById('toggle-grid-btn');
    if (toggleGridBtn) {
        toggleGridBtn.click();
    }
    
    // Close the sidebar menu if it's open
    const sidebarNav = document.getElementById('sidebar-nav');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    if (sidebarNav && sidebarNav.classList.contains('active')) {
        sidebarNav.classList.remove('active');
        if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    }
};

// Hamburger Sidebar Menu Logic
window.toggleMobileMenu = function() {
    const sidebarNav = document.getElementById('sidebar-nav');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    if (sidebarNav && sidebarOverlay) {
        sidebarNav.classList.toggle('active');
        sidebarOverlay.classList.toggle('active');
    }
};

// Search Logic for Home Page
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('symbol-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();
            const cards = document.querySelectorAll('.word-card');
            
            // Show grid when searching
            const wordGrid = document.getElementById('word-grid');
            if (wordGrid && searchTerm.length > 0) {
                wordGrid.style.display = 'grid';
            }
            
            cards.forEach(card => {
                const word = card.getAttribute('data-word').toLowerCase();
                if (word.includes(searchTerm)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});

// Edit Modal Logic for View Uploaded Content Page
window.openEditModal = function(id, word, category) {
    const modal = document.getElementById('edit-modal');
    if (!modal) return;
    
    // Set form action dynamically
    const form = document.getElementById('edit-form');
    // Using a relative path for the edit route
    form.action = `/caregiver/edit_icon/${id}`;
    
    // Fill the inputs
    document.getElementById('edit_word').value = word;
    
    const categorySelect = document.getElementById('edit_category');
    if(categorySelect) {
        for(let i=0; i<categorySelect.options.length; i++) {
            if(categorySelect.options[i].value === category) {
                categorySelect.selectedIndex = i;
                break;
            }
        }
    }
    
    // Show modal
    modal.classList.add('active');
};

window.closeEditModal = function() {
    const modal = document.getElementById('edit-modal');
    if (modal) {
        modal.classList.remove('active');
    }
};

// Close modal when clicking outside of it
document.addEventListener('click', (e) => {
    const modal = document.getElementById('edit-modal');
    if (modal && modal.classList.contains('active')) {
        const content = modal.querySelector('.modal-content');
        if (e.target === modal && !content.contains(e.target)) {
            closeEditModal();
        }
    }
});

// Text to Speech Functions
function speakTTSConverterText(){
    var text = document.getElementById("ttsInput").value;
    if (!text) return;
    speakText(text, 'ml-IN');
}

function clearTTSConverterText(){
    document.getElementById("ttsInput").value = "";
}

// Speech to Text Functions
function startRecognition() {
    const micBtn = document.getElementById("micBtn");
    
    // Check if browser supports speech recognition
    const defaultSpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!defaultSpeechRecognition) {
        alert("Your browser does not support Speech Recognition. Try using Google Chrome.");
        return;
    }

    const recognition = new defaultSpeechRecognition();
    recognition.lang = "ml-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function() {
        micBtn.classList.add("recording");
        micBtn.innerHTML = "🎙️ Listening...";
        document.getElementById("speechText").value = "";
    };

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("speechText").value = transcript;
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
        alert("Error recognizing speech: " + event.error);
    };

    recognition.onend = function() {
        micBtn.classList.remove("recording");
        micBtn.innerHTML = "🎤 Start Speaking";
    };

    recognition.start();
}

function speakRecognizedText() {
    var text = document.getElementById("speechText").value;
    if (!text) return;
    speakText(text, 'ml-IN');
}

function clearRecognizedText() {
    document.getElementById("speechText").value = "";
}


