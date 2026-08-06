with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Enlever "TEST saveName"
content = content.replace("  alert('TEST saveName');\n", "")

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("CLEAN")
