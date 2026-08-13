#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Chercher et supprimer le code PDF du début
pdf_code_start = "  document.getElementById('pdfUploadInput').addEventListener('change', async (e) => {"
pdf_code_end = "  });\n});"

# Trouver le PDF code
import re
pdf_match = re.search(rf"{re.escape(pdf_code_start)}.*?{re.escape(pdf_code_end)}", content, re.DOTALL)

if pdf_match:
    pdf_code = pdf_match.group(0)
    # Supprimer du début
    content = content.replace(pdf_code, "")
    
    # Ajouter avant </body>
    pdf_wrapped = f"""<script>
document.addEventListener('DOMContentLoaded', () => {{
{pdf_code}
}});
</script>"""
    
    content = content.replace('</body>', pdf_wrapped + '\n</body>')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ PDF code déplacé à la fin!")
