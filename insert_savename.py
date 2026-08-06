with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_savename = '''async function saveName() {
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

'''

html = html.replace('async function savePassword()', new_savename + 'async function savePassword()')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ saveName() insérée")
