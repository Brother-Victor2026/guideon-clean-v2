#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter un console.log au début du DOMContentLoaded
old = "document.addEventListener('DOMContentLoaded', () => {"
new = "document.addEventListener('DOMContentLoaded', () => {\n  console.log('🔍 DOMContentLoaded exécuté');"

content = content.replace(old, new)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Console.log ajouté!")
