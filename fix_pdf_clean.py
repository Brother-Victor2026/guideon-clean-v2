#!/usr/bin/env python3

filepath = 'public/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# Code simple et propre à remplacer
old = """      if (confirmed) {
        const fileList = Array.from(files).map(f => `[PDF] ${f.name}`).join('\n');
        const textarea = document.getElementById('ui');
        if (textarea) {
          textarea.value += '\n' + fileList;
          alert('✅ ' + files.length + ' fichier(s) ajouté(s)');
        }
      }

      // Réinitialiser l'input
      e.target.value = '';"""

new = """      if (confirmed) {
        const textarea = document.getElementById('ui');
        for (const file of files) {
          const formData = new FormData();
          formData.append('pdf', file);
          fetch('/api/analyze-pdf', {method: 'POST', body: formData})
            .then(r => r.json())
            .then(d => { if (textarea) textarea.value = '\\n📄 ' + d.fileName + '\\n\\n' + d.analysis; })
            .catch(e => alert('Erreur: ' + e.message));
        }
      }

      // Réinitialiser l'input
      e.target.value = '';"""

if old not in content:
    print("❌ Code not found!")
    print("Cherche juste le pattern...")
    exit(1)

content = content.replace(old, new)

with open(filepath, 'w') as f:
    f.write(content)

print("✅ PDF fixed clean!")
