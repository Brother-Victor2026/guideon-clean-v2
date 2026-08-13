#!/usr/bin/env python3
"""
Corriger les IDs du formulaire reset-password pour correspondre à rpwd()
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Les changements à faire
changes = [
    ('id="resetCode"', 'id="rc"'),
    ('id="resetPassword"', 'id="rp"'),
    ('id="resetPasswordConfirm"', 'id="rpe"'),
]

count = 0
for old, new in changes:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"✓ {old} → {new}")
    else:
        print(f"⚠ {old} non trouvé")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {count} IDs corrigés!")
print("Les IDs correspondent maintenant à la fonction rpwd()")

