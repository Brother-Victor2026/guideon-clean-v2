#!/usr/bin/env python3

filepath = 'public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Ancien code qui ajoute juste à la textarea
old_code = """            const data = await res.json();
            if (textarea) {
              textarea.value += `\\n📄 ${data.fileName}\\n\\n${data.analysis}`;
            }"""

# Nouveau code qui envoie directement au chat
new_code = """            const data = await res.json();
            
            // Créer le message PDF
            const pdfMessage = `📄 **${data.fileName}**\\n\\n${data.analysis}`;
            
            // Ajouter à la textarea
            const textarea = document.getElementById('ui');
            if (textarea) {
              textarea.value = pdfMessage;
            }
            
            // Envoyer directement au chat
            setTimeout(() => {
              if (textarea) sm();
            }, 500);"""

if old_code not in content:
    print("❌ ERREUR: Code ancien non trouvé!")
    exit(1)

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Frontend modifié pour automatique!")
