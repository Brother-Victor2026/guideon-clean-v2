#!/usr/bin/env python3
"""
Session 12 - Fix changePassword ULTRA-SÉCURISÉ
Remplace UNIQUEMENT la fonction changePassword
"""

html_file = '/data/data/com.termux/files/home/my-ai/public/index.html'

# Lire le fichier
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fonction modal (à insérer AVANT changePassword)
modal_func = '''function showModal(title,message,okText='OK',cancelText=null,onOk=null,onCancel=null){const d=document.createElement('div');d.id='modalOverlay_'+Date.now();d.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:10000;';const m=document.createElement('div');m.style.cssText='background:#0f0f1a;border:2px solid #7c3aed;border-radius:12px;padding:20px;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.5);';const t=document.createElement('h3');t.textContent=title;t.style.cssText='color:#a78bfa;margin:0 0 12px 0;font-size:16px;';const msg=document.createElement('p');msg.textContent=message;msg.style.cssText='color:#9ca3af;margin:0 0 20px 0;font-size:14px;line-height:1.5;';const btns=document.createElement('div');btns.style.cssText='display:flex;gap:8px;justify-content:flex-end;';if(cancelText){const cancelBtn=document.createElement('button');cancelBtn.textContent=cancelText;cancelBtn.style.cssText='padding:8px 16px;background:#374151;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';cancelBtn.onclick=()=>{d.remove();if(onCancel)onCancel();};btns.appendChild(cancelBtn);}const okBtn=document.createElement('button');okBtn.textContent=okText;okBtn.style.cssText='padding:8px 16px;background:#2d1b69;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';okBtn.onclick=()=>{d.remove();if(onOk)onOk();};btns.appendChild(okBtn);m.appendChild(t);m.appendChild(msg);m.appendChild(btns);d.appendChild(m);document.body.appendChild(d);}'''

# Nouvelle fonction changePassword minifiée mais améliorée
new_change_pwd = '''function changePassword(){const newPwd=document.getElementById('newPwdSec').value,confirmPwd=document.getElementById('confirmPwdSec').value;if(!newPwd||!confirmPwd){showModal('Erreur','Remplissez tous les champs','OK');return;}if(newPwd!==confirmPwd){showModal('Erreur','Les mots de passe ne correspondent pas','OK');return;}const btn=event.target;btn.disabled=true;btn.textContent='⏳ Changement...';fetch('/api/user/password',{method:'PUT',headers:{'Authorization':'Bearer '+localStorage.getItem('gtoken'),'Content-Type':'application/json'},body:JSON.stringify({password:newPwd})}).then(r=>r.json()).then(r=>{if(r.success){showModal('Succès','✅ Mot de passe changé!','Annuler','Accepter',()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';},()=>{document.getElementById('newPwdSec').value='';document.getElementById('confirmPwdSec').value='';btn.disabled=false;btn.textContent='Changer';});}else{showModal('Erreur','❌ '+r.error,'Annuler','Accepter',()=>{btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});}}).catch(e=>{showModal('Erreur','❌ Erreur: '+e.message,'Annuler','Accepter',()=>{btn.disabled=false;btn.textContent='Changer';},()=>{btn.disabled=false;btn.textContent='Changer';});});}'''

# Ancienne fonction à remplacer (pattern EXACT minifié)
old_change_pwd = "function changePassword(){const t=document.getElementById('newPwdSec').value,e=document.getElementById('confirmPwdSec').value;t&&e?t===e?fetch('/api/user/password',{method:'PUT',headers:{'Authorization':'Bearer '+localStorage.getItem('gtoken'),'Content-Type':'application/json'},body:JSON.stringify({password:t})}).then(t=>t.json()).then(e=>{e.success?(alert('✅ Changé!'),document.getElementById('newPwdSec').value='',document.getElementById('confirmPwdSec').value=''):alert('❌ '+e.error)}).catch(t=>alert('Erreur')):alert('❌ Mots de passe différents'):alert('❌ Remplissez les champs')}"

print("🔍 Vérification avant remplacement...")
if old_change_pwd in content:
    print("✓ Fonction changePassword() trouvée exactement")
    
    # Remplacer
    content = content.replace(old_change_pwd, new_change_pwd)
    print("✓ Fonction remplacée")
    
    # Ajouter showModal si absent
    if 'function showModal(' not in content:
        cp_pos = content.find('function changePassword()')
        if cp_pos != -1:
            content = content[:cp_pos] + modal_func + content[cp_pos:]
            print("✓ Fonction showModal() insérée")
    else:
        print("✓ showModal() déjà présente")
    
    # Sauvegarder
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ SUCCÈS!")
    print("✓ changePassword() remplacée")
    print("✓ Boutons: Annuler AVANT Accepter")
    print("✓ Modal dialog implémenté")
    
else:
    print("❌ Fonction changePassword() NON trouvée exactement!")
    print("Vérification alternative...")
    if 'function changePassword()' in content:
        print("⚠ Fonction existe mais la chaîne exacte ne correspond pas")
        print("Probablement déjà modifiée ou différente")
    else:
        print("❌ Fonction changePassword() ABSENTE du fichier!")

