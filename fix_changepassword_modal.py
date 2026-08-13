#!/usr/bin/env python3
"""
Session 12 - Fix changePassword avec Modal Dialog
Remplace les alert() par un vrai modal HTML/CSS
"""
import os
import re

# Fichier à modifier
html_file = '/data/data/com.termux/files/home/my-ai/public/index.html'

# Lire le fichier
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fonction modal à insérer (minifiée pour rester compact)
modal_function = '''function showModal(title,message,okText='OK',cancelText=null,onOk=null,onCancel=null){const d=document.createElement('div');d.id='modalOverlay_'+Date.now();d.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:10000;';const m=document.createElement('div');m.style.cssText='background:#0f0f1a;border:2px solid #7c3aed;border-radius:12px;padding:20px;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.5);';const t=document.createElement('h3');t.textContent=title;t.style.cssText='color:#a78bfa;margin:0 0 12px 0;font-size:16px;';const msg=document.createElement('p');msg.textContent=message;msg.style.cssText='color:#9ca3af;margin:0 0 20px 0;font-size:14px;line-height:1.5;';const btns=document.createElement('div');btns.style.cssText='display:flex;gap:8px;justify-content:flex-end;';const okBtn=document.createElement('button');okBtn.textContent=okText;okBtn.style.cssText='padding:8px 16px;background:#2d1b69;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';okBtn.onclick=()=>{d.remove();if(onOk)onOk();};btns.appendChild(okBtn);if(cancelText){const cancelBtn=document.createElement('button');cancelBtn.textContent=cancelText;cancelBtn.style.cssText='padding:8px 16px;background:#374151;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';cancelBtn.onclick=()=>{d.remove();if(onCancel)onCancel();};btns.appendChild(cancelBtn);}m.appendChild(t);m.appendChild(msg);m.appendChild(btns);d.appendChild(m);document.body.appendChild(d);}'''

# Nouvelle fonction changePassword() minifiée mais améliorée
new_change_password = '''function changePassword(){const newPwd=document.getElementById('newPwdSec').value,confirmPwd=document.getElementById('confirmPwdSec').value;if(!newPwd||!confirmPwd){showModal('Erreur','Remplissez tous les champs','OK');return;}if(newPwd!==confirmPwd){showModal('Erreur','Les mots de passe ne correspondent pas','OK');return;}const btn=event.target;btn.disabled=true;btn.textContent='⏳ Changement...';fetch('/api/user/password',{method:'PUT',headers:{'Authorization':'Bearer '+localStorage.getItem('gtoken'),'Content-Type':'application/json'},body:JSON.stringify({password:newPwd})}).then(r=>r.json()).then(r=>{if(r.success){showModal('Succès','✅ Mot de passe changé avec succès!','OK',null,()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';});}else{showModal('Erreur','❌ '+r.error,'OK',null,()=>{btn.disabled=false;btn.textContent='Changer';});}}).catch(e=>{showModal('Erreur','❌ Erreur réseau: '+e.message,'OK',null,()=>{btn.disabled=false;btn.textContent='Changer';});});}'''

# Ancienne fonction à remplacer (pattern minifié)
old_pattern = r"function changePassword\(\)\{const t=document\.getElementById\('newPwdSec'\)\.value,e=document\.getElementById\('confirmPwdSec'\)\.value;t&&e\?t===e\?fetch\('/api/user/password',\{method:'PUT',headers:\{'Authorization':'Bearer '\+localStorage\.getItem\('gtoken'\),'Content-Type':'application/json'\},body:JSON\.stringify\(\{password:t\}\)\}\)\.then\(t=>t\.json\(\)\)\.then\(e=>\{e\.success\?\(alert\('✅ Changé!'\),document\.getElementById\('newPwdSec'\)\.value='',document\.getElementById\('confirmPwdSec'\)\.value=''\):alert\('❌ '\+e\.error\)\}\)\.catch\(t=>alert\('Erreur'\)\):alert\('❌ Mots de passe différents'\):alert\('❌ Remplissez les champs'\)\}"

# Vérifier si la fonction existe
if 'function changePassword()' in content:
    # Chercher et remplacer avec regex
    try:
        # Remplacer l'ancienne fonction par la nouvelle
        new_content = re.sub(old_pattern, new_change_password, content)
        
        # Si la regex ne fonctionne pas exactement, chercher manuellement
        if new_content == content:
            # Cherche la fonction changePassword et la remplace
            start = content.find('function changePassword()')
            if start != -1:
                # Trouver la fin de la fonction (le dernier })
                end = content.find('}', start)
                # Continuer jusqu'à trouver le vrai end (avant la prochaine fonction)
                depth = 0
                for i in range(start, len(content)):
                    if content[i] == '{':
                        depth += 1
                    elif content[i] == '}':
                        depth -= 1
                        if depth == 0:
                            end = i + 1
                            break
                
                old_func = content[start:end]
                new_content = content[:start] + new_change_password + content[end:]
        
        # Insérer showModal avant changePassword si absent
        if 'function showModal(' not in new_content:
            cp_pos = new_content.find('function changePassword()')
            new_content = new_content[:cp_pos] + modal_function + new_content[cp_pos:]
        
        # Écrire le fichier modifié
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Modification réussie!")
        print("✓ Fonction showModal() insérée")
        print("✓ Fonction changePassword() remplacée")
        print("\nVérification:")
        print("- showModal présent:", "function showModal(" in new_content)
        print("- changePassword présent:", "function changePassword()" in new_content)
        print("- Ancien alert('Erreur') supprimé:", "alert('Erreur')" not in new_content)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
else:
    print("❌ Fonction changePassword() non trouvée!")

