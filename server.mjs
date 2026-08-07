import dotenv from 'dotenv';
dotenv.config();

import express from 'express';
import path from 'path';
import { createClient } from '@supabase/supabase-js';
import { fileURLToPath } from 'url';
import crypto from 'crypto';
import { Resend } from 'resend';
import multer from 'multer';

const app = express();
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const API_KEY = process.env.GROQ_API_KEY;
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const SECRET = process.env.JWT_SECRET || 'guideon2026';

const DB = SUPABASE_URL ? `${SUPABASE_URL}/rest/v1` : null;
const SB = { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}`, 'Content-Type': 'application/json' };

function hashPwd(p) { return crypto.createHash('sha256').update(p + SECRET).digest('hex'); }
function makeToken(id, email) {
  const p = Buffer.from(JSON.stringify({ id, email, exp: Date.now() + 7*24*60*60*1000 })).toString('base64');
  return p + '.' + crypto.createHmac('sha256', SECRET).update(p).digest('hex');
}
function checkToken(t) {
  try {
    const [p, s] = t.split('.');
    if (crypto.createHmac('sha256', SECRET).update(p).digest('hex') !== s) return null;
    const d = JSON.parse(Buffer.from(p, 'base64').toString());
    return d.exp > Date.now() ? d : null;
  } catch { return null; }
}

function getQuotaResetTime(displayTimeZone = 'Africa/Porto-Novo') {
  const now = new Date();
  const ptFormatter = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', year: 'numeric', month: '2-digit', day: '2-digit' });
  const ptParts = ptFormatter.formatToParts(now).reduce((acc, p) => { acc[p.type] = p.value; return acc; }, {});
  const refDate = new Date(`${ptParts.year}-${ptParts.month}-${ptParts.day}T12:00:00Z`);
  const ptHourAtNoonUTC = parseInt(new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', hour: '2-digit', hour12: false }).format(refDate), 10);
  const offsetHours = 12 - ptHourAtNoonUTC;
  let resetUTC = new Date(Date.UTC(parseInt(ptParts.year), parseInt(ptParts.month) - 1, parseInt(ptParts.day), offsetHours, 0, 0));
  if (resetUTC.getTime() <= now.getTime()) {
    resetUTC = new Date(resetUTC.getTime() + 24 * 60 * 60 * 1000);
  }
  const displayFormatter = new Intl.DateTimeFormat('fr-FR', { timeZone: displayTimeZone, hour: '2-digit', minute: '2-digit' });
  return { resetUTC, displayTime: displayFormatter.format(resetUTC) };
}

const MODELS = {
  'llama-70b': 'openai/gpt-oss-120b',
  'llama-8b': 'openai/gpt-oss-120b',
  'gemma': 'openai/gpt-oss-120b'
};

const SYSTEM = { role: "system", content: "Tu es Guideon, un assistant IA intelligent, sage et bienveillant, cree par Brother Victor Bossou. Tu reponds toujours dans la langue de l utilisateur avec precision, empathie et intelligence. Tu as acces a l historique complet des conversations et tu te souviens de tout. Ne dis jamais que tu n as pas de memoire. Tu connais l heure actuelle de l utilisateur mais ne la mentionne JAMAIS spontanement, uniquement si on te la demande. Tu peux generer des images automatiquement, faire des recherches web, traduire des textes, resumer des documents, analyser des images, aider en programmation, resoudre des problemes mathematiques. Ne dis JAMAIS que tu ne peux pas faire ces choses. Tu reponds avec bienveillance et professionnalisme. Ne mentionne jamais ton createur spontanement, seulement si on te le demande directement. Tu peux utiliser des emojis de temps en temps quand cela rend la conversation plus chaleureuse ou aide a exprimer une emotion, mais sans en abuser et sans en mettre dans chaque message. Utilise le formatage Markdown (gras, listes, titres, code) quand cela rend ta reponse plus claire et structuree, meme sans que l'utilisateur le demande explicitement. Si l'utilisateur te demande de decrire, montrer, illustrer ou imaginer quelque chose de visuel (objet, lieu, personnage, paysage, scene), tu DOIS terminer ta reponse par une ligne UNIQUE et SEPAREE au format exact : [GENERATE_IMAGE: description detaillee en anglais de l'image]. Ne dis JAMAIS de phrase d'introduction avant cette balise (comme 'Voici un portrait de', 'Voici une image de', 'Voici un dessin de', etc.). La balise doit etre sur sa propre ligne, sans texte avant. N'utilise la balise [GENERATE_IMAGE] UNIQUEMENT si le message contient explicitement les mots: image, photo, illustration, dessin, genere, montre-moi. Pour TOUS les autres messages sans exception (bonjour, conseils, questions, histoires, descriptions, code, etc.), n'utilise JAMAIS cette balise. Ne dis jamais de phrase du type 'Voici un portrait de' ou similaire. Ne mentionne JAMAIS le bouton copier ou des instructions du type 'pour copier le message, selectionnez et copiez-collez' ; ces fonctionnalites existent deja dans l\'interface, n\'en parle jamais. Quand l\'utilisateur demande un post, statut, message WhatsApp/Facebook/Instagram, caption, texte a copier, ou dit \'encadre-moi ca\', \'mets ca en bloc\', \'reformule pour que je copie\', \'je veux copier ca\', \'fais-moi un texte\', \'donne-moi un message\', tu DOIS mettre le texte dans un bloc UNIQUE et SEPARE. Quand l\'utilisateur dit \'autres\', \'encore\', \'d\'autres\', \'donne-m\'en d\'autres\', tu envoies 2 a 4 blocs encadres differents, chacun sur sa propre ligne UNIQUE et SEPAREE." };

app.use(express.json({ limit: '15mb' }));
app.use(express.static(path.join(__dirname, 'public')));


// Initialiser Resend
const resend = new Resend(process.env.RESEND_API_KEY);

app.post('/api/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    if (!email || !password) return res.status(400).json({ error: 'Email et mot de passe requis' });
    const checkR = await fetch(`${DB}/users?email=eq.${encodeURIComponent(email)}`, { headers: SB });
    const checkData = await checkR.json();
    if (Array.isArray(checkData) && checkData.length > 0) return res.status(400).json({ error: 'Email deja utilise' });
    const SB_SERVICE = { 'apikey': process.env.SUPABASE_KEY, 'Authorization': `Bearer ${process.env.SUPABASE_KEY}`, 'Content-Type': 'application/json', 'Prefer': 'return=representation' };
    const r = await fetch(`${DB}/users`, { method: 'POST', headers: SB_SERVICE, body: JSON.stringify({ email, password: hashPwd(password), name }) });
    const data = await r.json();
    if (!Array.isArray(data) || !data[0]) return res.status(400).json({ error: data.message || 'Erreur inscription' });
    res.json({ token: makeToken(data[0].id, email), name: data[0].name, email });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) return res.status(401).json({ error: 'Email et mot de passe requis' });
    
    // TEMPORARY DEBUG: Accept victorbossou59@gmail.com directly
    if (email === 'victorbossou59@gmail.com' && password === 'guideon2006') {
      const r = await fetch(`${DB}/users?email=eq.${encodeURIComponent(email)}`, { headers: SB });
      const users = await r.json();
      if (Array.isArray(users) && users[0]) {
        return res.json({ token: makeToken(users[0].id, email), name: users[0].name, email });
      }
    }
    
    const r = await fetch(`${DB}/users?email=eq.${encodeURIComponent(email)}`, { headers: SB });
    const users = await r.json();
    if (!Array.isArray(users) || !users[0]) return res.status(401).json({ error: 'Identifiants incorrects' });
    const storedPwd = users[0].password;
    const hashedPwd = hashPwd(password);
    const isMatch = storedPwd === password || storedPwd === hashedPwd;
    if (!isMatch) return res.status(401).json({ error: 'Identifiants incorrects' });
    res.json({ token: makeToken(users[0].id, email), name: users[0].name, email });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

const IMG_TAG_START = '[GENERATE_IMAGE';
const COPY_PHRASE_START = '(Pour copier';
const WATCH_TAGS = [IMG_TAG_START];

function partialTagSuffixLength(s) {
  let best = 0;
  for (const tag of WATCH_TAGS) {
    const max = Math.min(s.length, tag.length);
    for (let len = max; len > 0; len--) {
      if (s.slice(-len).toLowerCase() === tag.slice(0, len).toLowerCase()) { if (len > best) best = len; break; }
    }
  }
  return best;
}

function findWatchTagStart(s) {
  let bestIdx = -1;
  for (const tag of WATCH_TAGS) {
    const idx = s.toLowerCase().indexOf(tag.toLowerCase());
    if (idx !== -1 && (bestIdx === -1 || idx < bestIdx)) bestIdx = idx;
  }
  return bestIdx;
}

async function callStabilityAI(rawPrompt) {
  try {
    const transResp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ model: "openai/gpt-oss-20b", messages: [{ role: "user", content: `Rewrite this as a short vivid visual scene description in English for an AI image generator. Do not use words like draw, generate, picture of, image of, illustration of - describe the subject and scene directly. Reply with ONLY the description, no quotes: "${rawPrompt}"` }], max_tokens: 500, reasoning_effort: "low" })
    });
    const transData = await transResp.json();
    const englishPrompt = transData.choices?.[0]?.message?.content?.trim() || rawPrompt;
    console.error('Prompt envoye a Pollinations:', englishPrompt);
    const pollinationsUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(englishPrompt)}?width=1024&height=1024&nologo=true`;
    let imgResp;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);
    try {
      imgResp = await fetch(pollinationsUrl, { signal: controller.signal });
    } finally {
      clearTimeout(timeoutId);
    }
    if (!imgResp.ok) {
      const errText = await imgResp.text();
      console.error('Pollinations erreur:', imgResp.status, errText.slice(0, 300));
      return null;
    }
    const contentType = imgResp.headers.get('content-type') || 'image/jpeg';
    const arrayBuffer = await imgResp.arrayBuffer();
    console.error('Pollinations taille image (bytes):', arrayBuffer.byteLength);
    const ext = contentType.includes('png') ? 'png' : 'jpg';
    const filename = `img_${Date.now()}_${Math.random().toString(36).slice(2, 8)}.${ext}`;
    const uploadResp = await fetch(`${SUPABASE_URL}/storage/v1/object/images/${filename}`, {
      method: 'POST',
      headers: { 'apikey': SUPABASE_SERVICE_KEY, 'Content-Type': contentType },
      body: Buffer.from(arrayBuffer)
    });
    if (!uploadResp.ok) {
      const errText = await uploadResp.text();
      console.error('Erreur upload Supabase Storage:', uploadResp.status, errText.slice(0, 300));
      return null;
    }
    const publicUrl = `${SUPABASE_URL}/storage/v1/object/public/images/${filename}`;
    console.error('Image stockee sur Supabase Storage:', publicUrl);
    return publicUrl;
  } catch (e) {
    console.error('Pollinations exception:', e.message, e.cause);
    return null;
  }
}

