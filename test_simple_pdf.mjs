import pdfParse from 'pdf-parse';
import fs from 'fs';

const pdfBuffer = fs.readFileSync('./simple.pdf');
pdfParse(pdfBuffer).then(data => {
  console.log('✅ PDF valide!');
  console.log('Texte extrait:', data.text);
}).catch(e => {
  console.error('❌ Erreur:', e.message);
});
