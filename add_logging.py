with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Ajouter console.log dans saveName
old = '''async function saveName() {
  const name = document.getElementById('pn')?.value;
  if(!name) return alert('Entrez un nouveau nom');
  const token = localStorage.getItem('gtoken');
  if(!token) return alert('Non connecté');
  try {
    const r = await fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})});'''

new = '''async function saveName() {
  const name = document.getElementById('pn')?.value;
  if(!name) return alert('Entrez un nouveau nom');
  const token = localStorage.getItem('gtoken');
  console.log('TOKEN:', token);
  if(!token) return alert('Non connecté');
  try {
    console.log('Sending:', {name});
    const r = await fetch('/api/profile/update', {method:'POST', headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'}, body:JSON.stringify({name})});
    console.log('Response:', r);'''

html = html.replace(old, new)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Logging ajouté")
