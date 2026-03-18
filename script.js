// Expanded Vocabulary Setup (Malayalam)
const vocabulary = [
    { id: 'i', word: 'ഞാൻ', emoji: '🧑', type: 'pronoun' },
    { id: 'you', word: 'നിങ്ങൾ', emoji: '👉', type: 'pronoun' },
    { id: 'want', word: 'വേണം', emoji: '🤲', type: 'verb' },
    { id: 'like', word: 'ഇഷ്ടമാണ്', emoji: '❤️', type: 'verb' },
    { id: 'more', word: 'കൂടുതൽ', emoji: '➕', type: 'adjective' },
    { id: 'finished', word: 'കഴിഞ്ഞു', emoji: '✅', type: 'adjective' },
    { id: 'stop', word: 'നിർത്തുക', emoji: '🛑', type: 'verb' },
    { id: 'go', word: 'പോകുക', emoji: '🟢', type: 'verb' },
    { id: 'help', word: 'സഹായിക്കുക', emoji: '🤝', type: 'verb' },
    { id: 'eat', word: 'കഴിക്കുക', emoji: '🍎', type: 'verb' },
    { id: 'drink', word: 'കുടിക്കുക', emoji: '🚰', type: 'verb' },
    { id: 'play', word: 'കളിക്കുക', emoji: '⚽', type: 'verb' },
    { id: 'sleep', word: 'ഉറങ്ങുക', emoji: '🛏️', type: 'verb' },
    { id: 'bathroom', word: 'ബാത്ത്റൂം', emoji: '🚽', type: 'noun' },
    { id: 'food', word: 'ഭക്ഷണം', emoji: '🍔', type: 'noun' },
    { id: 'water', word: 'വെള്ളം', emoji: '💧', type: 'noun' },
    { id: 'home', word: 'വീട്', emoji: '🏠', type: 'noun' },
    { id: 'yes', word: 'അതെ', emoji: '👍', type: 'adjective' },
    { id: 'no', word: 'ഇല്ല', emoji: '👎', type: 'adjective' },
    { id: 'happy', word: 'സന്തോഷം', emoji: '😄', type: 'adjective' },
    { id: 'sad', word: 'സങ്കടം', emoji: '😢', type: 'adjective' },
    { id: 'angry', word: 'ദേഷ്യം', emoji: '😠', type: 'adjective' }
];

// State
let currentSentence = [];
let currentFilter = 'all';

// DOM Elements
const gridContainer = document.getElementById('word-grid');
const speechBar = document.getElementById('speech-bar');
const speakBtn = document.getElementById('speak-btn');
const clearBtn = document.getElementById('clear-btn');
const filterBtns = document.querySelectorAll('.filter-btn');

// Initialize Synthesis
const synth = window.speechSynthesis;

// Functions
function renderGrid() {
    gridContainer.innerHTML = '';

    vocabulary.forEach(item => {
        const card = document.createElement('div');
        // Include filter logic
        const isHidden = currentFilter !== 'all' && item.type !== currentFilter;
        card.className = `word-card ${item.type} ${isHidden ? 'hidden' : ''}`;
        card.id = `card-${item.id}`;

        card.innerHTML = `
            <div class="card-image-container">
                <span class="card-emoji">${item.emoji}</span>
            </div>
            <div class="card-text">${item.word}</div>
        `;

        card.addEventListener('click', () => handleWordClick(item, card));
        gridContainer.appendChild(card);
    });
}

function handleWordClick(item, cardElement) {
    // Add visual feedback class
    cardElement.classList.add('playing');
    setTimeout(() => {
        cardElement.classList.remove('playing');
    }, 500);

    // Play individual word out loud
    speakText(item.word);

    // Add to current sentence
    currentSentence.push(item);
    renderSpeechBar();
}

function renderSpeechBar() {
    speechBar.innerHTML = '';

    currentSentence.forEach(item => {
        const chip = document.createElement('div');
        chip.className = 'word-chip';
        chip.textContent = item.word;
        speechBar.appendChild(chip);
    });
}

function speakText(text) {
    if (synth.speaking) {
        // Optional Cancel to make it snappy
        synth.cancel();
    }

    if (text !== '') {
        const utterThis = new SpeechSynthesisUtterance(text);

        // Attempt to find a Malayalam voice, fallback to Hindi or default Google voice
        const voices = synth.getVoices();
        const preferredVoice = voices.find(v => v.lang.includes('ml-IN')) ||
            voices.find(v => v.name.includes('Malayalam')) ||
            voices.find(v => v.lang.includes('hi-IN')) ||
            voices.find(v => v.name.includes('Google'));
        if (preferredVoice) {
            utterThis.voice = preferredVoice;
        }

        utterThis.lang = 'ml-IN'; // Force malayalam locale
        utterThis.pitch = 1.2; // Slightly higher/friendly pitch
        utterThis.rate = 0.9;

        synth.speak(utterThis);
    }
}

function speakSentence() {
    if (currentSentence.length === 0) return;

    // Visual feedback on speech bar
    speechBar.classList.add('speaking');

    const sentenceText = currentSentence.map(item => item.word).join(' ');
    speakText(sentenceText);

    // Remove speaking decoration based on approx time it takes to speak
    const msgDuration = Math.max(1000, sentenceText.length * 90);
    setTimeout(() => {
        speechBar.classList.remove('speaking');
    }, msgDuration);
}

function clearSentence() {
    currentSentence = [];
    renderSpeechBar();
}

function handleFilterClick(e) {
    // Update active button styling
    filterBtns.forEach(btn => btn.classList.remove('active'));
    e.target.classList.add('active');

    // Get filter and re-render grid
    currentFilter = e.target.getAttribute('data-filter');
    renderGrid();
}

// Event Listeners
speakBtn.addEventListener('click', speakSentence);
clearBtn.addEventListener('click', clearSentence);
filterBtns.forEach(btn => btn.addEventListener('click', handleFilterClick));

// Optional: Deal with voices loading asynchronously in some browsers
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => synth.getVoices();
}

// Initialize App
renderGrid();
