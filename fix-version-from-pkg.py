#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer la constante VERSION hard-codée
old = "const VERSION = '2.0.5';"
new = """import pkg from './package.json' assert { type: 'json' };
const VERSION = pkg.version;"""

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ VERSION lira maintenant depuis package.json!")
else:
    print("❌ const VERSION non trouvée")
