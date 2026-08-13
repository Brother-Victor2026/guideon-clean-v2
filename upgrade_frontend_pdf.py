#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer le script PDF par une version qui envoie au backend
old_script = '''<script>
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

new_script = '''<script>
(function() {
  const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {
      const files = e.target.files;
      if (files.length === 0) return;
      
      const fileNames = Array.from(files).map(f => f.name).join(', ');
      const confirmed = confirm('Analyser ' + files.length + ' fichier(s)?\\n\\n' + fileNames);
      
      if (confirmed) {
        // Envoyer chaque fichier à /api/analyze-pdf
        for (const file of files) {
          const formData = new FormData();
          formData.append('pdf', file);
          
          try {
            const response = await fetch('/api/analyze-pdf', {
              method: 'POST',
              body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
              const textarea = document.getElementById('ui');
              if (textarea) {
                textarea.value += '\\n\\n📄 **' + file.name + '**\\n' + data.analysis;
              }
            } else {
              alert('Erreur: ' + data.error);
            }
          } catch(err) {
            alert('Erreur analyse PDF: ' + err.message);
          }
        }
      }
      
      // Réinitialiser
      e.target.value = '';
    });
  }
})();
</script>'''

content = content.replace(old_script, new_script)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Frontend PDF amélioré!")
