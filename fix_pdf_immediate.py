#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer le DOMContentLoaded par du code immédiat
old = """document.addEventListener('DOMContentLoaded', () => {
  alert('TEST: DOMContentLoaded works');
    console.log('✅ DOMContentLoaded déclenché');
  document.getElementById('pdfUploadInput').addEventListener('change', async (e) => {"""

new = """function setupPdfListener() {
  const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {"""

content = content.replace(old, new)

# Fermer la fonction et l'exécuter
old2 = """    } catch(err) {
      alert(`Upload échoué: ${err.message}`);
    }
  });
});"""

new2 = """    } catch(err) {
      alert(`Upload échoué: ${err.message}`);
    }
    });
  } else {
    console.error('PDF input not found');
  }
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupPdfListener);
} else {
  setupPdfListener();
}"""

content = content.replace(old2, new2)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PDF setup immédiat appliqué!")
