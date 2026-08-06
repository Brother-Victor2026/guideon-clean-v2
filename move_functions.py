with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    lines = f.readlines()

# Extraire les 4 fonctions (lignes 105-approx 180)
functions_start = 104  # ligne 105 (0-indexed)
functions_end = None

# Trouver où finit saveToneStyle
for i in range(functions_start, len(lines)):
    if i > functions_start + 50 and lines[i].strip().startswith('async function') and 'saveTone' not in lines[i]:
        functions_end = i
        break

if functions_end is None:
    # Chercher le prochain </script> ou autre marqueur
    for i in range(functions_start, len(lines)):
        if '</script>' in lines[i]:
            functions_end = i
            break

# Extraire les fonctions
functions = lines[functions_start:functions_end]

# Supprimer les fonctions de leur place actuelle
del lines[functions_start:functions_end]

# Trouver le <script> tag (maintenant le prochain après suppression)
script_tag_line = None
for i, line in enumerate(lines):
    if '<script>' in line and i > functions_start - 50:
        script_tag_line = i
        break

# Insérer juste après le <script> tag
if script_tag_line is not None:
    lines.insert(script_tag_line + 1, '\n')
    for j, func in enumerate(functions):
        lines.insert(script_tag_line + 2 + j, func)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.writelines(lines)

print("FONCTIONS DEPLACEES")
