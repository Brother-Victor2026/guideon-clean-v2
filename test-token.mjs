import crypto from 'crypto';

const token = 'PASTE_THE_TOKEN_HERE';
const SECRET = 'guideon2026';

function checkToken(t) {
  try {
    const [p, s] = t.split('.');
    console.log('✓ Payload:', p);
    console.log('✓ Signature reçue:', s.substring(0, 20) + '...');
    
    const expected = crypto.createHmac('sha256', SECRET).update(p).digest('hex');
    console.log('✓ Signature attendue:', expected.substring(0, 20) + '...');
    console.log('✓ Match:', expected === s ? 'OUI ✅' : 'NON ❌');
    
    const d = JSON.parse(Buffer.from(p, 'base64').toString());
    console.log('✓ Decoded:', JSON.stringify(d, null, 2));
    console.log('✓ Now:', Date.now());
    console.log('✓ Exp:', d.exp);
    console.log('✓ Expiré?:', d.exp > Date.now() ? 'NON ✅' : 'OUI ❌');
    
    return d.exp > Date.now() ? d : null;
  } catch(e) { 
    console.error('❌ ERREUR:', e.message);
    return null; 
  }
}

const result = checkToken(token);
console.log('\n>>> RÉSULTAT FINAL:', result);
