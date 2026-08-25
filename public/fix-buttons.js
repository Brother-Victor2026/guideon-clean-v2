// FIX TOUS LES BOUTONS (sauf X)

// HAUT: 3 boutons
document.addEventListener('DOMContentLoaded', () => {
  // Bouton CC (gauche haut)
  document.querySelectorAll('button').forEach(btn => {
    if (btn.textContent.includes('🔤')) {
      btn.onclick = () => toggleCC();
    }
  });
  
  // Bouton Audio (milieu haut)
  document.querySelectorAll('button').forEach(btn => {
    if (btn.textContent.includes('🔊') && !btn.textContent.includes('Haut-parleur')) {
      btn.onclick = () => {
        const menu = document.getElementById('audioMenu');
        if (menu) menu.style.display = menu.style.display === 'none' ? 'flex' : 'none';
      };
    }
  });
  
  // Bouton Voix (droite haut)
  document.querySelectorAll('button').forEach(btn => {
    if (btn.textContent.includes('⚙️')) {
      btn.onclick = () => {
        const menu = document.getElementById('voiceMenu');
        if (menu) menu.style.display = menu.style.display === 'none' ? 'flex' : 'none';
      };
    }
  });
  
  // BAS: Bouton Micro (gauche)
  const micBtn = document.getElementById('voiceMicBtn');
  if (micBtn) {
    micBtn.onclick = () => {
      if (isGuideOnSpeaking) {
        stopGuideOnSpeaking();
      } else {
        startListening();
      }
    };
  }
  
  // BAS: Bouton Photo (milieu)
  document.querySelectorAll('button').forEach(btn => {
    if (btn.textContent === '⋯') {
      btn.onclick = () => showPhotoMenu();
    }
  });
});
