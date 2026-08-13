#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Supprimer l'alerte du bouton
old_btn = '<button class="pp" onclick="document.getElementById(\'pdfUploadInput\').click(); alert(\'PDF selected\');">📄 PDF</button>'
new_btn = '<button class="pp" onclick="document.getElementById(\'pdfUploadInput\').click();">📄 PDF</button>'
content = content.replace(old_btn, new_btn)

# 2. Remplacer l'input pour permettre multiple fichiers
old_input = '<input type="file" id="pdfUploadInput" accept=".pdf" style="display:none;">'
new_input = '<input type="file" id="pdfUploadInput" accept=".pdf" multiple style="display:none;">'
content = content.replace(old_input, new_input)

# 3. Remplacer le script par une version avec dialog custom
old_script = '''<script>
(function() {
  const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {
      alert('Upload: ' + e.target.files[0].name);
    });
  }
})();
</script>'''

new_script = '''<script>
(function() {
  const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {
      const files = e.target.files;
      if (files.length === 0) return;
      
      // Créer un dialog avec OK et Annuler
      const fileNames = Array.from(files).map(f => f.name).join(', ');
      const confirmed = confirm('Ajouter ' + files.length + ' fichier(s)?\\n\\n' + fileNames);
      
      if (confirmed) {
        const fileList = Array.from(files).map(f => `[PDF] ${f.name}`).join('\\n');
        const textarea = document.getElementById('ui');
        if (textarea) {
          textarea.value += '\\n' + fileList;
          alert('✅ ' + files.length + ' fichier(s) ajouté(s)');
        }
      }
      
      // Réinitialiser l'input
      e.target.value = '';
    });
  }
})();
</script>'''

content = content.replace(old_script, new_script)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fonctionnalité PDF complète!")
