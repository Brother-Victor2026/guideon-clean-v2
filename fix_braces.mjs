import fs from 'fs';

let content = fs.readFileSync('public/voice-modal.js', 'utf8');

// Supprimer les deux accolades mal placées
const bad = `      const reply = data.reply || '';
      }
    }

    console.log('📖 Réponse reçue:', reply.substring(0, 50));`;

const good = `      const reply = data.reply || '';

    console.log('📖 Réponse reçue:', reply.substring(0, 50));`;

if (content.includes(bad)) {
  content = content.replace(bad, good);
  fs.writeFileSync('public/voice-modal.js', content);
  console.log('✅ Accolades supprimées');
} else {
  console.log('❌ Pattern pas trouvé');
}
