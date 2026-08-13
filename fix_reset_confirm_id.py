#!/usr/bin/env python3
"""
Corriger le dernier ID - resetConfirm → rpe
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'id="resetConfirm"'
new = 'id="rpe"'

if old in content:
    content = content.replace(old, new)
    print(f"✓ {old} → {new}")
else:
    print(f"⚠ {old} non trouvé")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ID resetConfirm corrigé!")

