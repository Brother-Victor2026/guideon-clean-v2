#!/usr/bin/env python3

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

modal = '''<!-- Modal Privacy Report -->
<div id="privacyModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:9999;align-items:flex-start;justify-content:center;overflow-y:auto;padding-top:20px;">
  <div style="background:#1a1a2e;padding:24px;border-radius:16px;width:88%;max-width:600px;border:1px solid #2d1b69;margin-bottom:20px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
      <h3 style="color:#a78bfa;margin:0;">📊 Rapport de Confidentialité</h3>
      <button onclick="document.getElementById('privacyModal').style.display='none'" style="background:none;border:none;color:#6b7280;font-size:24px;cursor:pointer;padding:0;width:24px;height:24px;">✕</button>
    </div>
    <div id="privacyContent" style="color:#9ca3af;font-size:12px;line-height:1.8;margin-bottom:16px;"></div>
    <div style="display:flex;gap:8px;">
      <button onclick="downloadPrivacyPDF()" style="flex:1;padding:10px;background:#2d1b69;color:#fff;border:none;border-radius:8px;cursor:pointer;">📥 Télécharger PDF</button>
      <button onclick="document.getElementById('privacyModal').style.display='none'" style="flex:1;padding:10px;background:#374151;color:#fff;border:none;border-radius:8px;cursor:pointer;">✕ Fermer</button>
    </div>
  </div>
</div>

'''

old_str = '</html>'
new_str = modal + '</html>'

if old_str in content:
    content = content.replace(old_str, new_str)
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Modal ajouté avec succès!")
else:
    print("❌ </html> non trouvé")
