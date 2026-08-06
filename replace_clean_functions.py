with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    lines = f.readlines()

new_saveName = '''async function saveName() {
  const name = document.getElementById('pn')?.value;
  if(!name) { alert('Entrez un nom'); return; }
  const token = localStorage.getItem('gtoken');
  if(!token) { alert('Non connecte'); return; }
  try {
    const r = await fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})});
    const d = await r.json();
    alert(d.success ? 'OK Nom' : 'Erreur: '+d.error);
    if(d.success) document.getElementById('pn').value = '';
  } catch(e) { alert('Erreur: '+e.message); }
}
'''

new_savePassword = '''async function savePassword() {
  const pwd = document.getElementById('pp')?.value;
  if(!pwd || pwd.length < 6) { alert('Min 6 chars'); return; }
  const token = localStorage.getItem('gtoken');
  if(!token) { alert('Non connecte'); return; }
  try {
    const r = await fetch('/api/profile', {method:'PUT', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token}, body:JSON.stringify({password:pwd})});
    const d = await r.json();
    alert(d.success ? 'OK MDP' : 'Erreur: '+d.error);
    if(d.success) document.getElementById('pp').value = '';
  } catch(e) { alert('Erreur: '+e.message); }
}
'''

new_savePreferences = '''async function savePreferences() {
  const inst = document.getElementById('inst')?.value;
  const token = localStorage.getItem('gtoken');
  if(inst && token) {
    try {
      await fetch('/api/instructions', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({instructions:inst})});
    } catch(e) {}
  }
  alert('OK Prefs');
}
'''

new_saveToneStyle = '''async function saveToneStyle() {
  const tone = document.getElementById('toneInput')?.value;
  const style = document.getElementById('styleInput')?.value;
  const token = localStorage.getItem('gtoken');
  if(!token) { alert('Non connecte'); return; }
  try {
    const r = await fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({tone, style})});
    const d = await r.json();
    alert(d.success ? 'OK Tone' : 'Erreur: '+d.error);
  } catch(e) { alert('Erreur: '+e.message); }
}
'''

# Remplacer les lignes 104-122 (saveName)
lines[104:123] = [new_saveName]

# Recalculer les positions après le premier remplacement
# saveName prenait 19 lignes, nouvelle prend 13, donc décalage de -6
offset1 = 13 - 19  # -6

# Trouver à nouveau savePassword (qui était ligne 123, maintenant 123+offset1)
new_savePassword_line = 123 + offset1

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.writelines(lines)

print("ETAPE 1 COMPLETE")
