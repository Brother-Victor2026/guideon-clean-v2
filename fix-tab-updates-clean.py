#!/usr/bin/env python3

with open('public/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Les lignes 774-782 contiennent le div tab-updates
# Remplacer par un div vide
new_content = []
for i, line in enumerate(lines):
    if i < 773 or i > 781:  # Garder tout sauf les lignes 774-782
        new_content.append(line)
    elif i == 773:  # Ligne 774 (index 773)
        # Ajouter un div vide
        new_content.append('      <div id="tab-updates" class="tab-content" style="display:none;"></div>\n')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_content)
print("✅ tab-updates remplacé par un div vide proprement!")
