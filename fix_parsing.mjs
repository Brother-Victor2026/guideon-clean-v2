import fs from 'fs';

let content = fs.readFileSync('public/voice-modal.js', 'utf8');

// Chercher la ligne de reader et tout remplacer jusqu'à la fin du while
const pattern = /const reader = resp\.body\.getReader\(\);[\s\S]*?while \(true\) \{[\s\S]*?\}\s*\}/;

const replacement = `const data = await resp.json();
      const reply = data.reply || '';`;

if (pattern.test(content)) {
  content = content.replace(pattern, replacement);
  fs.writeFileSync('public/voice-modal.js', content);
  console.log('✅ Parsing changé pour JSON simple');
} else {
  console.log('❌ Pattern pas trouvé');
}
