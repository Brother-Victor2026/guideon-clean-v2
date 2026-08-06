import re

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'r') as f:
    content = f.read()

# FIX 1: app.put('/api/profile')
old_put = """app.put('/api/profile', async (req, res) => {
  try {
    const { token, name, password } = req.body;
    console.log('🔑 Token:', token);
    const user = checkToken(token);
    console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const updates = {};
    if (name) updates.name = name;
    if (password) updates.password = hashPwd(password);
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify(updates) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});"""

new_put = """app.put('/api/profile', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Non autorisé' });
    const { name, password } = req.body;
    const updates = {};
    if (name) updates.name = name;
    if (password) updates.password = hashPwd(password);
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify(updates) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});"""

content = content.replace(old_put, new_put)

# FIX 2: app.post('/api/instructions')
old_post = """app.post('/api/instructions', async (req, res) => {
  try {
    const { token, instructions } = req.body;
    console.log('🔑 Token:', token);
    const user = checkToken(token);
    console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ instructions }) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});"""

new_post = """app.post('/api/instructions', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Non autorisé' });
    const { instructions } = req.body;
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ instructions }) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});"""

content = content.replace(old_post, new_post)

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'w') as f:
    f.write(content)

print("✅ Corrections appliquées aux 2 endpoints")
