with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

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
}'''

new_savePreferences = '''async function savePreferences() {
  const inst = document.getElementById('inst')?.value;
  const token = localStorage.getItem('gtoken');
  if(inst && token) {
    try {
      await fetch('/api/instructions', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({instructions:inst})});
    } catch(e) {}
  }
  alert('OK Prefs');
}'''

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
}'''

import re

# Remplacer savePassword (la plus longue version)
pattern = r'async function savePassword\(\)[\s\S]*?(?=async function|\Z)'
content = re.sub(pattern, new_savePassword + '\n\n', content, count=1)

# Remplacer savePreferences
pattern = r'async function savePreferences\(\)[\s\S]*?(?=async function|\Z)'
content = re.sub(pattern, new_savePreferences + '\n\n', content, count=1)

# Remplacer saveToneStyle
pattern = r'async function saveToneStyle\(\)[\s\S]*?(?=async function|\Z)'
content = re.sub(pattern, new_saveToneStyle + '\n\n', content, count=1)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("TOUTES LES FONCTIONS REMPLACEES")
