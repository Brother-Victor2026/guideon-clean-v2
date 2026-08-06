import re

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

new_functions = '''async function saveName() {
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

async function savePassword() {
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

async function savePreferences() {
  const inst = document.getElementById('inst')?.value;
  const token = localStorage.getItem('gtoken');
  if(inst && token) {
    try {
      await fetch('/api/instructions', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({instructions:inst})});
    } catch(e) {}
  }
  alert('OK Prefs');
}

async function saveToneStyle() {
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

p1 = r'async function saveName\(\)[^}]*\}'
p2 = r'async function savePassword\(\)[^}]*\}'
p3 = r'async function savePreferences\(\)[^}]*\}'
p4 = r'async function saveToneStyle\(\)[^}]*\}'

f1, rest = new_functions.split('\n\n', 1)
f2, rest = rest.split('\n\n', 1)
f3, rest = rest.split('\n\n', 1)
f4 = rest

content = re.sub(p1, f1, content, flags=re.DOTALL)
content = re.sub(p2, f2, content, flags=re.DOTALL)
content = re.sub(p3, f3, content, flags=re.DOTALL)
content = re.sub(p4, f4, content, flags=re.DOTALL)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("FAIT")
