#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter une alerte juste après <script>
old = "<script>\nfunction loadRealtime"
new = "<script>\nalert('SCRIPT LOADED');\nfunction loadRealtime"

content = content.replace(old, new)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Alerte au début du script ajoutée!")
