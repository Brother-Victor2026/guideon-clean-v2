#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer juste après l'ouverture du DOMContentLoaded
old = "document.addEventListener('DOMContentLoaded', () => {\n    console.log"
new = "document.addEventListener('DOMContentLoaded', () => {\n  alert('TEST: DOMContentLoaded works');\n    console.log"

content = content.replace(old, new)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Alerte test ajoutée!")
