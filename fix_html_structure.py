#!/usr/bin/env python3
import re

# Lire le fichier
with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remplacer </html><script> par <script>
content = content.replace('</html><script>', '<script>')

# 2. Supprimer tous les </body> et </html> à la fin (garder juste le contenu)
content = re.sub(r'\n*</body>\s*\n*</html>\s*$', '', content)

# 3. Ajouter </body></html> à la fin
content = content.rstrip() + '\n</body>\n</html>'

# Sauvegarder
with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ HTML structure fixée!")
