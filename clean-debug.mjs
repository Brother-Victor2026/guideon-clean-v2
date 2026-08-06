import fs from 'fs';

const file = './server.mjs';
let content = fs.readFileSync(file, 'utf8');

// Remplace la fonction checkToken pour retirer le debug détaillé
const oldFunc = `function checkToken(t) {
  try {
    console.log('🔐 checkToken() called with token length:', t.length);
    const [p, s] = t.split('.');
    console.log('🔐 Payload length:', p.length, 'Signature length:', s.length);
    
    const expected = crypto.createHmac('sha256', SECRET).update(p).digest('hex');
    console.log('🔐 Expected sig:', expected.substring(0, 20) + '...');
    console.log('🔐 Received sig:', s.substring(0, 20) + '...');
    console.log('🔐 Match:', expected === s ? 'YES' : 'NO');
    
    if (expected !== s) {
      console.error('❌ Signature mismatch!');
      return null;
    }
    
    const d = JSON.parse(Buffer.from(p, 'base64').toString());
    console.log('🔐 Decoded:', JSON.stringify(d));
    console.log('🔐 Now:', Date.now(), 'Exp:', d.exp, 'Valid:', d.exp > Date.now());
    
    return d.exp > Date.now() ? d : null;
  } catch(e) { 
    console.error('❌ checkToken error:', e.message);
    return null; 
  }
}`;

const newFunc = `function checkToken(t) {
  try {
    const [p, s] = t.split('.');
    if (crypto.createHmac('sha256', SECRET).update(p).digest('hex') !== s) return null;
    const d = JSON.parse(Buffer.from(p, 'base64').toString());
    return d.exp > Date.now() ? d : null;
  } catch { return null; }
}`;

content = content.replace(oldFunc, newFunc);

// Retire les console.log de /api/chat
content = content.replace(/\s*console\.log\('🔐 token exists:.*?\);\s*/g, '');
content = content.replace(/\s*console\.log\('📥 token length:.*?\);\s*/g, '');

fs.writeFileSync(file, content);
console.log('✅ Debug nettoyé - checkToken() simplifié');
