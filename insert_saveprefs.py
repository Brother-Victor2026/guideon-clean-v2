with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_prefs = '''async function savePreferences() {
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

'''

html = html.replace('function checkUpdates()', new_prefs + 'function checkUpdates()')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ savePreferences() insérée")
