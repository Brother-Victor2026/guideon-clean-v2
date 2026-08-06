#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Trouver tab-profile et le remplacer complètement
start = content.find('<div id="tab-profile" class="tab-content"')
end = content.find('</div><div id="tab-', start) + 6

if start != -1 and end > start:
    new_profile = '''<div id="tab-profile" class="tab-content" style="display:none;">
<h4 style="color:#a78bfa;">👤 Profil</h4>
<input id="profName" placeholder="Nom" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<input id="profTone" placeholder="Ton (friendly/formal/casual)" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<input id="profStyle" placeholder="Style (concis/détaillé/neutre)" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<button onclick="loadMyProfile()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:8px;">🔄 Charger</button>
<button onclick="saveMyProfile()" style="width:100%;padding:10px;background:#10b981;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:8px;">💾 Sauvegarder</button>
<div id="profStats" style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-top:12px;font-size:12px;color:#9ca3af;"></div>
</div><div id="tab-'''
    
    content = content[:start] + new_profile + content[end:]

# Ajouter les fonctions
js = '''
function loadMyProfile(){
  const tok=localStorage.getItem('gtoken');
  fetch('/api/profile',{headers:{'Authorization':'Bearer '+tok}}).then(r=>r.json()).then(d=>{
    document.getElementById('profName').value=d.profile.name||'';
    document.getElementById('profTone').value=d.profile.tone||'';
    document.getElementById('profStyle').value=d.profile.style||'';
    loadMyStats();
  });
}
function saveMyProfile(){
  const tok=localStorage.getItem('gtoken');
  fetch('/api/profile/update',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+tok},body:JSON.stringify({name:document.getElementById('profName').value,tone:document.getElementById('profTone').value,style:document.getElementById('profStyle').value})}).then(r=>r.json()).then(d=>alert('✅ Sauvegardé')).catch(e=>alert('❌ '+e.message));
}
function loadMyStats(){
  const tok=localStorage.getItem('gtoken');
  fetch('/api/feedback/stats',{headers:{'Authorization':'Bearer '+tok}}).then(r=>r.json()).then(d=>document.getElementById('profStats').innerHTML='📊 Feedback: '+d.total_feedbacks+'<br>😊 Satisfaction: '+d.satisfaction_rate);
}
'''

content = content.replace('</script>', js + '</script>')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("✅ Profil enrichi")
