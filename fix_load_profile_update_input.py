with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Trouver et remplacer la dernière loadProfile (ligne 1298)
old_load = '''function loadProfile(){
  const tok = localStorage.getItem('gtoken');
  fetch('/api/profile', {headers: {'Authorization': 'Bearer '+tok}})
    .then(r=>r.json())
    .then(d => {
      document.getElementById('profileData').innerHTML = '👤 ' + d.profile.name + '<br>✉️ ' + d.profile.email;
      document.getElementById('toneInput').value = d.profile.tone || '';
      document.getElementById('styleInput').value = d.profile.style || '';
      loadStats();
    })
    .catch(e => document.getElementById('profileData').innerHTML = '❌ ' + e.message);
}'''

new_load = '''function loadProfile(){
  const tok = localStorage.getItem('gtoken');
  fetch('/api/profile', {headers: {'Authorization': 'Bearer '+tok}})
    .then(r=>r.json())
    .then(d => {
      document.getElementById('profileData').innerHTML = '👤 ' + d.profile.name + '<br>✉️ ' + d.profile.email;
      document.getElementById('pn').value = d.profile.name || '';
      document.getElementById('toneInput').value = d.profile.tone || '';
      document.getElementById('styleInput').value = d.profile.style || '';
      loadStats();
    })
    .catch(e => document.getElementById('profileData').innerHTML = '❌ ' + e.message);
}'''

content = content.replace(old_load, new_load)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("LOADPROFILE MISE A JOUR")
