with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# savePassword
old_pwd = r'async function savePassword\(\)[\s\S]*?\n\}'
new_pwd = '''async function savePassword() {
  const pwd = document.getElementById('pp')?.value;
  if(!pwd || pwd.length < 6) return alert('Min 6 chars');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecte');
  fetch('/api/profile', {method:'PUT', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token}, body:JSON.stringify({password:pwd})})
    .then(r=>r.json())
    .then(d => {
      if(d.success) {
        if(confirm('OK MDP - Continuer ?')) location.reload();
      } else alert('Erreur: '+d.error);
    })
    .catch(e => alert('Erreur: '+e.message));
}'''

# saveToneStyle
old_tone = r'async function saveToneStyle\(\)[\s\S]*?\n\}'
new_tone = '''async function saveToneStyle() {
  const tone = document.getElementById('toneInput')?.value;
  const style = document.getElementById('styleInput')?.value;
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecte');
  fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({tone, style})})
    .then(r=>r.json())
    .then(d => {
      if(d.success) {
        if(confirm('OK Tone/Style - Continuer ?')) location.reload();
      } else alert('Erreur: '+d.error);
    })
    .catch(e => alert('Erreur: '+e.message));
}'''

import re
content = re.sub(old_pwd, new_pwd, content, flags=re.DOTALL)
content = re.sub(old_tone, new_tone, content, flags=re.DOTALL)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("3 FONCTIONS FIXEES")
