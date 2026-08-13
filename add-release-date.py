#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Chercher le pattern UNIQUE de l'endpoint /api/version
old_pattern = '''        ],
        updateAvailable: false
      }});'''

new_pattern = '''        ],
        releaseDate: "30 juillet 2026",
        updateAvailable: false
      }});'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Date ajoutée à l'endpoint /api/version!")
else:
    print("❌ Pattern unique non trouvé")
    print("Vérification du contenu...")
