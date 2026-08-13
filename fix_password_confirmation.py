#!/usr/bin/env python3
"""
Ajouter modal de CONFIRMATION AVANT de changer le mot de passe
"""

html_file = '/data/data/com.termux/files/home/my-ai/public/index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Nouvelle changePassword avec confirmation AVANT l'action
new_change_pwd = '''function changePassword(){const newPwd=document.getElementById('newPwdSec').value,confirmPwd=document.getElementById('confirmPwdSec').value;if(!newPwd||!confirmPwd){showModal('Erreur','Remplissez tous les champs','OK');return;}if(newPwd!==confirmPwd){showModal('Erreur','Les mots de passe ne correspondent pas','OK');return;}showModal('Confirmation','Êtes-vous sûr de vouloir changer votre mot de passe?','Annuler','Accepter',()=>{},()=>{const btn=event.target;btn.disabled=true;btn.textContent='⏳ Changement...';fetch('/api/user/password',{method:'PUT',headers:{'Authorization':'Bearer '+localStorage.getItem('gtoken'),'Content-Type':'application/json'},body:JSON.stringify({password:newPwd})}).then(r=>r.json()).then(r=>{if(r.success){showModal('Succès','✅ Mot de passe changé!','OK',null,()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';});}else{showModal('Erreur','❌ '+r.error,'OK',null,()=>{btn.disabled=false;btn.textContent='Changer';});}}).catch(e=>{showModal('Erreur','❌ Erreur: '+e.message,'OK',null,()=>{btn.disabled=false;btn.textContent='Changer';});});});}'''

# Ancienne fonction
old_change_pwd = '''function changePassword(){const newPwd=document.getElementById('newPwdSec').value,confirmPwd=document.getElementById('confirmPwdSec').value;if(!newPwd||!confirmPwd){showModal('Erreur','Remplissez tous les champs','OK');return;}if(newPwd!==confirmPwd){showModal('Erreur','Les mots de passe ne correspondent pas','OK');return;}const btn=event.target;btn.disabled=true;btn.textContent='⏳ Changement...';fetch('/api/user/password',{method:'PUT',headers:{'Authorization':'Bearer '+localStorage.getItem('gtoken'),'Content-Type':'application/json'},body:JSON.stringify({password:newPwd})}).then(r=>r.json()).then(r=>{if(r.success){showModal('Succès','✅ Mot de passe changé!','Annuler','Accepter',()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';},()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';});}else{showModal('Erreur','❌ '+r.error,'Annuler','Accepter',()=>{btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});}}).catch(e=>{showModal('Erreur','❌ Erreur: '+e.message,'Annuler','Accepter',()=>{btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});});}'''

if old_change_pwd in content:
    content = content.replace(old_change_pwd, new_change_pwd)
    print("✅ Modal de confirmation ajoutée!")
    print("✓ Étapes:")
    print("  1. Utilisateur clique 'Changer'")
    print("  2. Modal: 'Êtes-vous sûr?'")
    print("  3. 'Annuler' → annule tout")
    print("  4. 'Accepter' → change le password")
    print("  5. Modal de succès avec 'OK' seul")
else:
    print("❌ Fonction non trouvée!")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

