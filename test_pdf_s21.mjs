import pdfParse from 'pdf-parse';
import fs from 'fs';

const pdfBuffer = fs.readFileSync('./rapport.pdf');
pdfParse(pdfBuffer).then(data => {
  console.log('✅ PDF valide:', data.text.substring(0, 100));
}).catch(e => {
  console.error('❌ Erreur PDF:', e.message);
});
