const fs = require('fs');
let code = fs.readFileSync('server.mjs', 'utf-8');

// 1️⃣ Ajouter isSearchQuery après checkToken
const checkTokenEnd = code.indexOf('  } catch { return null; }\n}');
const insertAfterCheckToken = code.indexOf('\n\nfunction getQuotaResetTime', checkTokenEnd);
const isSearchQueryCode = `\nfunction isSearchQuery(message) {
  const searchWords = ['qui est', 'cherche', 'recherche', "c'est quoi", 'qui a', 'quel est', 'donne-moi', 'explique', 'raconte', 'comment', 'pourquoi'];
  return searchWords.some(w => message.toLowerCase().includes(w));
}`;
code = code.slice(0, insertAfterCheckToken) + isSearchQueryCode + code.slice(insertAfterCheckToken);

// 2️⃣ Ajouter let searchSources = null après let user = null
code = code.replace(
  /let user = null;/,
  "let user = null;\n    let searchSources = null;"
);

// 3️⃣ Ajouter code de recherche après if (token && DB)
const searchBlockCode = `
    // Détection et recherche en arrière-plan
    if (isSearchQuery(message)) {
      try {
        const searchRes = await fetch('http://localhost:8080/api/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: message })
        });
        const searchData = await searchRes.json();
        if (searchData.result) {
          searchSources = {
            duckduckgo: true,
            wikipedia: searchData.result.toLowerCase().includes('wikipedia') ? true : false
          };
        }
      } catch(e) { console.error('Search query error:', e.message); }
    }`;

code = code.replace(
  /    }\n    const timeWords/,
  "    }" + searchBlockCode + "\n    const timeWords"
);

// 4️⃣ Ajouter affichage des sources avant res.write({ done: true })
const sourcesDisplayCode = `
    // Ajouter les sources si présentes
    if (searchSources) {
      const sourceEmojis = {
        duckduckgo: '🔍 DuckDuckGo',
        wikipedia: '📚 Wikipedia'
      };
      const activeSources = Object.keys(searchSources)
        .filter(s => searchSources[s])
        .map(s => sourceEmojis[s])
        .join(' | ');
      
      if (activeSources) {
        res.write(\`data: \${JSON.stringify({ content: '\\n\\n**Sources:** ' + activeSources })}\\n\\n\`);
      }
    }`;

code = code.replace(
  /    res\.write\(\`data: \$\{JSON\.stringify\(\{ done: true \}\)\}\\n\\n\`\);/,
  sourcesDisplayCode + "\n    res.write(`data: ${JSON.stringify({ done: true })}\\n\\n`);"
);

fs.writeFileSync('server.mjs', code);
console.log('✅ Toutes les modifications appliquées!');
