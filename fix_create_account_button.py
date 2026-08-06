import re

# Lire le fichier
with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ÉTAPE 1: Ajouter la fonction JavaScript AVANT </script>
new_function = '''
// Fonction pour afficher l'enregistrement
function switchToRegistration(){
  if(!confirm('Aller à l\\'enregistrement ?')) return;
  document.getElementById('prof').style.display='none';
  document.getElementById('authModal').scrollIntoView({behavior:'smooth'});
  stab('reg');
  alert('✅ Formulaire d\\'enregistrement prêt');
}
'''

# Insérer avant </script>
content = content.replace('</script>', new_function + '\n</script>')

# ÉTAPE 2: Remplacer le bouton cassé
old_button = '''<button onclick="document.getElementById('prof').style.display='none';document.getElementById('authModal').scrollIntoView({behavior:'smooth'});stab('reg')" style="width:100%;padding:10px;background:#065f46;color:#fff;border:none;border-radius:8px;cursor:pointer;">➕ Créer compte</button>'''

new_button = '''<button onclick="switchToRegistration()" style="width:100%;padding:10px;background:#065f46;color:#fff;border:none;border-radius:8px;cursor:pointer;">➕ Créer compte</button>'''

content = content.replace(old_button, new_button)

# Sauvegarder
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Bouton 'Créer compte' FIXÉ avec alerte confirm")
