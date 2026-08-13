with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter du logging après le fetch Groq
old = "if (!response.ok) {"
new = """console.log('🔍 Groq response status:', response.status);
    console.log('🔍 Groq response ok:', response.ok);
    if (!response.ok) {"""

content = content.replace(old, new)

with open('server.mjs', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Logs ajoutés!")
