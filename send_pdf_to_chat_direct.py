#!/usr/bin/env python3

filepath = 'public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer la boucle d'envoi à /api/analyze-pdf
old_code = """        for (const file of files) {
          try {
            const formData = new FormData();
            formData.append('pdf', file);

            console.log('[PDF] Envoi:', file.name);
            const response = await fetch('/api/analyze-pdf', {
              method: 'POST',
              body: formData
            });

            if (!response.ok) {
              const error = await response.json();
              alert('Erreur: ' + error.error);
              continue;
            }

            const data = await response.json();
            
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
            }, 500);
          } catch(e) {
            alert('Erreur: ' + e.message);
          }
        }"""

new_code = """        const textarea = document.getElementById('ui');
        for (const file of files) {
          const reader = new FileReader();
          reader.onload = (e) => {
            const base64 = e.target.result;
            const pdfMessage = `📄 **${file.name}**\\n\\n[PDF attaché - Guidéon peut l'analyser directement]\\n\\nPeux-tu analyser ce PDF et me donner un résumé?`;
            if (textarea) {
              textarea.value = pdfMessage;
              setTimeout(() => sm(), 300);
            }
          };
          reader.readAsDataURL(file);
        }"""

if old_code not in content:
    print("❌ ERREUR: Code non trouvé!")
    exit(1)

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PDF envoyé directement à Guidéon!")
