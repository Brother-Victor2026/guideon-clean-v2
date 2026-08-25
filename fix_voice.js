const fs = require('fs');
let content = fs.readFileSync('server.mjs', 'utf8');

const oldCode = `const data = await response.json();
                const reply = data.choices[0].message.content;
                res.json({ reply });`;

const newCode = `const data = await response.json();
                console.log('🔴 GROQ Response:', JSON.stringify(data, null, 2));
                if (!data.choices || !data.choices[0]) {
                  return res.status(500).json({ error: 'Invalid GROQ response', response: data });
                }
                const reply = data.choices[0].message.content;
                res.json({ reply });`;

if (content.includes(oldCode)) {
  content = content.replace(oldCode, newCode);
  fs.writeFileSync('server.mjs', content);
  console.log('✅ Modifié avec succès');
} else {
  console.log('❌ Code pas trouvé');
}
