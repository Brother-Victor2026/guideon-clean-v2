with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    lines = f.readlines()

# Trouver les lignes où commencent les 4 fonctions
saveName_line = None
savePassword_line = None
savePreferences_line = None
saveToneStyle_line = None

for i, line in enumerate(lines):
    if 'async function saveName()' in line:
        saveName_line = i
    elif 'async function savePassword()' in line:
        savePassword_line = i
    elif 'async function savePreferences()' in line:
        savePreferences_line = i
    elif 'async function saveToneStyle()' in line:
        saveToneStyle_line = i

print(f"saveName: {saveName_line}, savePassword: {savePassword_line}, savePreferences: {savePreferences_line}, saveToneStyle: {saveToneStyle_line}")

# Compter combien de lignes chaque fonction prend (jusqu'au prochain 'async function' ou autre)
if saveName_line and savePassword_line:
    print(f"saveName prend {savePassword_line - saveName_line} lignes")
