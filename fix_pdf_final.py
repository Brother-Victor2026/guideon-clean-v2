#!/usr/bin/env python3

filepath = 'public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Chercher le début du for et la fin du }
# Remplacer tout simplement le contenu

pattern = "for (const file of files) {"
idx = content.find(pattern)

if idx == -1:
    print("❌ Pattern not found")
    exit(1)

# Trouver la fin du for (le prochain } qui ferme la boucle)
start = idx + len(pattern)
brace_count = 1
i = start

while i < len(content) and brace_count > 0:
    if content[i] == '{':
        brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
    i += 1

end = i

# Remplacer
new_code = """for (const file of files) {
            const pdfMsg = '📄 ' + file.name + '\\n\\nPeux-tu analyser ce PDF?';
            if (textarea) {
              textarea.value = pdfMsg;
              setTimeout(() => sm(), 300);
            }
          }"""

content = content[:start] + "\n" + new_code + "\n" + content[end:]

with open(filepath, 'w') as f:
    f.write(content)

print("✅ PDF code simplified!")
