#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer require('fs') par fs
content = content.replace("require('fs').existsSync", "fs.existsSync")
content = content.replace("require('fs').readFileSync", "fs.readFileSync")
content = content.replace("require('fs').writeFileSync", "fs.writeFileSync")

with open('server.mjs', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Utilisation de fs corrigée!")
