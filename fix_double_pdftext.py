#!/usr/bin/env python3

filepath = 'server.mjs'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer la double déclaration
old = """    let pdfText = '';
    try {
      const pdf = await pdfjsLib.getDocument({data: req.file.buffer}).promise;
      let pdfText = '';"""

new = """    let pdfText = '';
    try {
      const pdf = await pdfjsLib.getDocument({data: req.file.buffer}).promise;"""

content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Double déclaration pdfText supprimée!")
