import re

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

old_rpwd = r"function rpwd\(\) \{[\s\S]*?const c = document\.getElementById\('rc'\)\.value\.trim\(\);[\s\S]*?const p = document\.getElementById\('np'\)\.value;[\s\S]*?const pc = document\.getElementById\('cp'\)\.value;"

new_rpwd = """function rpwd() {
  const c = document.getElementById('resetCode').value.trim();
  const p = document.getElementById('resetPassword').value;
  const pc = document.getElementById('resetConfirm').value;"""

content = re.sub(old_rpwd, new_rpwd, content)

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ IDs fixes dans rpwd()")
