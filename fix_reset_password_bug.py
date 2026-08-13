#!/usr/bin/env python3
"""
Corriger le bug /api/reset-password - variable 'r' undefined
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Ancien code cassé
old = """const users = await fetch(`${DB}/users?reset_token=eq.${code}`, { headers: SB });
    const users = await r.json();"""

# Nouveau code correct
new = """const response = await fetch(`${DB}/users?reset_token=eq.${code}`, { headers: SB });
    const users = await response.json();"""

if old in content:
    content = content.replace(old, new)
    print("✅ Bug /api/reset-password corrigé!")
    print("✓ Variable 'r' remplacée par 'response'")
else:
    print("⚠ Pattern exact non trouvé, cherche manuellement...")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

