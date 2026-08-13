#!/usr/bin/env python3

filepath = 'public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Code original à remplacer
old_code = """      if (confirmed) {
        const fileList = Array.from(files).map(f => `[PDF] ${f.name}`).join('\n');
        const textarea = document.getElementById('ui');
        if (textarea) {
          textarea.value += '\n' + fileList;
          alert('✅ ' + files.length + ' fichier(s) ajouté(s)');
        }
      }"""

# Nouveau code avec analyse
new_code = """      if (confirmed) {
        const textarea = document.getElementById('ui');
        for (const file of files) {
          const formData = new FormData();
          formData.append('pdf', file);
          try {
            const res = await fetch('/api/analyze-pdf', {method: 'POST', body: formData});
            if (!res.ok) {
              const err = await res.json();
              alert('Erreur: ' + err.error);
              continue;
            }
            const data = await res.json();
            if (textarea) {
              textarea.value += '\\n📄 ' + data.fileName + '\\n' + data.analysis;
            }
          } catch(e) {
            alert('Erreur: ' + e.message);
          }
        }
      }"""

if old_code not in content:
    print("❌ ERREUR: Code original non trouvé!")
    exit(1)

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Code PDF analyse ajouté!")
