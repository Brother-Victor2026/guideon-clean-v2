#!/usr/bin/env python3
import re

filepath = 'public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Chercher avec regex flexible
pattern = r"const pdfInput = document\.getElementById\('pdfUploadInput'\);.*?e\.target\.value = '';.*?\}\);"

if not re.search(pattern, content, re.DOTALL):
    print("❌ ERREUR: Pattern PDF non trouvé!")
    exit(1)

# Nouveau code
new_code = """const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {
      const files = e.target.files;
      if (files.length === 0) return;

      const fileNames = Array.from(files).map(f => f.name).join(', ');
      const confirmed = confirm('Analyser ' + files.length + ' fichier(s)?\\n\\n' + fileNames);

      if (confirmed) {
        for (const file of files) {
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
              alert('❌ Erreur: ' + error.error);
              continue;
            }

            const data = await response.json();
            console.log('[PDF] Analyse reçue:', data.fileName);
            
            const textarea = document.getElementById('ui');
            if (textarea) {
              textarea.value += `\\n📄 **${data.fileName}**\\n\\n${data.analysis}`;
              alert('✅ ' + data.fileName + ' analysé');
            }
          } catch (err) {
            console.error('[PDF] Erreur:', err);
            alert('❌ Erreur analyse: ' + err.message);
          }
        }
      }

      e.target.value = '';
    });
  }"""

content = re.sub(pattern, new_code, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Code frontend PDF remplacé avec regex!")
