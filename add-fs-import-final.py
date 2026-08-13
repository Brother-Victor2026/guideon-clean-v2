#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter fs après path
old = "import path from 'path';"
new = "import path from 'path';\nimport fs from 'fs';"

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ fs importé!")
else:
    print("❌ Point d'insertion non trouvé")
