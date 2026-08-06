with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Le HTML à insérer (inputs + bouton)
tone_style_inputs = '<input id="toneInput" placeholder="Tone de voix..." style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;"><input id="styleInput" placeholder="Style..." style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;"><button onclick="saveToneStyle()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:12px;">💾 Enregistrer Tone/Style</button>'

# Point d'insertion : après "Sauvegarder préférences</button>" et avant "<label"
search = 'Sauvegarder préférences</button><label'
replacement = 'Sauvegarder préférences</button>' + tone_style_inputs + '<label'

html = html.replace(search, replacement)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Inputs tone/style ajoutés au HTML")
