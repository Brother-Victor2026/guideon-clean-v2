#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer le addEventListener par une version sécurisée
old = """  alert('🔵 DOMContentLoaded déclenché');
    console.log('✅ DOMContentLoaded déclenché');
  document.getElementById('pdfUploadInput').addEventListener('change', async (e) => {"""

new = """  alert('🔵 DOMContentLoaded déclenché');
    console.log('✅ DOMContentLoaded déclenché');
  const pdfInput = document.getElementById('pdfUploadInput');
  if (pdfInput) {
    pdfInput.addEventListener('change', async (e) => {"""

content = content.replace(old, new)

# Fermer le if à la fin du addEventListener
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
    alert('❌ PDF input not found');
  }
});"""

content = content.replace(old2, new2)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PDF listener sécurisé!")
