with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Remplacer saveName complètement
old_saveName = r'async function saveName\(\) \{[\s\S]*?\n\}'
new_saveName = '''async function saveName() {
  alert('TEST saveName');
  const name = document.getElementById('pn')?.value;
  if(!name) return alert('Entrez un nom');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecte');
  fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})})
    .then(r=>r.json())
    .then(d => alert(d.success ? 'OK Nom' : 'Erreur: '+d.error))
    .catch(e => alert('Erreur: '+e.message));
}'''

import re
content = re.sub(old_saveName, new_saveName, content, flags=re.DOTALL)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("saveName REMPLACEE")
