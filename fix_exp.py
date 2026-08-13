with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer 7 jours par 60 jours
content = content.replace('Date.now() + 7*24*60*60*1000', 'Date.now() + 60*24*60*60*1000')

with open('server.mjs', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Expiration fixée à 60 jours!")
