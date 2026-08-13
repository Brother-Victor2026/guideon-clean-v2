#!/usr/bin/env python3

filepath = 'public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Chercher et fixer la double fermeture
# On cherche le pattern: 
#     }
#   }
# })();

# Et on remplace par:
#     }
# })();

fixed = False
i = 0
while i < len(lines) - 2:
    if '    }' in lines[i] and '  }' in lines[i+1] and '})();' in lines[i+2]:
        # On a trouvé la double fermeture
        print(f"✅ Double fermeture trouvée à ligne {i+1}")
        # Supprimer la ligne i+1 (la deuxième })
        lines.pop(i+1)
        fixed = True
        break
    i += 1

if not fixed:
    print("⚠️  Pattern exact non trouvé, cherche alternative...")
    # Cherche juste deux } d'affilée avant })();
    for i in range(len(lines) - 2):
        if lines[i].strip() == '}' and lines[i+1].strip() == '}' and '})();' in lines[i+2]:
            print(f"✅ Double fermeture trouvée à ligne {i+1}")
            lines.pop(i+1)
            fixed = True
            break

if fixed:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("✅ Double fermeture supprimée!")
else:
    print("❌ Pattern double fermeture non trouvé!")
    exit(1)
