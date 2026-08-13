#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer le bouton PDF par une version avec onclick complet
old = '<button class="pp" onclick="document.getElementById(\'pdfUploadInput\').click();">📄 PDF</button>'
new = '<button class="pp" onclick="document.getElementById(\'pdfUploadInput\').click(); alert(\'PDF selected\');">📄 PDF</button>'

content = content.replace(old, new)

# Ajouter un listener simple après l'input
old2 = '<input type="file" id="pdfUploadInput" accept=".pdf" style="display:none;">'
new2 = '''<input type="file" id="pdfUploadInput" accept=".pdf" style="display:none;">
<script>
(function() {
  const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {
      alert('Upload: ' + e.target.files[0].name);
    });
  }
})();
</script>'''

content = content.replace(old2, new2)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PDF fix ultra-simple appliqué!")
