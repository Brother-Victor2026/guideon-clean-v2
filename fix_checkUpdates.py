import re

with open('public/functions.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Nouvelle fonction checkUpdates()
new_func = '''async function checkUpdates() {
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

    const lastCheck = new Date().toLocaleString('fr-FR');
    let html = '<h4 style="color:#a78bfa;">📦 Mises à jour</h4>';
    
    if (data.update_available) {
      html += '<div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;"><p style="color:#a78bfa;font-size:13px;font-weight:bold;margin:0 0 6px 0;">⚠️ Nouvelle version: ' + data.latest_version + '</p><p style="color:#9ca3af;font-size:12px;margin:0;">' + data.release_date + '</p></div>';
    } else {
      html += '<div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;"><p style="color:#65a30d;font-size:13px;font-weight:bold;">✅ Dernière: ' + data.current_version + '</p><p style="color:#9ca3af;font-size:12px;">📅 ' + data.release_date + '</p><p style="color:#9ca3af;font-size:12px;">🔔 Check: ' + lastCheck + '</p><p style="color:#9ca3af;font-size:12px;">⚡ Prochain: dans 24h</p></div>';
    }

    html += '<h4 style="color:#a78bfa;">Vérification</h4><button onclick="checkUpdates()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:8px;">🔄 Vérifier</button><label style="color:#9ca3af;font-size:12px;"><input type="checkbox" id="autoUpdate" checked> Auto</label>';
    tabContent.innerHTML = html;
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}'''

pattern = r'async function checkUpdates\(\) \{[\s\S]*?\n\}'
content = re.sub(pattern, new_func, content)

with open('public/functions.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ checkUpdates() updated!")
