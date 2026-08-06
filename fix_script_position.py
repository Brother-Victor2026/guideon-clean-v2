with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Trouver le contenu du script orphelin
start = html.find('</html><script>')
end = html.rfind('</script>')

if start != -1 and end != -1:
    orphan_script = html[start+8:end]  # Extrait <script>...content
    
    # Placer avant le premier </html>
    html = html.replace('</html><script>', '</script></html><script>')
    html = html.replace('</html><script>', '<script>' + orphan_script + '</script>\n</html>')
    
    # Nettoyer les doublons
    html = html.replace('</script></html><script>', '<script>')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Script repositionné avant </html>")
