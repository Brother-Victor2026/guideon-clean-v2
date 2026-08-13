import pdfParse from 'pdf-parse';
import fs from 'fs';

const pdfBuffer = fs.readFileSync('./sample.pdf');
pdfParse(pdfBuffer).then(data => {
  console.log('✅ PDF valide!');
  console.log('Texte extrait (100 chars):', data.text.substring(0, 100));
}).catch(e => {
  console.error('❌ Erreur:', e.message);
});
