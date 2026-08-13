#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter fs après les autres imports
old = "import crypto from 'crypto';"
new = "import crypto from 'crypto';\nimport fs from 'fs';"

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Import fs ajouté!")
else:
    print("❌ Point d'insertion non trouvé")
