with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Remplacer la ligne location.reload() dans saveName par loadProfile() avec localStorage
content = content.replace(
    "if(confirm('OK Nom - Continuer ?')) {\n        location.reload();",
    "if(confirm('OK Nom - Continuer ?')) {\n        localStorage.setItem('gname', name);\n        document.getElementById('userEmail').textContent = name;\n        loadProfile();"
)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("SAVENAME CORRIGEE")
