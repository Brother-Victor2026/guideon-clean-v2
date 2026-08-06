with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'r') as f:
    lines = f.readlines()

# Fix 1: Ligne 579 - remplacer const { token, name, password } = req.body;
for i, line in enumerate(lines):
    if i == 578 and "const { token, name, password } = req.body;" in line:
        indent = "    "
        lines[i] = indent + "const token = req.headers.authorization?.replace('Bearer ', '');\n"
        lines.insert(i+1, indent + "if (!token) return res.status(401).json({ error: 'Token manquant' });\n")
        break

# Fix 2: Trouver et remplacer la ligne pour /api/instructions
for i, line in enumerate(lines):
    if "const { token, instructions } = req.body;" in line and i > 590:
        indent = "    "
        lines[i] = indent + "const token = req.headers.authorization?.replace('Bearer ', '');\n"
        lines.insert(i+1, indent + "if (!token) return res.status(401).json({ error: 'Token manquant' });\n")
        break

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'w') as f:
    f.writelines(lines)

print("FIX APPLIQUE")
