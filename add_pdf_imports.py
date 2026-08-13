#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter les imports après PDFDocument
old = "import PDFDocument from 'pdfkit';"
new = """import PDFDocument from 'pdfkit';
import pdfParse from 'pdf-parse';
import Anthropic from '@anthropic-ai/sdk';"""

content = content.replace(old, new)

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Imports ajoutés!")
