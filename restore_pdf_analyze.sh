#!/bin/bash

# Remplacer juste le bloc if (confirmed)
cat > /tmp/new_pdf_code.txt << 'CODE'
if (confirmed) {
        const textarea = document.getElementById('ui');
        for (const file of files) {
          const formData = new FormData();
          formData.append('pdf', file);
          try {
            const res = await fetch('/api/analyze-pdf', {method: 'POST', body: formData});
            if (!res.ok) { const err = await res.json(); alert('❌ ' + err.error); continue; }
            const data = await res.json();
            if (textarea) { textarea.value = '\n📄 ' + data.fileName + '\n\n' + data.analysis; }
          } catch(e) { alert('❌ ' + e.message); }
        }
      }
CODE

# Lire le code à remplacer
python3 << 'PYSCRIPT'
import re

filepath = 'public/index.html'

with open(filepath, 'r') as f:
    content = f.read()

with open('/tmp/new_pdf_code.txt', 'r') as f:
    new_code = f.read()

# Chercher et remplacer le bloc if (confirmed)
old_pattern = r"if \(confirmed\) \{.*?e\.target\.value = '';.*?\};"
# Mais on cherche juste le if...}
old_pattern = r"if \(confirmed\) \{[^}]*\}[^}]*\}"

# Utiliser une approche simple: find and replace
idx = content.find('if (confirmed) {')
if idx == -1:
    print("❌ not found")
    exit(1)

# Trouver la fin - cherche "e.target.value = '';"
end_idx = content.find("e.target.value = '';", idx) + len("e.target.value = '';")

old_text = content[idx:end_idx]
content = content.replace(old_text, new_code)

with open(filepath, 'w') as f:
    f.write(content)

print("✅ Restored!")
PYSCRIPT
