#!/usr/bin/env python3
"""
Corriger les IDs du formulaire reset-password
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer les IDs pour correspondre à la fonction
replacements = [
    ('id="resetCode"', 'id="rc"'),
    ('id="resetPassword"', 'id="rp"'),
    ('id="resetPasswordConfirm"', 'id="rpe"'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ {old} → {new}")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ IDs du formulaire reset-password corrigés!")

