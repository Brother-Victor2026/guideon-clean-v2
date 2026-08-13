#!/usr/bin/env python3

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer le div tab-updates par un vide
old_pattern = r'<div id="tab-updates"[^>]*>.*?</div></div>'
import re

# Chercher et remplacer simplement
if 'id="tab-updates"' in content:
    # Trouver le début
    start = content.find('id="tab-updates"')
    start = content.rfind('<div', 0, start)  # Début du div
    
    # Trouver la fin (deux </div>)
    temp = content[start:]
    count = 0
    end = start
    for i, char in enumerate(temp):
        if temp[i:i+6] == '</div>':
            count += 1
            if count == 2:
                end = start + i + 6
                break
    
    # Remplacer
    new_div = '<div id="tab-updates" class="tab-content" style="display:none;"></div></div>'
    content = content[:start] + new_div + content[end:]
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ tab-updates vidé!")
else:
    print("❌ id=\"tab-updates\" non trouvé")
