#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    lines = f.readlines()

# Trouver la ligne 673 (index 672)
insert_line = 673

# Ajouter JUSTE APRÈS le bouton Sauvegarder préférences
new_fields = '''<h4 style="color:#a78bfa;">🎯 Ton et Style</h4>
<input id="toneInput" placeholder="Ton (friendly/formal/casual)" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<input id="styleInput" placeholder="Style (concis/détaillé/neutre)" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<button onclick="updateProfile()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:12px;">💾 Enregistrer tone/style</button>
'''

lines.insert(insert_line, new_fields + '\n')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.writelines(lines)

print("✅ Champs tone/style ajoutés SEULEMENT")
