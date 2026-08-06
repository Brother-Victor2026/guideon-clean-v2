import fs from 'fs';

const file = './server.mjs';
let content = fs.readFileSync(file, 'utf8');

// Cherche la ligne et ajoute du debug
const old = "const { message, history, token, model, temperature, session_id, userTime } = req.body;";
const newDebug = `const { message, history, token, model, temperature, session_id, userTime } = req.body;
  console.log('📥 token exists:', !!token);
  console.log('📥 token length:', token ? token.length : 'null');`;

if (content.includes(old)) {
  content = content.replace(old, newDebug);
  fs.writeFileSync(file, content);
  console.log('✅ Debug ajouté');
} else {
  console.log('❌ Ligne non trouvée');
}