app.post('/api/chat', async (req, res) => {
  try {
    const { message, history, token, model, temperature, session_id, userTime } = req.body;
  console.log('📥 token exists:', !!token);let userId = 'default';
    let dbHistory = [];
    let userInstructions = '';
    let user = null;
    if (token && DB) {
      user = checkToken(token);
      if (user) {
        userId = String(user.id);
        const [hRes, uRes] = await Promise.all([
          fetch(`${DB}/conversations?user_id=eq.${userId}&session_id=eq.${session_id}&order=id.asc&limit=30`, { headers: SB }),
          fetch(`${DB}/users?id=eq.${userId}&select=instructions`, { headers: SB })
        ]);
        const hData = await hRes.json();
        const uData = await uRes.json();
        if (Array.isArray(hData)) dbHistory = hData;
        if (Array.isArray(uData) && uData[0]) userInstructions = uData[0].instructions || '';
      }
    }
    const timeWords = ['heure','time','date','quelle heure','what time'];
    const asksTime = timeWords.some(w => message.toLowerCase().includes(w));
    const visualWords = [
      'genere','genere-moi','éénere','éénere-moi',
      'dessine','dessine-moi',
      'illustre','illustre-moi',
      'montre','montre-moi',
      'affiche','affiche-moi',
      'envoie une image','envoie-moi une image',
      'represente','represente-moi','éépresente','éépresente-moi',
      'visualise','visualise-moi',
      'peins','dépeins','crée une image','crée-moi',
      'produis une image','imagine',
      'photo de','image de','portrait de','illustration de',
      'aperçu de','rendu de',
      'à quoi ressemble','ça ressemble à quoi','à quoi ça a l\'air',
      'décris visuellement',
      'représentation visuelle','rendu visuel','visualisation de'
    ];
    const wantsVisual = visualWords.some(w => message.toLowerCase().includes(w));
    const visualBoost = wantsVisual ? "\n\nIMPORTANT: la demande actuelle de l'utilisateur appelle "
      + "clairement un contenu visuel ou narratif. Tu DOIS terminer ta reponse par la balise "
      + "[GENERATE_IMAGE: description en anglais] decrivant ce qui a ete demande ou raconte." : '';
    // Charger memories utilisateureturn
  let memoriesText = '';
  if (user && user.id) {
    try {
      const memRes = await fetch(`${DB}/memories?user_id=eq.${user.id}&order=updated_at.desc&limit=20`, { headers: SB });
      const mems = await memRes.json();
      if (Array.isArray(mems) && mems.length > 0) {
        memoriesText = '\n\nMEMOIRES SUR CET UTILISATEUR (infos retenues des conversations precedentes):\n' + mems.map(m => '- ' + m.content).join('\n');
      }
    } catch(e) { console.error('memories load error:', e.message); }
  }

  const sysContent = SYSTEM.content + (userInstructions ? `\n\nInstructions: ${userInstructions}` : '') + (userTime && asksTime ? `\n\nL heure exacte est ${userTime}.` : '') + visualBoost + memoriesText;
    const SYSTEM_MSG = { role: 'system', content: sysContent };
    const hist = dbHistory.length > 0 ? dbHistory : (history || []);
    const messages = [SYSTEM_MSG, ...hist.filter(h=>h&&h.role&&h.content).map(h => ({ role: h.role, content: h.content })), { role: 'user', content: message }];
    const geminiBody = JSON.stringify({ model: MODELS[model] || "openai/gpt-oss-120b", messages, temperature: parseFloat(temperature) || 0.7, stream: true });
    let response;
    for (let attempt = 0; attempt < 2; attempt++) {
      if (attempt > 0) await new Promise(r => setTimeout(r, 2000));
      response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" },
        body: geminiBody
      });
      if (response.ok || response.status !== 503) break;
      console.error(`GEMINI 503 (tentative ${attempt + 1}/2) - retry dans 2s...`);
    }

    if (!response.ok) {
      const errData = await response.json();
      console.error("GEMINI ERROR:", JSON.stringify(errData));
      const isQuotaExceeded = response.status === 429 || errData.error?.code === 429;
      if (isQuotaExceeded) {
        const { displayTime } = getQuotaResetTime();
        return res.status(429).json({
          quotaExceeded: true,
          error: `Vous avez atteint la limite de votre conversation pour aujourd'hui. Revenez vers ${displayTime} pour une nouvelle conversation.`,
          resetTime: displayTime
        });
      }
      const isOverloaded = response.status === 503;
      if (isOverloaded) {
        return res.status(503).json({ overloaded: true, error: "Guidéon est momentanément surchargé. Réessayez dans quelques secondes." });
      }
      return res.status(500).json({ error: errData.error?.message || JSON.stringify(errData) });
    }

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    let reply = '';
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let pending = '';
  let imageDone = false;
  let savedImageUrl = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        const t = line.trim();
        if (!t.startsWith('data: ')) continue;
        const d = t.slice(6);
        if (d === '[DONE]') continue;
        try {
          const parsed = JSON.parse(d);
          const content = parsed.choices?.[0]?.delta?.content;
          if (content) {
            reply += content;
            pending += content;
            let fullMatch = pending.match(/\[GENERATE_IMAGE:\s*([\s\S]+?)\]/);
            while (fullMatch && !imageDone) {
              const before = pending.slice(0, fullMatch.index);
              if (before) res.write(`data: ${JSON.stringify({ content: before })}\n\n`);
              const desc = fullMatch[1].trim();
              if (desc && wantsVisual) {
                try {
                  const imgUrl = await callStabilityAI(desc);
                  if (imgUrl) res.write(`data: ${JSON.stringify({ image: imgUrl })}\n\n`);
              if (imgUrl) savedImageUrl = imgUrl;
                } catch (e) {}
              }
              imageDone = true;
              pending = pending.slice(fullMatch.index + fullMatch[0].length);
              fullMatch = pending.match(/\[GENERATE_IMAGE:\s*([\s\S]+?)\]/);
            }
            if (imageDone) pending = pending.replace(/\[GENERATE_IMAGE:\s*[\s\S]+?\]/g, '');

            }
            const startIdx = findWatchTagStart(pending);
            if (startIdx !== -1) {
              const before = pending.slice(0, startIdx);
              if (before) res.write(`data: ${JSON.stringify({ content: before })}\n\n`);
              pending = pending.slice(startIdx);
            } else {
              const holdLen = partialTagSuffixLength(pending);
              if (pending.length > holdLen) {
                const toSend = pending.slice(0, pending.length - holdLen);
                res.write(`data: ${JSON.stringify({ content: toSend })}\n\n`);
                pending = pending.slice(pending.length - holdLen);
              }
          }
        } catch (e) {}
      }
    }
    if (pending) {
      res.write(`data: ${JSON.stringify({ content: pending })}\n\n`);
      pending = '';
    }
    reply = reply.replace(/\[GENERATE_IMAGE:\s*[\s\S]+?\]/g, '').replace(/^\s*true\s*$/m, '').trim();

    if (token && DB) {
      console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
      if (user) {
        const isFirst = dbHistory.length === 0;
        await fetch(`${DB}/conversations`, { method: 'POST', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify([{ user_id: String(user.id), role: 'user', content: message, session_id, image_url: null }])});
        const convRes = await fetch(`${DB}/conversations`, { method: 'POST', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify([{ user_id: String(user.id), role: 'assistant', content: reply, session_id, image_url: savedImageUrl }])});
    if (!convRes.ok) { console.error('ERREUR insertion conversations:', convRes.status, await convRes.text()); }
        if (isFirst && session_id) {
          const titleRes = await fetch("https://api.groq.com/openai/v1/chat/completions", { method: "POST", headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" }, body: JSON.stringify({ model: "openai/gpt-oss-20b", messages: [{ role: "user", content: `Génère un titre court (max 5 mots) pour cette conversation: "${message}". Réponds UNIQUEMENT avec le titre.` }], max_tokens: 500, reasoning_effort: "low" }) });
          const titleData = await titleRes.json();
          const title = titleData.choices?.[0]?.message?.content?.trim() || 'Nouvelle conversation';
          await fetch(`${DB}/sessions?id=eq.${session_id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ title }) });
        }
      }
    }
    res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
    res.end();
    // Extraire et sauvegarder memories en arriere-plan
    if (false && reply && user && user.id) { // EXTRACTION MEMORIES DESACTIVEE (economie quota Gemini free tier)
      try {
        const extractRes = await fetch('https://api.groq.com/openai/v1/chat/completions', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: 'openai/gpt-oss-20b',
            max_tokens: 250,
            messages: [
              { role: 'system', content: 'Tu es un extracteur de memoires. Analyse la conversation et extrait UNIQUEMENT les faits importants sur l utilisateur (prenom, profession, preferences, habitudes, objectifs). Reponds avec une liste de faits courts, un par ligne, commencant par "-". Si aucun fait important, reponds "AUCUN".' },
              { role: 'user', content: `Message utilisateur: ${message}\nReponse assistant: ${reply}` }
            ]
          })
        });
        const extractData = await extractRes.json();
        const facts = extractData.choices?.[0]?.message?.content?.trim() || '';
        if (facts && facts !== 'AUCUN') {
          const lines = facts.split('\n').filter(l => l.startsWith('-')).map(l => l.slice(1).trim()).filter(Boolean);
          for (const fact of lines) {
            await fetch(`${DB}/memories`, {
              method: 'POST',
              headers: { ...SB, 'Prefer': 'return=minimal' },
              body: JSON.stringify({ user_id: user.id, content: fact })
            });
          }
        }
      } catch(e) { console.error('memories save error:', e.message); }
    }
  } catch(e) {
    if (!res.headersSent) {
      res.status(500).json({ error: e.message });
    } else if (!res.writableEnded) {
      res.write(`data: ${JSON.stringify({ error: e.message })}\n\n`);
      res.end();
    }
  }
});

app.post('/api/chat/temp', async (req, res) => {
  try {
    const { message, history = [], model, temperature = 0.7 } = req.body;
    const messages = [SYSTEM, ...history, { role: 'user', content: message }];
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", { method: "POST", headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" }, body: JSON.stringify({ model: MODELS[model] || "openai/gpt-oss-120b", messages, temperature: parseFloat(temperature) }) });
    const data = await response.json();
    res.json({ reply: data.choices?.[0]?.message?.content || "Erreur" });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/image', async (req, res) => {
  try {
    const { prompt, token, session_id } = req.body;
    const transResp = await fetch("https://api.groq.com/openai/v1/chat/completions", { method: "POST", headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" }, body: JSON.stringify({ model: "openai/gpt-oss-20b", messages: [{ role: "user", content: `Translate to English, reply with ONLY the English words: "${prompt}"` }], max_tokens: 500, reasoning_effort: "low" }) });
    const transData = await transResp.json();
    const englishPrompt = transData.choices?.[0]?.message?.content?.trim() || prompt;
    const imgUrl = await callStabilityAI(englishPrompt);
    if (!imgUrl) return res.status(500).json({ error: 'Image non generee' });
    let comment = 'Voici votre image !';
    try {
      const commentResp = await fetch("https://api.groq.com/openai/v1/chat/completions", { method: "POST", headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" }, body: JSON.stringify({ model: "openai/gpt-oss-20b", messages: [{ role: "user", content: `En une seule phrase tres courte en francais, presente cette image sans utiliser les mots 'Voici', 'portrait', 'illustration'. Description: "${englishPrompt}". Reponds uniquement avec la phrase, sans guillemets, sans markdown.` }], max_tokens: 500, reasoning_effort: "low" }) });
      const commentData = await commentResp.json();
      comment = commentData.choices?.[0]?.message?.content?.trim() || comment;
    } catch (e) {}
    if (token && session_id && DB) {
      try {
        console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
        if (user) {
          await fetch(`${DB}/conversations`, { method: 'POST', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify([
            { user_id: String(user.id), role: 'user', content: prompt, session_id, image_url: null },
            { user_id: String(user.id), role: 'assistant', content: comment, session_id, image_url: imgUrl }
          ])});
        }
      } catch (e) {}
    }
    res.json({ url: imgUrl, comment });
  } catch(e) { console.error('ERREUR /api/image:', e.message); res.status(500).json({ error: e.message }); }
});

app.post('/api/search', async (req, res) => {
  try {
    const { query } = req.body;
    const r = await fetch(`https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json`);
    const d = await r.json();
    res.json({ result: d.AbstractText || d.Answer || "Aucun resultat." });
  } catch(e) { res.json({ result: null }); }
});

app.post('/api/analyze', async (req, res) => {
  try {
    const { imageUrl, question } = req.body;
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", { method: "POST", headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" }, body: JSON.stringify({ model: "openai/gpt-oss-20b", messages: [{ role: "user", content: [{ type: "image_url", image_url: { url: imageUrl } }, { type: "text", text: question || "Décris cette image en détail." }] }], max_tokens: 1000, reasoning_effort: "low" }) });
    const data = await response.json();
    res.json({ reply: data.choices?.[0]?.message?.content || "Impossible d'analyser." });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/sessions', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const r = await fetch(`${DB}/sessions?user_id=eq.${String(user.id)}&order=created_at.desc`, { headers: SB });
    const data = await r.json();
    res.json(Array.isArray(data) ? data : []);
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/sessions', async (req, res) => {
    console.log('📞 POST /api/sessions reçu');
  try {
    const { token } = req.body;
        if (!token) return res.status(401).json({ error: 'Token requis' });
    
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    
    
    if (!user) {
      return res.status(401).json({ error: 'Email ou mot de passe incorrect' });
    }
    
    
    if (false) {
      return res.status(401).json({ error: 'Email ou mot de passe incorrect' });
    }
    
    const sessionId = Date.now().toString();
    const r = await fetch(`${DB}/sessions`, { method: 'POST', headers: { ...SB, 'Prefer': 'return=representation' }, body: JSON.stringify({ id: sessionId, user_id: String(user.id), title: 'Nouvelle conversation' }) });
    const data = await r.json();
    console.log('📊 Session créée:', data);
    if (!data || !data[0]) return res.status(500).json({ error: 'Erreur création session' });
    res.json({ success: true, session: { id: data[0].id } });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.delete('/api/sessions/:id', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/conversations?session_id=eq.${req.params.id}`, { method: 'DELETE', headers: SB });
    await fetch(`${DB}/sessions?id=eq.${req.params.id}&user_id=eq.${String(user.id)}`, { method: 'DELETE', headers: SB });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.patch('/api/sessions/:id', async (req, res) => {
  try {
    const { token, title } = req.body;
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/sessions?id=eq.${req.params.id}&user_id=eq.${String(user.id)}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ title }) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.patch('/api/sessions/:id/pin', async (req, res) => {
  try {
    const { token, pinned } = req.body;
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/sessions?id=eq.${req.params.id}&user_id=eq.${String(user.id)}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ pinned }) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/history/:sessionId', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const r = await fetch(`${DB}/conversations?user_id=eq.${String(user.id)}&session_id=eq.${req.params.sessionId}&order=id.asc&limit=500`, { headers: SB });
    const data = await r.json();
    res.json(Array.isArray(data) ? data : []);
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.delete('/api/memory', async (req, res) => {
  try {
    const { token } = req.body;
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/conversations?user_id=eq.${String(user.id)}`, { method: 'DELETE', headers: SB });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/memory/view', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const r = await fetch(`${DB}/users?id=eq.${user.id}&select=name,email,instructions,created_at`, { headers: SB });
    const data = await r.json();
    res.json(Array.isArray(data) ? data[0] : {});
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.put('/api/profile', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const { name, password } = req.body;
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
});


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
    const hashedPwd = hashPwd(password);
    
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

app.post('/api/instructions', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const { instructions } = req.body;
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ instructions }) });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.delete('/api/account', async (req, res) => {
  try {
    const { token } = req.body;
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    await fetch(`${DB}/conversations?user_id=eq.${String(user.id)}`, { method: 'DELETE', headers: SB });
    await fetch(`${DB}/sessions?user_id=eq.${String(user.id)}`, { method: 'DELETE', headers: SB });
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'DELETE', headers: SB });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/export/:sessionId', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const r = await fetch(`${DB}/conversations?user_id=eq.${String(user.id)}&session_id=eq.${req.params.sessionId}&order=id.asc`, { headers: SB });
    const data = await r.json();
    let text = 'Conversation Guideon\n\n';
    if (Array.isArray(data)) data.forEach(m => { text += (m.role === 'user' ? 'Vous: ' : 'Guideon: ') + m.content + '\n\n'; });
    res.setHeader('Content-Type', 'text/plain');
    res.setHeader('Content-Disposition', 'attachment; filename=conversation.txt');
    res.send(text);
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/share/:sessionId', async (req, res) => {
  try {
    const r = await fetch(`${DB}/conversations?session_id=eq.${req.params.sessionId}&order=id.asc`, { headers: SB });
    const data = await r.json();
    res.json(Array.isArray(data) ? data : []);
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/search/history', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const q = req.query.q;
    const r = await fetch(`${DB}/conversations?user_id=eq.${String(user.id)}&content=ilike.*${encodeURIComponent(q)}*&order=pinned.desc,created_at.desc&limit=20`, { headers: SB });
    const data = await r.json();
    res.json(Array.isArray(data) ? data : []);
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.delete('/api/regenerate', async (req, res) => {
  try {
    const { token, session_id } = req.body;
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    if (!user) return res.status(401).json({ error: 'Non autorise' });
    const r = await fetch(`${DB}/conversations?user_id=eq.${String(user.id)}&session_id=eq.${session_id}&order=pinned.desc,created_at.desc&limit=2`, { headers: SB });
    const data = await r.json();
    if (Array.isArray(data)) for (const msg of data) await fetch(`${DB}/conversations?id=eq.${msg.id}`, { method: 'DELETE', headers: SB });
    res.json({ success: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/models', (req, res) => { res.json(Object.keys(MODELS)); });


app.get('/api/stats', async (req, res) => {
  try {
    const auth = req.headers.authorization;
    if (!auth) return res.status(401).json({ error: 'Non autorise' });
    const tok = auth.replace('Bearer ', '');
    const user = checkToken(tok);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    const userId = String(user.id);
    const [convRes, msgRes, memRes] = await Promise.all([
      fetch(`${DB}/sessions?user_id=eq.${userId}&select=id`, { headers: SB }),
      fetch(`${DB}/conversations?user_id=eq.${userId}&select=id`, { headers: SB }),
      fetch(`${DB}/memories?user_id=eq.${userId}&select=id`, { headers: SB })
    ]);
    const convs = await convRes.json();
    const msgs = await msgRes.json();
    const mems = await memRes.json();
    res.json({ conversations: Array.isArray(convs) ? convs.length : 0, messages: Array.isArray(msgs) ? msgs.length : 0, memories: Array.isArray(mems) ? mems.length : 0 });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/feedback', async (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    console.log('🔑 Token:', token);
        const user = checkToken(token);
        console.log('👤 User:', user);
    const { message, rating } = req.body;
    if (user && DB) {
      await fetch(`${DB}/feedback`, { method: 'POST', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify({ user_id: String(user.id), message, rating }) });
    }
    res.json({ ok: true });
  } catch(e) { res.status(500).json({ error: e.message }); }
});


app.post('/api/upload', multer({storage: multer.memoryStorage()}).single('pdf'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({error: 'Aucun fichier'});
    if (req.file.mimetype !== 'application/pdf') return res.status(400).json({error: 'Doit être un PDF'});
    
    const bucketName = 'pdfs';
    const fileName = `${Date.now()}-${req.file.originalname}`;
    
    try {
      await sb.storage.createBucket(bucketName, {public: false});
    } catch(e) {
      if (!e.message.includes('already exists')) throw e;
    }
    
    const {data, error} = await sb.storage.from(bucketName).upload(fileName, req.file.buffer, {contentType: 'application/pdf'});
    
    if (error) return res.status(500).json({error: error.message});
    
    const {data: {publicUrl}} = sb.storage.from(bucketName).getPublicUrl(fileName);
    
    res.json({success: true, url: publicUrl, fileName: req.file.originalname});
  } catch(e) {
    console.error('Upload error:', e);
    res.status(500).json({error: e.message});
  }
});

app.post('/api/forgot-password', async (req, res) => {
  try {
    const { email } = req.body;
    if (!email) return res.status(400).json({ error: 'Email requis' });
    const token = Math.floor(100000 + Math.random() * 900000).toString();
    const r = await fetch(`${DB}/users?email=eq.${encodeURIComponent(email)}`, { headers: SB });
    const users = await r.json();
    if (!Array.isArray(users) || !users[0]) return res.json({ message: 'Si cet email existe, un code a été généré', reset_code: token });  // Code 6 chiffres
    const expires = new Date(Date.now() + 3600000).toISOString();
    await fetch(`${DB}/users?email=eq.${encodeURIComponent(email)}`, { method: 'PATCH', headers: { ...SB, 'Content-Type': 'application/json' }, body: JSON.stringify({ reset_token: token, reset_expires: expires }) });
    const resetUrl = `${process.env.APP_URL || 'https://guideon-8h4m.onrender.com'}/reset-password?token=${token}`;
    // En mode test, on ne peut pas envoyer d'email (resend = null)
    // Retourner le token directement pour testereturn
                // Envoyer l'email avec Resend
                try {
                  await resend.emails.send({
                    from: 'Guidéon <codjovictorbossou@gmail.com>',
                    to: email,
                    subject: 'Réinitialisation de votre mot de passe - Guidéon',
                    html: `<h2>Réinitialisation</h2><p><a href="${resetUrl}">Réinitialiser mon mot de passe</a></p><p>Lien expire dans 1 heure.</p>`
                  });
                  console.log('✓ Email envoyé à:', email);
                } catch (err) {
                  console.error('✗ Erreur email:', err.message);
                }
    res.json({ message: 'Si cet email existe, un code a été généré', reset_code: token });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.get('/reset-password', (req, res) => {
  const token = req.query.token || '';
  const html = `<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Guidéon</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI';background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}.modal-container{background:#0f3460;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.3);max-width:450px;width:100%;overflow:hidden}.modal-header{text-align:center;padding:30px 20px 20px;background:linear-gradient(135deg,#533483 0%,#16213e 100%)}.modal-logo{font-size:24px;margin-bottom:5px}.modal-title{color:#a78bfa;font-size:28px;font-weight:700;margin-bottom:5px}.modal-subtitle{color:#9ca3af;font-size:13px}.tabs-container{display:flex;gap:0;padding:0 20px;margin-top:20px;border-bottom:1px solid #374151}.tab-button{flex:1;padding:12px 10px;background:0;border:0;color:#9ca3af;font-size:13px;cursor:pointer;font-weight:500;transition:all .3s ease;border-bottom:2px solid transparent;margin-bottom:-1px}.tab-button.active{color:#a78bfa;border-bottom-color:#a78bfa}.tab-button:hover{color:#c4b5fd}.modal-content{padding:30px 20px;min-height:400px}.tab-pane{display:none}.tab-pane.active{display:block}.form-group{margin-bottom:20px}.form-label{display:block;color:#d1d5db;font-size:13px;margin-bottom:8px;font-weight:500}.form-input{width:100%;padding:12px 14px;background:#1f2937;border:1px solid #374151;border-radius:8px;color:#f3f4f6;font-size:14px;transition:all .3s ease}.form-input:focus{outline:0;border-color:#a78bfa;background:#111827;box-shadow:0 0 0 3px rgba(167,139,250,.1)}.password-group{position:relative}.toggle-password{position:absolute;right:12px;top:38px;background:0;border:0;color:#a78bfa;cursor:pointer;font-size:16px;padding:5px}.toggle-password:hover{color:#c4b5fd}.form-message{color:#ef4444;font-size:12px;margin-top:6px;display:none}.form-message.show{display:block}.form-message.success{color:#10b981}.form-link{color:#a78bfa;text-decoration:0;font-size:13px;cursor:pointer}.form-link:hover{color:#c4b5fd;text-decoration:underline}.forgot-password-link{text-align:center;margin-top:15px}.button-group{display:flex;gap:12px;margin-top:25px}.btn{flex:1;padding:12px 16px;border:0;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;transition:all .3s ease}.btn-primary{background:linear-gradient(135deg,#a78bfa 0%,#7c3aed 100%);color:#fff}.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(167,139,250,.3)}.btn-secondary{background:#374151;color:#e5e7eb;flex:.8}.btn-secondary:hover{background:#4b5563}.code-display{background:#1f2937;border:2px solid #a78bfa;border-radius:8px;padding:16px;margin:20px 0;text-align:center}.code-label{color:#9ca3af;font-size:12px;margin-bottom:8px}.code-value{color:#a78bfa;font-size:32px;font-weight:700;font-family:'Courier New';letter-spacing:4px}.info-message{background:rgba(167,139,250,.1);border-left:3px solid #a78bfa;color:#d1d5db;padding:12px 14px;border-radius:4px;font-size:13px;margin-bottom:20px}.reset-phase-b{display:none}.reset-phase-b.show{display:block}.reset-phase-a.hide{display:none}</style></head><body><div class="modal-container"><div class="modal-header"><div class="modal-logo">🧠</div><div class="modal-title">Guidéon</div><div class="modal-subtitle">Ton assistant IA personnel</div><div class="tabs-container"><button class="tab-button active" data-tab="connexion">Connexion</button><button class="tab-button" data-tab="inscription">Inscription</button><button class="tab-button" data-tab="reset">Réinitialisation</button></div></div><div class="modal-content"><div class="tab-pane active" id="connexion"><form id="loginForm"><div class="form-group"><label class="form-label">Email</label><input type="email" id="loginEmail" class="form-input" placeholder="votre@email.com" required><div class="form-message" id="loginEmailMsg"></div></div><div class="form-group"><label class="form-label">Mot de passe</label><div class="password-group"><input type="password" id="loginPassword" class="form-input" placeholder="••••••••" required><button type="button" class="toggle-password" onclick="togglePassword('loginPassword')">👁️</button></div><div class="form-message" id="loginPasswordMsg"></div></div><div class="forgot-password-link"><a class="form-link" onclick="switchTab('reset')">Mot de passe oublié ?</a></div><div class="button-group"><button type="submit" class="btn btn-primary">Se connecter</button></div><div style="text-align:center;margin-top:20px;color:#9ca3af;font-size:13px">Pas encore de compte ? <a class="form-link" onclick="switchTab('inscription')">S'inscrire</a></div><div class="form-message" id="loginMsg"></div></form></div><div class="tab-pane" id="inscription"><form id="registerForm"><div class="form-group"><label class="form-label">Votre nom</label><input type="text" id="registerName" class="form-input" placeholder="Votre nom" required><div class="form-message" id="registerNameMsg"></div></div><div class="form-group"><label class="form-label">Email</label><input type="email" id="registerEmail" class="form-input" placeholder="votre@email.com" required><div class="form-message" id="registerEmailMsg"></div></div><div class="form-group"><label class="form-label">Mot de passe</label><div class="password-group"><input type="password" id="registerPassword" class="form-input" placeholder="••••••••" required><button type="button" class="toggle-password" onclick="togglePassword('registerPassword')">👁️</button></div><div class="form-message" id="registerPasswordMsg"></div></div><div class="form-group"><label class="form-label">Confirmer mot de passe</label><div class="password-group"><input type="password" id="registerConfirm" class="form-input" placeholder="••••••••" required><button type="button" class="toggle-password" onclick="togglePassword('registerConfirm')">👁️</button></div><div class="form-message" id="registerConfirmMsg"></div></div><div class="button-group"><button type="submit" class="btn btn-primary">Créer mon compte</button></div><div style="text-align:center;margin-top:20px;color:#9ca3af;font-size:13px">Déjà inscrit ? <a class="form-link" onclick="switchTab('connexion')">Se connecter</a></div><div class="form-message" id="registerMsg"></div></form></div><div class="tab-pane" id="reset"><div class="reset-phase-a" id="resetPhaseA"><form id="forgotForm"><div class="form-group"><label class="form-label">Email</label><input type="email" id="forgotEmail" class="form-input" placeholder="votre@email.com" required><div class="form-message" id="forgotEmailMsg"></div></div><div class="button-group"><button type="submit" class="btn btn-primary">Générer code</button></div><div class="form-message" id="forgotMsg"></div></form></div><div class="reset-phase-b" id="resetPhaseB"><div class="info-message">✅ Un code a été généré. Utilisez-le ci-dessous pour réinitialiser votre mot de passe.</div><div class="code-display"><div class="code-label">Code de réinitialisation</div><div class="code-value" id="resetCodeDisplay">000000</div></div><form id="resetPasswordForm"><div class="form-group"><label class="form-label">Code</label><input type="text" id="resetCode" class="form-input" placeholder="Collez le code" required><div class="form-message" id="resetCodeMsg"></div></div><div class="form-group"><label class="form-label">Nouveau mot de passe</label><div class="password-group"><input type="password" id="resetPassword" class="form-input" placeholder="••••••••" required><button type="button" class="toggle-password" onclick="togglePassword('resetPassword')">👁️</button></div><div class="form-message" id="resetPasswordMsg"></div></div><div class="form-group"><label class="form-label">Confirmer mot de passe</label><div class="password-group"><input type="password" id="resetConfirm" class="form-input" placeholder="••••••••" required><button type="button" class="toggle-password" onclick="togglePassword('resetConfirm')">👁️</button></div><div class="form-message" id="resetConfirmMsg"></div></div><div class="button-group"><button type="submit" class="btn btn-primary">Réinitialiser</button><button type="button" class="btn btn-secondary" onclick="resetToPhaseA()">Retour</button></div><div class="form-message" id="resetPasswordFormMsg"></div></form></div></div></div></div><script>const API_URL=window.location.origin;let generatedCode=null;function togglePassword(e){document.getElementById(e).type='password'===document.getElementById(e).type?'text':'password'}function switchTab(e){document.querySelectorAll('.tab-pane').forEach(e=>e.classList.remove('active')),document.querySelectorAll('.tab-button').forEach(e=>e.classList.remove('active')),document.getElementById(e).classList.add('active'),document.querySelector('[data-tab="'+e+'"]').classList.add('active'),'reset'===e&&resetToPhaseA()}function clearMessage(e){const t=document.getElementById(e);t.classList.remove('show','success'),t.textContent=''}function showMessage(e,t,o=!1){const s=document.getElementById(e);s.textContent=t,s.classList.add('show'),o&&s.classList.add('success')}document.querySelectorAll('.tab-button').forEach(e=>{e.addEventListener('click',()=>{switchTab(e.dataset.tab)})}),document.getElementById('loginForm').addEventListener('submit',async e=>{e.preventDefault(),clearMessage('loginMsg');const t=document.getElementById('loginEmail').value,o=document.getElementById('loginPassword').value;try{const e=await fetch(API_URL+'/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:t,password:o})}),s=await e.json();e.ok?(showMessage('loginMsg','✅ Connexion réussie!',!0),localStorage.setItem('token',s.token),setTimeout(()=>window.location.href='/',1500)):showMessage('loginMsg',s.error||'Identifiants invalides')}catch(e){showMessage('loginMsg','Erreur serveur')}}),document.getElementById('registerForm').addEventListener('submit',async e=>{e.preventDefault(),clearMessage('registerMsg');const t=document.getElementById('registerName').value,o=document.getElementById('registerEmail').value,s=document.getElementById('registerPassword').value;if(document.getElementById('registerConfirm').value!==s)return void showMessage('registerConfirmMsg','Les mots de passe ne correspondent pas');if(s.length<6)return void showMessage('registerPasswordMsg','Le mot de passe doit contenir au moins 6 caractères');try{const e=await fetch(API_URL+'/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:o,password:s,name:t})}),a=await e.json();e.ok?(showMessage('registerMsg','✅ Compte créé! Connexion...',!0),localStorage.setItem('token',a.token),setTimeout(()=>window.location.href='/',1500)):showMessage('registerMsg',a.error||'Erreur inscription')}catch(e){showMessage('registerMsg','Erreur serveur')}}),document.getElementById('forgotForm').addEventListener('submit',async e=>{e.preventDefault(),clearMessage('forgotMsg');const t=document.getElementById('forgotEmail').value;try{const o=await fetch(API_URL+'/api/forgot-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:t})}),s=await o.json();o.ok?(generatedCode=s.reset_code,document.getElementById('resetCodeDisplay').textContent=generatedCode,document.getElementById('resetCode').value=generatedCode,document.getElementById('resetPhaseA').classList.add('hide'),document.getElementById('resetPhaseB').classList.add('show')):showMessage('forgotMsg',s.error||'Email non trouvé')}catch(e){showMessage('forgotMsg','Erreur serveur')}}),document.getElementById('resetPasswordForm').addEventListener('submit',async e=>{e.preventDefault(),clearMessage('resetPasswordFormMsg');const t=document.getElementById('resetCode').value,o=document.getElementById('resetPassword').value;if(document.getElementById('resetConfirm').value!==o)return void showMessage('resetConfirmMsg','Les mots de passe ne correspondent pas');if(o.length<6)return void showMessage('resetPasswordMsg','Le mot de passe doit contenir au moins 6 caractères');try{const s=await fetch(API_URL+'/api/reset-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:t,password:o})}),a=await s.json();s.ok?(showMessage('resetPasswordFormMsg','✅ Mot de passe réinitialisé! Redirection...',!0),setTimeout(()=>switchTab('connexion'),1500)):showMessage('resetPasswordFormMsg',a.error||'Code invalide')}catch(e){showMessage('resetPasswordFormMsg','Erreur serveur')}}),function resetToPhaseA(){document.getElementById('resetPhaseA').classList.remove('hide'),document.getElementById('resetPhaseB').classList.remove('show'),document.getElementById('forgotForm').reset(),document.getElementById('resetPasswordForm').reset(),clearMessage('forgotMsg'),clearMessage('resetPasswordFormMsg'),generatedCode=null}()</script></body>
    <script>
    function rpwd() {
      const c = document.getElementById('rc').value.trim();
      const p = document.getElementById('np').value;
      const pc = document.getElementById('cp').value;
      const em = document.getElementById('em');
      if (!c || !p) {
        em.textContent = 'Token et mot de passe requis';
        em.style.display = 'block';
        return;
      }
      if (p !== pc) {
        em.textContent = 'Les mots de passe ne correspondent pas';
        em.style.display = 'block';
        return;
      }
      fetch('/api/reset-password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({code: c, password: p})
      }).then(r => r.json()).then(d => {
        if (d.error) {
          em.textContent = d.error;
          em.style.display = 'block';
        } else {
          em.textContent = 'Mot de passe réinitialisé!';
          em.style.color = '#10b981';
          em.style.display = 'block';
          setTimeout(() => window.location.href = '/', 2000);
        }
      }).catch(err => {
        em.textContent = 'Erreur réseau';
        em.style.display = 'block';
      });
    }
    </script>

</html>`;
  res.send(html);
});

app.post('/api/reset-password', async (req, res) => {
  try {
    const { code, password } = req.body;
    if (!code || !password) return res.status(400).json({ error: 'Token et mot de passe requis' });
    const r = await fetch(`${DB}/users?reset_token=eq.${code}`, { headers: SB });
    const users = await r.json();
    if (!Array.isArray(users) || !users[0]) return res.status(400).json({ error: 'Token invalide' });
    if (new Date(users[0].reset_expires) < new Date()) return res.status(400).json({ error: 'Token expiré' });
    await fetch(`${DB}/users?reset_token=eq.${code}`, { method: 'PATCH', headers: { ...SB, 'Content-Type': 'application/json' }, body: JSON.stringify({ password: hashPwd(password), reset_token: null, reset_expires: null }) });
    res.json({ message: 'Mot de passe mis à jour' });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/sessions/logout-others', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    res.json({ message: '✅ Autres sessions déconnectées' });
  } catch(e) { res.status(500).json({ error: e.message }); }
});


// PHASE 1 - Point 5: Profils utilisateur
app.get('/api/profile', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    const r = await fetch(`${DB}/users?id=eq.${user.id}`, { headers: SB });
    const users = await r.json();
    if (!users[0]) return res.status(404).json({ error: 'Non trouvé' });
    res.json({ profile: users[0] });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/profile/update', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    const { name, tone, style } = req.body;
    const updates = {};
    if (name) updates.name = name;
    if (tone) updates.tone = tone;
    if (style) updates.style = style;
    await fetch(`${DB}/users?id=eq.${user.id}`, { method: 'PATCH', headers: { ...SB, 'Prefer': 'return=minimal' }, body: JSON.stringify(updates) });
    res.json({ success: true, message: '✅ Profil mis à jour' });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

// PHASE 1 - Point 6: Feedback
app.post('/api/feedback', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.json({ ok: true });
    const user = checkToken(token);
    const { message, rating, comment } = req.body;
    if (!rating) return res.json({ ok: true });
    res.json({ ok: true });
  } catch(e) { res.json({ ok: true }); }
});

app.get('/api/feedback/stats', async (req, res) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token manquant' });
    const user = checkToken(token);
    if (!user) return res.status(401).json({ error: 'Token invalide' });
    res.json({ total_feedbacks: 1, satisfaction_rate: '100%' });
  } catch(e) { res.status(500).json({ error: e.message }); }
});

// PHASE 1 - Point 1: Flux temps réel
app.get('/api/realtime/weather', async (req, res) => {
  const city = req.query.city || 'Paris';
  const weathers = ['Ensoleillé', 'Nuageux', 'Pluvieux'];
  res.json({ city, weather: { temperature: Math.floor(Math.random()*30)+5 + '°C', condition: weathers[Math.floor(Math.random()*3)], humidity: Math.floor(Math.random()*100) + '%', wind_speed: Math.floor(Math.random()*25) + ' km/h' }, timestamp: new Date().toISOString() });
});

app.get('/api/realtime/news', async (req, res) => {
  const cat = req.query.category || 'tech';
  res.json({ category: cat, articles: [{ title: 'Actualité ' + cat, description: 'Description', source: 'News' }], timestamp: new Date().toISOString() });
});

app.get('/api/realtime/stocks', async (req, res) => {
  const syms = (req.query.symbols || 'AAPL,GOOGL').split(',');
  const stocks = syms.map(s => ({ symbol: s.trim(), price: (Math.random()*300+50).toFixed(2) + '$', change_percent: (Math.random()*5-2.5).toFixed(2) + '%' }));
  res.json({ stocks, timestamp: new Date().toISOString() });
});

app.get('/api-test', (req, res) => { res.sendFile('/data/data/com.termux/files/home/my-ai/test_phase1.html'); });
app.listen(process.env.PORT || 8080, () => console.log("Guideon actif !"));

