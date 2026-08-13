#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Supprimer les imports en double (lignes 21-24)
old = """import { fileURLToPath } from 'url';
import { dirname } from 'path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const pkg = JSON.parse(fs.readFileSync(__dirname + '/package.json', 'utf-8'));"""

new = """const pkg = JSON.parse(fs.readFileSync(__dirname + '/package.json', 'utf-8'));"""

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Doublons supprimés!")
else:
    print("❌ Pattern non trouvé")
