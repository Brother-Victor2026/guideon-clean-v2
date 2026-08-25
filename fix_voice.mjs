import fs from 'fs';

let content = fs.readFileSync('server.mjs', 'utf8');

// Chercher la ligne avec regex (flexible sur les espaces)
const regex = /const reply = data\.choices\[0\]\.message\.content;/;

if (content.includes('const reply = data.choices[0].message.content;')) {
  // Remplacer la ligne simple
  content = content.replace(
    'const reply = data.choices[0].message.content;',
    `console.log('🔴 GROQ Response:', JSON.stringify(data, null, 2));
                if (!data.choices || !data.choices[0]) {
                  return res.status(500).json({ error: 'Invalid GROQ response', response: data });
                }
                const reply = data.choices[0].message.content;`
  );
  fs.writeFileSync('server.mjs', content);
  console.log('✅ Modifié avec succès');
} else {
  console.log('❌ Code pas trouvé - cherche de manière différente');
  if (content.includes('data.choices[0].message.content')) {
    console.log('⚠️ Trouvé avec différentes espaces/caractères');
  }
}
