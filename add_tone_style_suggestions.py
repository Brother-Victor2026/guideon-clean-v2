with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Remplacer toneInput et styleInput par des selects
old_tone = '<input id="toneInput" placeholder="Tone de voix..." style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">'

new_tone = '''<select id="toneInput" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<option value="">-- Sélectionner un tone --</option>
<option value="formel">📋 Formel</option>
<option value="decontracte">😊 Décontracté</option>
<option value="professionnel">💼 Professionnel</option>
<option value="amical">👋 Amical</option>
<option value="neutre">😐 Neutre</option>
</select>'''

old_style = '<input id="styleInput" placeholder="Style..." style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">'

new_style = '''<select id="styleInput" style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;">
<option value="">-- Sélectionner un style --</option>
<option value="court">⏱️ Court</option>
<option value="detaille">📖 Détaillé</option>
<option value="creatif">✨ Créatif</option>
<option value="technique">🔧 Technique</option>
<option value="simplifie">🎯 Simplifié</option>
</select>'''

content = content.replace(old_tone, new_tone)
content = content.replace(old_style, new_style)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("DROPDOWNS AJOUTEES")
