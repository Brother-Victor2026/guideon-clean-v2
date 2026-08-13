#!/usr/bin/env python3
import json
import os

# Lire package.json
with open('package.json', 'r', encoding='utf-8') as f:
    pkg = json.load(f)
    current_version = pkg.get('version', '1.0.0')

# Lire server.mjs
with open('server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Nouveau code pour l'endpoint /api/version
new_endpoint = '''app.get('/api/version', (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    
    // Lire la version actuelle depuis package.json
    const pkg = require('./package.json');
    const currentVersion = pkg.version;
    
    // Lire la dernière version connue
    let lastVersion = '0.0.0';
    if (require('fs').existsSync('.last-version')) {
      lastVersion = require('fs').readFileSync('.last-version', 'utf-8').trim();
    }
    
    // Mettre à jour le fichier .last-version
    require('fs').writeFileSync('.last-version', currentVersion);
    
    // Déterminer si update disponible
    const updateAvailable = currentVersion !== lastVersion && lastVersion !== '0.0.0';
    
    res.json({
      current: currentVersion,
      latest: currentVersion,
      changelog: [
        "✨ Endpoint /api/sessions/logout-others",
        "🔒 Interface d'inscription améliorée",
        "📊 Nouvelles options de confidentialité",
        "📈 Statistiques détaillées"
      ],
      releaseDate: new Date().toLocaleDateString("fr-FR", { year: "numeric", month: "long", day: "numeric" }),
      updateAvailable: updateAvailable
    });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});'''

# Trouver et remplacer l'ancien endpoint
old_start = content.find("app.get('/api/version'")
old_end = content.find("});", old_start) + 3

if old_start > -1:
    content = content[:old_start] + new_endpoint + content[old_end:]
    with open('server.mjs', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Système de version automatique installé!")
else:
    print("❌ Endpoint /api/version non trouvé")
