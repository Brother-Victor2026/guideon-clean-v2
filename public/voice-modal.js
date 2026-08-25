let recognition = null;
let isListening = false;
let isGuideOnSpeaking = false;
let ttsUtterance = null;
let voiceForm = 'Cove';
let lastTranscript = '';
let isSendingMessage = false;

const voiceForms = {
  'Cove': { pitch: 1, rate: 1 },
  'Spruce': { pitch: 0.9, rate: 0.95 },
  'Breeze': { pitch: 1.1, rate: 1.05 },
  'Sol': { pitch: 0.8, rate: 1.1 },
  'Jupiter': { pitch: 1.2, rate: 1 },
  'Ember': { pitch: 1, rate: 0.9 },
  'Maple': { pitch: 0.95, rate: 1.15 },
  'Vale': { pitch: 1.3, rate: 0.85 },
  'Arbor': { pitch: 0.85, rate: 1.2 }
};

function initVoice() {
  if (recognition) return;
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  recognition = new SR();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'fr-FR';
  recognition.maxAlternatives = 1;
  
  recognition.soundstart = () => {};
  recognition.soundend = () => {};
  recognition.audiostart = () => {};
  recognition.audioend = () => {};
  
  recognition.onstart = () => {
    isListening = true;
    lastTranscript = '';
    document.getElementById('voiceStatus').textContent = '🎤 En écoute...';
    animatePulse();
  };
  
  recognition.onresult = (event) => {
    if (isGuideOnSpeaking) {
      window.speechSynthesis.cancel();
      isGuideOnSpeaking = false;
      document.getElementById('voiceMicBtn').textContent = '🎤 Parler';
    }
    
    let transcript = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    
    lastTranscript = transcript;
    document.getElementById('voiceText').textContent = transcript;
    
    // DÉTECTION FINALE - attendre la fin de phrase
    if (event.results[event.results.length - 1].isFinal) {
      console.log('✅ FINAL reçu:', transcript);
      recognition.stop();
      setTimeout(() => sendVoiceMessage(lastTranscript), 1000);
    }
  };
  
  recognition.onerror = (event) => {
    console.error('Erreur STT:', event.error);
  };
  
  recognition.onend = () => {
    isListening = false;
    console.log('✅ Reconnaissance terminée');
    // NE PAS redémarrer si en train d'envoyer le message
    if (!isSendingMessage && !isGuideOnSpeaking) {
      setTimeout(() => startListening(), 1000);
    }
  };
}

function startListening() {
  if (!recognition) initVoice();
  if (recognition && !isListening) {
    lastTranscript = '';
    document.getElementById('voiceText').textContent = '';
    console.log('🎤 Démarrage écoute...');
    recognition.start();
  }
}

function stopGuideOnSpeaking() {
  window.speechSynthesis.cancel();
  isGuideOnSpeaking = false;
  document.getElementById('voiceMicBtn').textContent = '🎤 Parler';
  document.getElementById('voiceStatus').textContent = '✅ Prêt';
  setTimeout(() => startListening(), 100);
}

async function sendVoiceMessage(text) {
  isSendingMessage = true;
  if (!text.trim()) {
    console.warn('⚠️ Texte vide reçu');
    setTimeout(() => startListening(), 500);
    return;
  }
  
  console.log('📝 ENVOI message:', text);
  addVoiceMessage('user', text);
  document.getElementById('voiceStatus').textContent = '⏳ Réponse...';
  
  try {
    const token = localStorage.getItem('token');
    console.log('🔗 Appel /api/chat...');
    
    const resp = await fetch('/api/voice-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    
    console.log('📥 Réponse reçue, status:', resp.status);
    
    const data = await resp.json();
      const reply = data.reply || '';
    console.log('📖 Réponse reçue:', reply.substring(0, 50));
    
    if (reply.trim()) {
      addVoiceMessage('assistant', reply.trim());
      speakResponse(reply.trim());
    } else {
      console.warn('⚠️ Réponse vide');
      isSendingMessage = false;
      setTimeout(() => startListening(), 500);
    }
  } catch(e) {
    console.error('❌ Erreur:', e.message);
    document.getElementById('voiceStatus').textContent = '❌ Erreur réseau';
    isSendingMessage = false;
    setTimeout(() => startListening(), 500);
  }
}

function speakResponse(text) {
  const synth = window.speechSynthesis;
  if (ttsUtterance) synth.cancel();
  ttsUtterance = new SpeechSynthesisUtterance(text);
  ttsUtterance.lang = 'fr-FR';
  const form = voiceForms[voiceForm] || voiceForms['Cove'];
  ttsUtterance.pitch = form.pitch;
  ttsUtterance.rate = form.rate;
  ttsUtterance.onstart = () => {
    isGuideOnSpeaking = true;
    document.getElementById('voiceMicBtn').textContent = '⏹️ Arrêter';
    document.getElementById('voiceStatus').textContent = '🔊 Parle...';
  };
  ttsUtterance.onend = () => {
    isGuideOnSpeaking = false;
    isSendingMessage = false;
    document.getElementById('voiceMicBtn').textContent = '🎤 Parler';
    document.getElementById('voiceStatus').textContent = '✅ Écoute';
    document.getElementById('voiceText').textContent = '';
    setTimeout(() => startListening(), 0);
  };
  synth.speak(ttsUtterance);
}

function changeVoiceForm(form) { voiceForm = form; document.getElementById('voiceMenu').style.display = 'none'; }
function changeAudioOutput(output) { document.getElementById('audioMenu').style.display = 'none'; }
function toggleCC() { alert('CC: À implémenter'); }
function showPhotoMenu() { alert('📷 Menu photo'); }

function animatePulse() {
  const v = document.getElementById('voiceVisualizer');
  if (!v || !isListening) return;
  const s = 0.8 + Math.sin(Date.now() / 300) * 0.2;
  v.style.transform = `scale(${s})`;
  if (isListening) requestAnimationFrame(animatePulse);
}

function addVoiceMessage(role, content) {
  const box = document.getElementById('voiceChatBox');
  if (!box) return;
  const div = document.createElement('div');
  div.style.cssText = `margin:6px 0;padding:8px;border-radius:6px;background:${role==='user'?'#7c3aed':'#1a1a2e'};color:#fff;font-size:11px;border:1px solid ${role==='user'?'#a78bfa':'#2d1b69'};word-wrap:break-word;`;
  div.textContent = (role === 'user' ? '🗣️ ' : '🎙️ ') + content;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

window.addEventListener('load', () => { initVoice(); });
