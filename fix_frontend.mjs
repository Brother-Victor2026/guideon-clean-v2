import fs from 'fs';

let content = fs.readFileSync('public/voice-modal.js', 'utf8');

// Remplacer l'appel à /api/chat par /api/voice-chat
const old = `const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(token ? { 'Authorization': \`Bearer \${token}\` } : {}) },
      body: JSON.stringify({ message: text, token, model: 'llama-70b', temperature: 0.7 })
    });`;

const newCode = `const resp = await fetch('/api/voice-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });`;

if (content.includes(old)) {
  content = content.replace(old, newCode);
  fs.writeFileSync('public/voice-modal.js', content);
  console.log('✅ Frontend changé pour /api/voice-chat');
} else {
  console.log('❌ Code pas trouvé');
}
