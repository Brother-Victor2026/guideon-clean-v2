import fs from 'fs';

const file = './public/index.html';
let content = fs.readFileSync(file, 'utf8');

const script = '<script src="clear-cache.js"></script>\n  ';
const pattern = /(\s*<head[^>]*>)/;

if (content.match(pattern)) {
  content = content.replace(pattern, '$1\n  ' + script);
  fs.writeFileSync(file, content);
  console.log('✅ clear-cache.js ajouté à index.html');
} else {
  console.log('❌ <head> non trouvé');
}
