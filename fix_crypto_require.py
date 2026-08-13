#!/usr/bin/env python3
"""
Corriger require('crypto') → crypto directement
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer require('crypto') par crypto
old = "require('crypto').createHash"
new = "crypto.createHash"

if old in content:
    content = content.replace(old, new)
    print("✓ require('crypto') remplacé par crypto")
else:
    print("⚠ Chaîne non trouvée, vérification...")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fix appliqué!")

