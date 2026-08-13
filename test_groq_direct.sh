#!/bin/bash

# Créer un fichier PDF valide avec du texte simple
cat > test_text.txt << 'TEXT'
Ceci est un document de test pour l'analyse PDF.
Il contient plusieurs paragraphes.
Le système doit extraire le texte et l'envoyer à GROQ pour analyse.
TEXT

# Envoyer directement à GROQ
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mixtral-8x7b-32768",
    "messages": [{
      "role": "user",
      "content": "Résume en 3 points ce texte: Ceci est un document de test pour l analyse PDF"
    }],
    "max_tokens": 512
  }' 2>&1 | tail -20
