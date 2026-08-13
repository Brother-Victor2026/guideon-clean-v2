#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer: <script src="..."> (avec code dedans)
# Par: <script src="..."></script> (fermé) + <script> (ouvert)

old = '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js">\nfunction loadRealtime'
new = '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n<script>\nfunction loadRealtime'

content = content.replace(old, new)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Balise <script> fixée!")
