#!/usr/bin/env python3

with open('public/functions.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Nouvelle fonction downloadPrivacyPDF SANS alerte
new_pdf = '''async function downloadPrivacyPDF() {
  try {
    const tok = localStorage.getItem("gtoken");
    const res = await fetch('/api/privacy-report', {
      method: 'GET',
      headers: { "Authorization": "Bearer " + tok }
    });
    
    if (!res.ok) {
      alert("❌ Erreur: " + res.statusText);
      return;
    }
    
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'rapport-confidentialite.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}'''

# Nouvelle fonction checkUpdates avec date et meilleur affichage
new_updates = '''async function checkUpdates() {
  try {
    const tok = localStorage.getItem("gtoken");
    const res = await fetch('/api/version', {
      method: 'GET',
      headers: { "Authorization": "Bearer " + tok }
    });
    
    if (!res.ok) {
      alert("❌ Erreur: " + res.statusText);
      return;
    }
    
    const data = await res.json();
    const tabContent = document.getElementById('tab-updates');
    if (!tabContent) {
      alert("❌ Section mises à jour non trouvée");
      return;
    }
    
    let html = `<h4 style="color:#a78bfa;">📦 Mises à jour</h4>`;
    
    if (data.update_available) {
      html += `
        <div style="background:#0f0f1a;border:1px solid #7c3aed;border-radius:8px;padding:12px;margin-bottom:16px;">
          <p style="color:#a78bfa;font-size:13px;font-weight:bold;margin:0 0 6px 0;">✨ Version ${data.latest} - ${data.releaseDate || 'Date non disponible'}</p>
          <p style="color:#9ca3af;font-size:12px;margin:0 0 8px 0;">🎉 Nouvelles fonctionnalités disponibles</p>
          <ul style="color:#9ca3af;font-size:12px;margin:6px 0;padding-left:20px;">
            ${data.changelog.map(c => `<li>${c}</li>`).join('')}
          </ul>
          <button onclick="location.reload()" style="width:100%;padding:8px;background:#7c3aed;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-top:8px;">🔄 Actualiser</button>
        </div>
      `;
    } else {
      html += `
        <div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;">
          <p style="color:#10b981;font-size:13px;font-weight:bold;">✅ Vous avez la dernière version: ${data.current}</p>
          <p style="color:#9ca3af;font-size:12px;">📅 ${data.releaseDate || 'Date non disponible'}</p>
        </div>
      `;
    }
    
    html += `
      <h4 style="color:#a78bfa;">Vérification</h4>
      <button onclick="checkUpdates()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:8px;">🔄 Vérifier à nouveau</button>
      <label style="color:#9ca3af;font-size:12px;display:flex;align-items:center;gap:8px;margin-top:12px;">
        <input type="checkbox" id="autoUpdate" checked> Mises à jour automatiques
      </label>
    `;
    
    tabContent.innerHTML = html;
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}'''

# Remplacer downloadPrivacyPDF
old_pdf_start = content.find('async function downloadPrivacyPDF()')
old_pdf_end = content.find('\n}', old_pdf_start) + 2
if old_pdf_start > -1:
    content = content[:old_pdf_start] + new_pdf + content[old_pdf_end:]

# Remplacer checkUpdates
old_check_start = content.find('async function checkUpdates()')
old_check_end = content.rfind('}', old_check_start) + 1
if old_check_start > -1:
    content = content[:old_check_start] + new_updates + content[old_check_end:]

with open('public/functions.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Fonctions corrigées!")
