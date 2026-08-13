#!/usr/bin/env python3
"""
Corriger l'ordre: Annuler À GAUCHE, Accepter À DROITE
"""

html_file = '/data/data/com.termux/files/home/my-ai/public/index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# showModal avec Annuler VRAIMENT à gauche (créé EN PREMIER)
modal_func = '''function showModal(title,message,okText='OK',cancelText=null,onOk=null,onCancel=null){const d=document.createElement('div');d.id='modalOverlay_'+Date.now();d.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:10000;';const m=document.createElement('div');m.style.cssText='background:#0f0f1a;border:2px solid #7c3aed;border-radius:12px;padding:20px;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.5);';const t=document.createElement('h3');t.textContent=title;t.style.cssText='color:#a78bfa;margin:0 0 12px 0;font-size:16px;';const msg=document.createElement('p');msg.textContent=message;msg.style.cssText='color:#9ca3af;margin:0 0 20px 0;font-size:14px;line-height:1.5;';const btns=document.createElement('div');btns.style.cssText='display:flex;gap:8px;justify-content:flex-end;';const cancelBtn=document.createElement('button');cancelBtn.textContent=cancelText||'Annuler';cancelBtn.style.cssText='padding:8px 16px;background:#374151;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';cancelBtn.onclick=()=>{d.remove();if(onCancel)onCancel();};if(cancelText)btns.appendChild(cancelBtn);const okBtn=document.createElement('button');okBtn.textContent=okText;okBtn.style.cssText='padding:8px 16px;background:#2d1b69;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;';okBtn.onclick=()=>{d.remove();if(onOk)onOk();};btns.appendChild(okBtn);m.appendChild(t);m.appendChild(msg);m.appendChild(btns);d.appendChild(m);document.body.appendChild(d);}'''

# Remplacer showModal
old_modal = 'function showModal(title,message,okText=\'OK\',cancelText=null,onOk=null,onCancel=null){const d=document.createElement(\'div\');d.id=\'modalOverlay_\'+Date.now();d.style.cssText=\'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:10000;\';const m=document.createElement(\'div\');m.style.cssText=\'background:#0f0f1a;border:2px solid #7c3aed;border-radius:12px;padding:20px;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.5);\';const t=document.createElement(\'h3\');t.textContent=title;t.style.cssText=\'color:#a78bfa;margin:0 0 12px 0;font-size:16px;\';const msg=document.createElement(\'p\');msg.textContent=message;msg.style.cssText=\'color:#9ca3af;margin:0 0 20px 0;font-size:14px;line-height:1.5;\';const btns=document.createElement(\'div\');btns.style.cssText=\'display:flex;gap:8px;justify-content:flex-end;\';if(cancelText){const cancelBtn=document.createElement(\'button\');cancelBtn.textContent=cancelText;cancelBtn.style.cssText=\'padding:8px 16px;background:#374151;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;\';cancelBtn.onclick=()=>{d.remove();if(onCancel)onCancel();};btns.appendChild(cancelBtn);}const okBtn=document.createElement(\'button\');okBtn.textContent=okText;okBtn.style.cssText=\'padding:8px 16px;background:#2d1b69;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;\';okBtn.onclick=()=>{d.remove();if(onOk)onOk();};btns.appendChild(okBtn);m.appendChild(t);m.appendChild(msg);m.appendChild(btns);d.appendChild(m);document.body.appendChild(d);}'

if old_modal in content:
    content = content.replace(old_modal, modal_func)
    print("✓ showModal() corrigée - Annuler À GAUCHE")
else:
    print("⚠ showModal() non trouvée, vérification...")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Ordre des boutons corrigé!")

