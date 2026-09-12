import fs from 'fs';
import { execSync } from 'child_process';

try {
  const diff = execSync('git diff --stat HEAD').toString();
  const additions = parseInt(diff.match(/\d+ insertions/)?.[0]?.match(/\d+/)?.[0] || 0);
  const deletions = parseInt(diff.match(/\d+ deletions/)?.[0]?.match(/\d+/)?.[0] || 0);
  
  const pkg = JSON.parse(fs.readFileSync('./package.json', 'utf8'));
  const [major, minor, patch] = pkg.version.split('.').map(Number);
  let newVersion;
  
  if (additions > deletions * 2) {
    newVersion = `${major}.${minor + 1}.0`;
  } else {
    newVersion = `${major}.${minor}.${patch + 1}`;
  }
  
  pkg.version = newVersion;
  fs.writeFileSync('./package.json', JSON.stringify(pkg, null, 2) + '\n');
  
  const history = JSON.parse(fs.readFileSync('./version-history.json', 'utf8'));
  history.current_version = newVersion;
  history.last_update = new Date().toLocaleString('fr-FR');
  history.history.unshift({version: newVersion, date: new Date().toLocaleString('fr-FR'), type: 'auto', changes: 'Auto-update'});
  fs.writeFileSync('./version-history.json', JSON.stringify(history, null, 2) + '\n');
  
  console.log(`✅ Version updated to ${newVersion}`);
  
  // Mettre à jour aussi le HTML avec la nouvelle version et date
  const htmlPath = './public/index.html';
  let html = fs.readFileSync(htmlPath, 'utf-8');
  const dateStr = new Date().toLocaleString('fr-FR');
  const [datePart, timePart] = dateStr.split(' ');
  
  html = html.replace(/id="latestVersion">\d+\.\d+\.\d+<\/span>/g, `id="latestVersion">${newVersion}</span>`);
  html = html.replace(/id="updateDate">[^<]+<\/span>/g, `id="updateDate">${datePart}</span>`);
  html = html.replace(/id="updateTime">[^<]+<\/span>/g, `id="updateTime">${timePart}</span>`);
  
  fs.writeFileSync(htmlPath, html, 'utf-8');
  console.log(`✅ HTML version updated to ${newVersion}`);
} catch (e) {
  console.log('Auto-version ready');
}
