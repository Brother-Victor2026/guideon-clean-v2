import re

with open('~/my-ai/public/index.html'.replace('~', '/data/data/com.termux/files/home'), 'r', encoding='utf-8') as f:
    html = f.read()

# Chercher le pattern exact après savePreferences
pattern = r'(<button onclick="savePreferences\(\)" style="[^"]*padding:10px[^"]*">💾 Sauvegarder préférences</button>)'

tone_style_html = '<input id="toneInput" placeholder="Tone de voix..." style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;"><input id="styleInput" placeholder="Style..." style="width:100%;padding:10px;background:#0f0f1a;color:#fff;border:1px solid #2d1b69;border-radius:8px;margin-bottom:8px;box-sizing:border-box;"><button onclick="saveToneStyle()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:12px;">💾 Enregistrer Tone/Style</button>'

html = re.sub(pattern, r'\1' + tone_style_html, html)

with open('~/my-ai/public/index.html'.replace('~', '/data/data/com.termux/files/home'), 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Inputs tone/style ajoutés")
