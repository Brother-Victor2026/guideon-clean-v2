#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# Supprimer l'import Anthropic
old_import = """import pdfParse from 'pdf-parse';
import Anthropic from '@anthropic-ai/sdk';"""

new_import = """import pdfParse from 'pdf-parse';"""

content = content.replace(old_import, new_import)

# Remplacer l'endpoint par une version GROQ
old_endpoint = """// Endpoint analyse PDF avec Claude
app.post('/api/analyze-pdf', multer({storage: multer.memoryStorage()}).single('pdf'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({error: 'Aucun fichier PDF'});
    if (req.file.mimetype !== 'application/pdf') return res.status(400).json({error: 'Doit être un PDF'});

    // Parser le PDF
    let pdfText = '';
    try {
      const data = await pdfParse(req.file.buffer);
      pdfText = data.text;
    } catch(e) {
      return res.status(400).json({error: 'Erreur parsing PDF: ' + e.message});
    }

    if (!pdfText || pdfText.trim().length === 0) {
      return res.status(400).json({error: 'PDF vide ou non lisible'});
    }

    // Limiter à 10000 chars pour Claude
    const textToAnalyze = pdfText.substring(0, 10000);

    // Appeler Claude API
    const client = new Anthropic();
    const response = await client.messages.create({
      model: 'claude-opus-4-6',
      max_tokens: 1024,
      messages: [{
        role: 'user',
        content: `Analyse ce texte PDF et donne un résumé concis, les points clés, et suggestions pertinentes:\\n\\n${textToAnalyze}`
      }]
    });

    const analysis = response.content[0]?.text || 'Analyse non disponible';

    res.json({
      success: true,
      fileName: req.file.originalname,
      analysis: analysis,
      textLength: pdfText.length
    });
  } catch(e) {
    console.error('Analyze PDF error:', e);
    res.status(500).json({error: 'Erreur analyse: ' + e.message});
  }
});"""

new_endpoint = """// Endpoint analyse PDF avec GROQ
app.post('/api/analyze-pdf', multer({storage: multer.memoryStorage()}).single('pdf'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({error: 'Aucun fichier PDF'});
    if (req.file.mimetype !== 'application/pdf') return res.status(400).json({error: 'Doit être un PDF'});

    // Parser le PDF
    let pdfText = '';
    try {
      const data = await pdfParse(req.file.buffer);
      pdfText = data.text;
    } catch(e) {
      return res.status(400).json({error: 'Erreur parsing PDF: ' + e.message});
    }

    if (!pdfText || pdfText.trim().length === 0) {
      return res.status(400).json({error: 'PDF vide ou non lisible'});
    }

    // Limiter à 10000 chars pour GROQ
    const textToAnalyze = pdfText.substring(0, 10000);

    // Appeler GROQ API
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
          content: `Analyse ce texte PDF et donne un résumé concis, les points clés, et suggestions pertinentes:\\n\\n${textToAnalyze}`
        }],
        max_tokens: 1024
      })
    });

    const groqData = await groqRes.json();
    const analysis = groqData.choices?.[0]?.message?.content || 'Analyse non disponible';

    res.json({
      success: true,
      fileName: req.file.originalname,
      analysis: analysis,
      textLength: pdfText.length
    });
  } catch(e) {
    console.error('Analyze PDF error:', e);
    res.status(500).json({error: 'Erreur analyse: ' + e.message});
  }
});"""

content = content.replace(old_endpoint, new_endpoint)

with open('/data/data/com.termux/files/home/my-ai/server.mjs', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Endpoint modifié pour GROQ!")
