import PDFDocument from 'pdfkit';
import fs from 'fs';

const doc = new PDFDocument();
doc.pipe(fs.createWriteStream('test.pdf'));
doc.fontSize(20).text('Test PDF Session 21', 100, 100);
doc.fontSize(14).text('Ceci est un fichier PDF de test pour Guideon', 100, 150);
doc.addPage().fontSize(12).text('Page 2 - Contenu supplémentaire', 100, 100);
doc.end();

console.log('✅ test.pdf créé');
