#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'releaseDate: "30 juillet 2026",'
new = 'releaseDate: new Date().toLocaleDateString("fr-FR", { year: "numeric", month: "long", day: "numeric" }),'

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Date dynamique ajoutée!")
else:
    print("❌ Texte exact non trouvé")
