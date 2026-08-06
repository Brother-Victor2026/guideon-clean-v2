with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    lines = f.readlines()

# Extraire les fonctions (lignes 104-158, 0-indexed)
functions = lines[104:159]

# Supprimer les fonctions de leur place
del lines[104:159]

# Trouver le <script> tag (qui était ligne 160, maintenant décalé)
script_line = None
for i, line in enumerate(lines):
    if line.strip() == '<script>' and i > 100:
        script_line = i
        break

# Insérer juste après le <script> tag
if script_line is not None:
    for j, func in enumerate(functions):
        lines.insert(script_line + 1 + j, func)
    print(f"Fonctions déplacées après <script> ligne {script_line}")

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.writelines(lines)

print("FAIT")
