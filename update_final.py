with open('public/functions.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trouver la ligne où commence checkUpdates()
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'async function checkUpdates()' in line:
        start_idx = i
    if start_idx != -1 and i > start_idx and line.strip() == '}':
        end_idx = i + 1
        break

if start_idx != -1 and end_idx != -1:
    # Nouvelle fonction complète
    new_function = '''async function checkUpdates() {
  const tabContent = document.getElementById('tab-updates');
  
  // Afficher le spinner
  tabContent.innerHTML = '<h4 style="color:#a78bfa;">📦 Mises à jour</h4><p style="color:#9ca3af;text-align:center;margin:20px 0;">🔄 Vérification en cours...</p>';
  
  try {
    const tok = localStorage.getItem("gtoken");
    const res = await fetch('/api/version', {
      method: 'GET',
      headers: { "Authorization": "Bearer " + tok }
    });

    if (!res.ok) {
      tabContent.innerHTML = '<h4 style="color:#a78bfa;">📦 Mises à jour</h4><p style="color:#f87171;">❌ Erreur: ' + res.statusText + '</p>';
      return;
    }

    const data = await res.json();
    const lastCheck = new Date().toLocaleString('fr-FR');
    let html = '<h4 style="color:#a78bfa;">📦 Mises à jour</h4>';
    
    if (data.updateAvailable) {
      html += '<div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;"><p style="color:#fbbf24;font-size:13px;font-weight:bold;margin:0 0 6px 0;">⚠️ Nouvelle version: ' + data.latest + '</p><p style="color:#9ca3af;font-size:12px;margin:0;">📅 ' + data.releaseDate + '</p></div>';
    } else {
      html += '<div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;"><p style="color:#65a30d;font-size:13px;font-weight:bold;margin:0;">✅ Dernière: ' + data.current + '</p><p style="color:#9ca3af;font-size:12px;margin:6px 0;">📅 ' + data.releaseDate + '</p><p style="color:#9ca3af;font-size:12px;margin:6px 0;">🔔 Check: ' + lastCheck + '</p><p style="color:#9ca3af;font-size:12px;margin:0;">⚡ Prochain: dans 24h</p></div>';
    }

    html += '<h4 style="color:#a78bfa;">Vérification</h4><button onclick="checkUpdates()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:8px;">🔄 Vérifier</button><label style="color:#9ca3af;font-size:12px;"><input type="checkbox" id="autoUpdate" checked> Auto</label>';
    
    tabContent.innerHTML = html;
  } catch (e) {
    tabContent.innerHTML = '<h4 style="color:#a78bfa;">📦 Mises à jour</h4><p style="color:#f87171;">❌ Erreur: ' + e.message + '</p>';
  }
}
'''
    
    # Remplacer
    lines = lines[:start_idx] + [new_function + '\n'] + lines[end_idx:]
    
    with open('public/functions.js', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ checkUpdates() écrite proprement!")
else:
    print("❌ Fonction non trouvée")
