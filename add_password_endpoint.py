#!/usr/bin/env python3
"""
Ajouter l'endpoint PUT /api/user/password
"""

server_file = '/data/data/com.termux/files/home/my-ai/server.mjs'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Nouvel endpoint à insérer
new_endpoint = '''
app.put('/api/user/password', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    
    const { password } = req.body;
    if (!password || password.length < 6) {
      return res.status(400).json({ error: 'Mot de passe trop court' });
    }
    
    // Hasher le mot de passe
    const hashedPwd = require('crypto').createHash('sha256').update(password).digest('hex');
    
    // Mettre à jour dans Supabase
    const response = await fetch(`${DB}/users?id=eq.${user.id}`, {
      method: 'PATCH',
      headers: { ...SB, 'Prefer': 'return=minimal' },
      body: JSON.stringify({ password: hashedPwd })
    });
    
    if (response.ok) {
      return res.json({ success: true });
    } else {
      return res.status(500).json({ error: 'Erreur mise à jour' });
    }
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
});

'''

# Trouver où insérer (avant app.post('/api/instructions')
insert_pos = content.find("app.post('/api/instructions'")
if insert_pos == -1:
    print("❌ app.post('/api/instructions') non trouvée!")
    exit(1)

# Insérer l'endpoint
new_content = content[:insert_pos] + new_endpoint + content[insert_pos:]

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Endpoint PUT /api/user/password ajouté!")
print("✓ Position: avant app.post('/api/instructions')")
print("✓ Fonctionnalités:")
print("  - Valide le token Bearer")
print("  - Hash le mot de passe")
print("  - Met à jour dans Supabase")
print("  - Retourne {success: true}")

