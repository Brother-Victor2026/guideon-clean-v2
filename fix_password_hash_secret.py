#!/usr/bin/env python3
"""
Corriger le changement de mot de passe pour utiliser hashPwd() avec SECRET
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Ancien hash sans SECRET
old = "const hashedPwd = crypto.createHash('sha256').update(password).digest('hex');"

# Nouveau hash avec hashPwd() qui inclut SECRET
new = "const hashedPwd = hashPwd(password);"

if old in content:
    content = content.replace(old, new)
    print("✓ Hash corrigé pour inclure SECRET")
else:
    print("⚠ Pattern exact non trouvé")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Endpoint corrigé!")
print("✓ Utilise maintenant hashPwd() avec SECRET")

