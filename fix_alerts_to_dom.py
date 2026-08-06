with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r') as f:
    content = f.read()

# Remplacer alert par un div visible
old_saveName = """if(d.success) { alert('✅ Nom mis à jour'); document.getElementById('pn').value = ''; } else alert('❌ Erreur: '+d.error);
  } catch(e) { alert('❌ Erreur: '+e.message); }"""

new_saveName = """if(d.success) { document.getElementById('pn').value = ''; alert('✅ Nom mis à jour: '+JSON.stringify(d)); } else { alert('❌ Erreur: '+JSON.stringify(d)); }
  } catch(e) { alert('❌ Erreur CATCH: '+e.message); console.log(e); }"""

content = content.replace(old_saveName, new_saveName)

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w') as f:
    f.write(content)

print("ALERTES MODIFIEES")
