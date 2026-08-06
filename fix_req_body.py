with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'r') as f:
    lines = f.readlines()

# Fix 1: app.put - ajouter const { name, password } après le check token
for i, line in enumerate(lines):
    if i > 577 and i < 590 and "if (!token) return res.status(401)" in line and "app.put" in ''.join(lines[i-5:i]):
        lines.insert(i+1, "    const { name, password } = req.body;\n")
        break

# Fix 2: app.post - ajouter const { instructions } après le check token
for i, line in enumerate(lines):
    if i > 590 and i < 605 and "if (!token) return res.status(401)" in line and "app.post('/api/instructions'" in ''.join(lines[i-5:i]):
        lines.insert(i+1, "    const { instructions } = req.body;\n")
        break

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'w') as f:
    f.writelines(lines)

print("VARIABLES AJOUTEES")
