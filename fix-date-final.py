#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trouver la ligne avec updateAvailable et l'insérer AVANT (ligne 957)
for i, line in enumerate(lines):
    if i == 956 and 'updateAvailable: false' in line:  # Ligne 957 en index 0
        # Insérer la date avant cette ligne
        indent = '        '
        lines.insert(i, f'{indent}releaseDate: "30 juillet 2026",\n')
        break

with open('server.mjs', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("✅ Date ajoutée avec succès!")
