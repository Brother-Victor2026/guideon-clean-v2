import PDFParser from 'pdf2json';
import fs from 'fs';

const parser = new PDFParser(null, 1);

parser.on("pdfParser_dataError", errData => {
  console.error("❌ Erreur:", errData);
});

parser.on("pdfParser_dataReady", pdfData => {
  const text = pdfData.Pages.map(p => 
    p.Texts?.map(t => t.R?.map(r => decodeURIComponent(r.T)).join('') || '').join(' ') || ''
  ).join('\n');
  
  console.log("✅ PDF parsé!");
  console.log("Texte (100 chars):", text.substring(0, 100));
});

parser.loadPDF('./sample.pdf');
