#!/usr/bin/env python3
import re

filepath = 'server.mjs'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'app.listen(process.env.PORT' not in content:
    print("❌ ERREUR: app.listen non trouvé!")
    exit(1)

new_endpoint = """// Endpoint analyse PDF avec GROQ - Session 21
app.post('/api/analyze-pdf', multer({storage: multer.memoryStorage(), limits: {fileSize: 50*1024*1024}}).single('pdf'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({error: 'Aucun fichier PDF'});
    if (req.file.mimetype !== 'application/pdf') return res.status(400).json({error: 'Doit être un PDF'});

    console.log(`[PDF] Analyse: ${req.file.originalname} (${req.file.size} bytes)`);

    let pdfText = '';
    try {
      const data = await pdfParse(req.file.buffer);
      pdfText = data.text;
    } catch(e) {
      console.error(`[PDF] Erreur parsing: ${e.message}`);
      return res.status(400).json({error: 'Erreur parsing PDF: ' + e.message});
    }

    if (!pdfText || pdfText.trim().length === 0) {
      return res.status(400).json({error: 'PDF vide ou non lisible'});
    }

    const textToAnalyze = pdfText.substring(0, 10000);
    console.log(`[PDF] Texte extrait: ${textToAnalyze.length} chars`);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);

    const groqRes = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'mixtral-8x7b-32768',
        messages: [{
          role: 'user',
          content: `Résume en 3 points ce PDF:\\n${textToAnalyze}`
        }],
        max_tokens: 512
      }),
      signal: controller.signal
    });

    clearTimeout(timeout);

    if (!groqRes.ok) {
      const errData = await groqRes.json();
      console.error(`[PDF] Erreur GROQ: ${groqRes.status}`, errData);
      return res.status(500).json({error: `Erreur GROQ: ${errData.error?.message || 'Inconnu'}`});
    }

    const groqData = await groqRes.json();
    const analysis = groqData.choices?.[0]?.message?.content || 'Analyse non disponible';

    console.log(`[PDF] Succès: ${req.file.originalname}`);

    res.json({
      success: true,
      fileName: req.file.originalname,
      analysis: analysis,
      textLength: pdfText.length
    });
  } catch(e) {
    console.error('[PDF] Erreur:', e.message);
    res.status(500).json({error: 'Erreur analyse: ' + e.message});
  }
});

"""

old_listen = "app.listen(process.env.PORT || 8080, () => console.log(\"Guideon actif !\"));"
new_listen = new_endpoint + old_listen

if old_listen not in content:
    print("❌ ERREUR: Pattern app.listen exact non trouvé!")
    exit(1)

content = content.replace(old_listen, new_listen)

if '/api/analyze-pdf' not in content:
    print("❌ ERREUR: L'endpoint n'a pas été ajouté!")
    exit(1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Endpoint /api/analyze-pdf ajouté avec succès!")
