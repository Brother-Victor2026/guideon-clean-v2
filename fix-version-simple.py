#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer la mauvaise syntaxe
old = """import pkg from './package.json' assert { type: 'json' };
const VERSION = pkg.version;"""

new = """const pkg = JSON.parse(fs.readFileSync('./package.json', 'utf-8'));
const VERSION = pkg.version;"""

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ VERSION lira depuis package.json (syntaxe compatible)!")
else:
    print("❌ Import JSON non trouvé")
