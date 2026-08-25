import fs from 'fs';

let content = fs.readFileSync('server.mjs', 'utf8');

const old = "model: 'llama-3.3-70b-versatile'";
const newModel = "model: 'openai/gpt-oss-20b'";

if (content.includes(old)) {
  content = content.replace(old, newModel);
  fs.writeFileSync('server.mjs', content);
  console.log('✅ Modèle changé en openai/gpt-oss-20b');
} else {
  console.log('❌ Modèle pas trouvé');
}
