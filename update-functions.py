#!/usr/bin/env python3

with open('public/functions.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Nouvelle fonction downloadPrivacyReport
new_privacy = '''// Afficher le rapport de confidentialité dans un modal
async function downloadPrivacyReport() {
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
    const text = await blob.text();
    
    // Afficher les données dans le modal
    const contentDiv = document.getElementById('privacyContent');
    contentDiv.innerHTML = `
      <h4 style="color:#a78bfa;margin:12px 0 8px 0;">👤 Informations Utilisateur</h4>
      <p>${text.split('\\n')[1] || 'Email: -'}</p>
      <p>${text.split('\\n')[2] || 'Nom: -'}</p>
      
      <h4 style="color:#a78bfa;margin:12px 0 8px 0;">📊 Statistiques</h4>
      <p>${text.split('\\n')[4] || 'Total conversations: -'}</p>
      
      <h4 style="color:#a78bfa;margin:12px 0 8px 0;">🔒 Engagement</h4>
      <p>✓ Aucune donnée personnelle vendue à des tiers<br>
      ✓ Chiffrement end-to-end disponible<br>
      ✓ Droits RGPD & CCPA garantis<br>
      ✓ Données supprimées après 90 jours inactifs</p>
    `;
    
    // Afficher le modal
    document.getElementById('privacyModal').style.display = 'flex';
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}

// Télécharger le PDF
async function downloadPrivacyPDF() {
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
    alert("✅ PDF téléchargé avec succès!");
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}'''

# Nouvelle fonction checkUpdates
new_updates = '''// Vérifier et afficher les mises à jour
async function checkUpdates() {
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
    
    // Remplacer le contenu du tab
    const tabContent = document.getElementById('tab-updates');
    if (!tabContent) {
      alert("❌ Section mises à jour non trouvée");
      return;
    }
    
    let html = `<h4 style="color:#a78bfa;">📦 Mises à jour</h4>`;
    
    if (data.update_available) {
      html += `
        <div style="background:#0f0f1a;border:1px solid #7c3aed;border-radius:8px;padding:12px;margin-bottom:16px;">
          <p style="color:#a78bfa;font-size:13px;font-weight:bold;margin:0 0 6px 0;">✨ Nouvelle version: ${data.latest}</p>
          <p style="color:#9ca3af;font-size:12px;margin:0 0 8px 0;">Votre version: ${data.current}</p>
          <ul style="color:#9ca3af;font-size:12px;margin:6px 0;padding-left:20px;">
            ${data.changes.map(c => `<li>${c}</li>`).join('')}
          </ul>
          <button onclick="location.reload()" style="width:100%;padding:8px;background:#7c3aed;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-top:8px;">🔄 Actualiser</button>
        </div>
      `;
    } else {
      html += `
        <div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;">
          <p style="color:#10b981;font-size:13px;font-weight:bold;">✅ Vous avez la dernière version: ${data.current}</p>
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
    alert("✅ Vérification effectuée!");
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}'''

# Remplacer les anciennes fonctions
content = content.replace(
    content[content.find('// Télécharger rapport'):content.find('// Vérifier les mises à jour')],
    new_privacy + '\n\n'
)

# Trouver et remplacer checkUpdates
start = content.find('// Vérifier les mises à jour')
end = content.rfind('}', start) + 1
content = content[:start] + new_updates + content[end:]

with open('public/functions.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Fonctions mises à jour avec succès!")
