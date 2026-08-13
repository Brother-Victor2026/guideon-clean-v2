#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter la date dans l'endpoint
old = '        updateAvailable: false'
new = '        releaseDate: "30 juillet 2026",\n        updateAvailable: false'

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Date ajoutée à l'endpoint!")
else:
    print("❌ Point d'insertion non trouvé")
