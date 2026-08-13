import pdfParse from 'pdf-parse';
import fs from 'fs';

const pdfBuffer = fs.readFileSync('./test.pdf');
pdfParse(pdfBuffer).then(data => {
  console.log('✅ PDF valide!');
  console.log('Texte extrait:', data.text.substring(0, 150));
}).catch(e => {
  console.error('❌ Erreur PDF:', e.message);
});
