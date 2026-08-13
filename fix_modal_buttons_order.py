#!/usr/bin/env python3
"""
Session 12 - Corriger l'ordre des boutons (Annuler AVANT OK)
"""
import re

html_file = '/data/data/com.termux/files/home/my-ai/public/index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Nouvelle showModal avec Annuler AVANT OK
new_modal = '''function showModal(title,message,okText='OK',cancelText=null,onOk=null,onCancel=null){const d=document.createElement('div');d.id='modalOverlay_'+Date.now();d.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:10000;';const m=document.createElement('div');m.style.cssText='background:#0f0f1a;border:2px solid #7c3aed;border-radius:12px;padding:20px;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.5);';const t=document.createElement('h3');t.textContent=title;t.style.cssText='color:#a78bfa;margin:0 0 12px 0;font-size:16px;';const msg=document.createElement('p');msg.textContent=message;msg.style.cssText='color:#9ca3af;margin:0 0 20px 0;font-size:14px;line-height:1.5;';const btns=document.createElement('div');btns.style.cssText='display:flex;gap:8px;justify-content:flex-end;';if(cancelText){const cancelBtn=document.createElement('button');cancelBtn.textContent=cancelText;cancelBtn.style.cssText='padding:8px 16px;background:#374151;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';cancelBtn.onclick=()=>{d.remove();if(onCancel)onCancel();};btns.appendChild(cancelBtn);}const okBtn=document.createElement('button');okBtn.textContent=okText;okBtn.style.cssText='padding:8px 16px;background:#2d1b69;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';okBtn.onclick=()=>{d.remove();if(onOk)onOk();};btns.appendChild(okBtn);m.appendChild(t);m.appendChild(msg);m.appendChild(btns);d.appendChild(m);document.body.appendChild(d);}'''

# Nouvelle changePassword avec les deux boutons
new_change_password = '''function changePassword(){const newPwd=document.getElementById('newPwdSec').value,confirmPwd=document.getElementById('confirmPwdSec').value;if(!newPwd||!confirmPwd){showModal('Erreur','Remplissez tous les champs','OK');return;}if(newPwd!==confirmPwd){showModal('Erreur','Les mots de passe ne correspondent pas','OK');return;}const btn=event.target;btn.disabled=true;btn.textContent='⏳ Changement...';fetch('/api/user/password',{method:'PUT',headers:{'Authorization':'Bearer '+localStorage.getItem('gtoken'),'Content-Type':'application/json'},body:JSON.stringify({password:newPwd})}).then(r=>r.json()).then(r=>{if(r.success){showModal('Succès','✅ Mot de passe changé avec succès!','Accepter','Annuler',()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});}else{showModal('Erreur','❌ '+r.error,'Accepter','Annuler',()=>{btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});}}).catch(e=>{showModal('Erreur','❌ Erreur réseau: '+e.message,'Accepter','Annuler',()=>{btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});});}'''

# Chercher et remplacer showModal
old_modal_pattern = r'function showModal\(title,message,okText=\'OK\',cancelText=null,onOk=null,onCancel=null\)\{const d=document\.createElement\(\'div\'\);.*?document\.body\.appendChild\(d\);\}'

if re.search(old_modal_pattern, content, re.DOTALL):
    content = re.sub(old_modal_pattern, new_modal, content, flags=re.DOTALL)
    print("✓ showModal() remplacée avec Annuler AVANT OK")
else:
    print("⚠ showModal() non trouvée par regex, cherche manuellement...")
    start = content.find('function showModal(')
    if start != -1:
        # Trouver la fin
        depth = 0
        for i in range(start, len(content)):
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    content = content[:start] + new_modal + content[end:]
                    print("✓ showModal() remplacée manuellement")
                    break

# Chercher et remplacer changePassword
old_pwd_pattern = r'function changePassword\(\)\{const newPwd=document\.getElementById\(\'newPwdSec\'\)\.value,confirmPwd=document\.getElementById\(\'confirmPwdSec\'\)\.value;if\(!newPwd\|\|!confirmPwd\)\{showModal\(\'Erreur\',\'Remplissez tous les champs\',\'OK\'\);return;\}if\(newPwd!==confirmPwd\)\{showModal\(\'Erreur\',\'Les mots de passe ne correspondent pas\',\'OK\'\);return;\}.*?catch\(e=>\{.*?\}\);\}'

if re.search(old_pwd_pattern, content, re.DOTALL):
    content = re.sub(old_pwd_pattern, new_change_password, content, flags=re.DOTALL)
    print("✓ changePassword() remplacée avec deux boutons")
else:
    print("⚠ changePassword() non trouvée par regex, cherche manuellement...")
    start = content.find('function changePassword()')
    if start != -1:
        depth = 0
        for i in range(start, len(content)):
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    content = content[:start] + new_change_password + content[end:]
                    print("✓ changePassword() remplacée manuellement")
                    break

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Modification terminée!")
print("- Boutons: Annuler AVANT OK")
print("- Les deux boutons présents dans changePassword()")

