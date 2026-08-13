#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter le script PDF juste avant </body>
pdf_script = """
<script>
document.addEventListener('DOMContentLoaded', () => {
  const pdfInput = document.getElementById('pdfUploadInput');
  if (!pdfInput) {
    console.error('PDF input not found');
    return;
  }
  pdfInput.addEventListener('change', async (e) => {
    alert('PDF selected: ' + (e.target.files[0]?.name || 'unknown'));
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('pdf', file);
    try {
      const response = await fetch('/api/upload', {method: 'POST', body: formData});
      const data = await response.json();
      if (data.success) {
        alert('PDF uploaded: ' + data.fileName);
        document.getElementById('ui').value = 'Fichier PDF: ' + data.fileName + '\nURL: ' + data.url;
      } else {
        alert('Error: ' + data.error);
      }
    } catch(err) {
      alert('Upload failed: ' + err.message);
    }
  });
});
</script>
"""

content = content.replace('</body>', pdf_script + '\n</body>')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PDF script ajouté proprement!")
