#!/usr/bin/env python3

filepath = 'server.mjs'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Chercher et remplacer l'import
old_import = "import pdfParse from 'pdf-parse';"
new_import = "import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.js';"

content = content.replace(old_import, new_import)

# Chercher la ligne du parsing PDF et la remplacer
old_parse = """      const data = await pdfParse(req.file.buffer);
      pdfText = data.text;"""

new_parse = """      const pdf = await pdfjsLib.getDocument({data: req.file.buffer}).promise;
      let pdfText = '';
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const text = await page.getTextContent();
        pdfText += text.items.map(t => t.str).join(' ') + ' ';
      }"""

content = content.replace(old_parse, new_parse)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Endpoint modifié pour pdfjs-dist!")
