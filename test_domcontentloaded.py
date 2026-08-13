#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer le début du DOMContentLoaded
old = "document.addEventListener('DOMContentLoaded', () => {"
new = "document.addEventListener('DOMContentLoaded', () => {\n  alert('🔵 DOMContentLoaded déclenché');"

content = content.replace(old, new, 1)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Alerte ajoutée!")
