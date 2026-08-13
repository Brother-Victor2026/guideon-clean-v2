#!/usr/bin/env python3

with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer la double fermeture
old = '''  }
});
});'''

new = '''  }
});'''

if old in content:
    content = content.replace(old, new)
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Erreur syntaxe corrigée!")
else:
    print("❌ Pattern non trouvé")
