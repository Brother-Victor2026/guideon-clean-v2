#!/bin/bash

# Sauvegarder d'abord
cp public/index.html public/index.html.backup-s21

# Remplacer le bloc if (confirmed) avec analyse
sed -i '425,433d' public/index.html

# Insérer le nouveau code à la ligne 425
sed -i '424a\      if (confirmed) {\
        const textarea = document.getElementById('"'"'ui'"'"');\
        for (const file of files) {\
          const formData = new FormData();\
          formData.append('"'"'pdf'"'"', file);\
          try {\
            const res = await fetch('"'"'/api/analyze-pdf'"'"', {method: '"'"'POST'"'"', body: formData});\
            if (!res.ok) { const err = await res.json(); alert('"'"'Erreur: '"'"' + err.error); continue; }\
            const data = await res.json();\
            if (textarea) { textarea.value += '"'"'\\n📄 '"'"' + data.fileName + '"'"'\\n'"'"' + data.analysis; }\
          } catch(e) { alert('"'"'Erreur: '"'"' + e.message); }\
        }\
      }' public/index.html

echo "✅ Remplacé avec sed!"
