import re

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Nouvelle implémentation des 4 fonctions
new_functions = '''async function saveName() {
  const name = document.getElementById('pn')?.value;
  if(!name) return alert('Entrez un nouveau nom');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecté');
  try {
    const r = await fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})});
    const d = await r.json();
    if(d.success) { alert('✅ Nom mis à jour'); document.getElementById('pn').value = ''; } else alert('❌ Erreur: '+d.error);
  } catch(e) { alert('❌ Erreur: '+e.message); }
}

async function savePassword() {
  const pwd = document.getElementById('pp')?.value;
  if(!pwd || pwd.length < 6) return alert('Mot de passe min 6 caractères');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecté');
  try {
    const r = await fetch('/api/profile', {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({token, password:pwd})});
    const d = await r.json();
    if(d.success) { alert('✅ Mot de passe mis à jour'); document.getElementById('pp').value = ''; } else alert('❌ Erreur: '+d.error);
  } catch(e) { alert('❌ Erreur: '+e.message); }
}

async function savePreferences() {
  const lang = document.getElementById('langSelect')?.value || 'auto';
  const theme = document.getElementById('themeSelect')?.value || 'dark';
  const length = document.getElementById('lengthSelect')?.value || 'normal';
  localStorage.setItem('gprefs', JSON.stringify({lang, theme, length, timestamp: Date.now()}));
  const inst = document.getElementById('inst')?.value;
  if(inst) {
    const token = localStorage.getItem('gtoken');
    if(token) {
      try {
        const r = await fetch('/api/instructions', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({instructions:inst})});
        const d = await r.json();
      } catch(e) {}
    }
  }
  alert('✅ Préférences sauvegardées');
}

async function saveToneStyle() {
  const tone = document.getElementById('toneInput')?.value;
  const style = document.getElementById('styleInput')?.value;
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecté');
  try {
    const r = await fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({tone, style})});
    const d = await r.json();
    if(d.success) { alert('✅ Tone/Style mis à jour'); } else alert('❌ Erreur: '+d.error);
  } catch(e) { alert('❌ Erreur: '+e.message); }
}'''

# Remplacer les 4 fonctions
patterns = [
    (r'function saveName\(\)\s*\{[^}]*\}', 'async function saveName() {...}'),
    (r'function savePassword\(\)\s*\{[^}]*\}', 'async function savePassword() {...}'),
    (r'function savePreferences\(\)\s*\{[^}]*?\n\}', 'async function savePreferences() {...}'),
]

# Chercher et remplacer chaque fonction
html = re.sub(r'async function saveName\(\)[^}]*\{[^}]*\}', new_functions.split('\n\n')[0], html)
html = re.sub(r'function savePassword\(\)[^}]*\{[^}]*\}', new_functions.split('\n\n')[1], html)
html = re.sub(r'function savePreferences\(\)\s*\{[^}]*?alert\([^)]*\);\s*\}', new_functions.split('\n\n')[2], html)

# Ajouter saveToneStyle si elle n'existe pas
if 'function saveToneStyle()' not in html:
    html = html.replace('function savePreferences()', 'function saveToneStyle() { ' + new_functions.split('\n\n')[3].replace('async function saveToneStyle() {', '') + '\n\nfunction savePreferences()')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Fonctions profil corrigées")
