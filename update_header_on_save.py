with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Remplacer saveName pour aussi mettre à jour le header
old_saveName = '''async function saveName() {
  const name = document.getElementById('pn')?.value;
  if(!name) return alert('Entrez un nom');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecte');
  fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})})
    .then(r=>r.json())
    .then(d => {
      if(d.success) {
        if(confirm('OK Nom - Continuer ?')) loadProfile();
      } else alert('Erreur: '+d.error);
    })
    .catch(e => alert('Erreur: '+e.message));
}'''

new_saveName = '''async function saveName() {
  const name = document.getElementById('pn')?.value;
  if(!name) return alert('Entrez un nom');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecte');
  fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})})
    .then(r=>r.json())
    .then(d => {
      if(d.success) {
        localStorage.setItem('gname', name);
        document.getElementById('userEmail').textContent = name;
        if(confirm('OK Nom - Continuer ?')) loadProfile();
      } else alert('Erreur: '+d.error);
    })
    .catch(e => alert('Erreur: '+e.message));
}'''

content = content.replace(old_saveName, new_saveName)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("HEADER MIS A JOUR")
