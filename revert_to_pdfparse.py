#!/usr/bin/env python3

filepath = 'server.mjs'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert l'import
content = content.replace(
    "import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';",
    "import pdfParse from 'pdf-parse';"
)

# Revert le parsing
old_parse = """      const pdf = await pdfjsLib.getDocument({data: req.file.buffer}).promise;
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const text = await page.getTextContent();
        pdfText += text.items.map(t => t.str).join(' ') + ' ';
      }"""

new_parse = """      const data = await pdfParse(req.file.buffer);
      pdfText = data.text;"""

content = content.replace(old_parse, new_parse)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Revert à pdf-parse!")
