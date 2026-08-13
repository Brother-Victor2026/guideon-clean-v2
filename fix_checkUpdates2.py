with open('public/functions.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer les noms de champs
content = content.replace('data.current_version', 'data.current')
content = content.replace('data.latest_version', 'data.latest')
content = content.replace('data.release_date', 'data.releaseDate')
content = content.replace('data.update_available', 'data.updateAvailable')

with open('public/functions.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Noms de champs corrigés!")
