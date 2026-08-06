with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Remplacer savePreferences avec confirm
old_prefs = r'async function savePreferences\(\)[\s\S]*?\n\}'
new_prefs = '''async function savePreferences() {
  const inst = document.getElementById('inst')?.value;
  const token = localStorage.getItem('gtoken');
  if(inst && token) {
    fetch('/api/instructions', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({instructions:inst})})
      .catch(e => {});
  }
  if(confirm('✅ Préférences sauvegardées - Continuer ?')) location.reload();
}'''

import re
content = re.sub(old_prefs, new_prefs, content, flags=re.DOTALL)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("savePreferences FIXEE")
