with open('public/functions.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Trouver et remplacer le début de checkUpdates
old_start = 'async function checkUpdates() {'
new_start = '''async function checkUpdates() {
  const tabContent = document.getElementById('tab-updates');
  tabContent.innerHTML = '<h4 style="color:#a78bfa;">📦 Mises à jour</h4><p style="color:#9ca3af;margin:20px 0;text-align:center;">🔄 Vérification en cours...</p>';
'''

content = content.replace(old_start, new_start)

with open('public/functions.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Spinner de chargement ajouté!")
