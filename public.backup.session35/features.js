function attachHandlers() {
  const allButtons = document.querySelectorAll('button');
  let foundPrivacy = false, foundUpdate = false;
  
  allButtons.forEach(btn => {
    if (btn.textContent.includes('Rapport de confidentialité') && !foundPrivacy) {
      foundPrivacy = true;
      btn.onclick = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('gtoken');
        if (!token) return alert('Token manquant');
        try {
          const res = await fetch('/api/privacy-report', { headers: { 'Authorization': `Bearer ${token}` } });
          const blob = await res.blob();
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'rapport.pdf';
          a.click();
        } catch (e) { alert('Erreur: ' + e.message); }
      };
    }
    
    if (btn.textContent.includes('Vérifier les mises à jour') && !foundUpdate) {
      foundUpdate = true;
      btn.onclick = async (e) => {
        e.preventDefault();
        try {
          const res = await fetch('/api/version');
          const data = await res.json();
          alert(`Version: ${data.current}\nDernière: ${data.latest}\nUpdate: ${data.updateAvailable}`);
        } catch (e) { alert('Erreur: ' + e.message); }
      };
    }
  });
}

document.addEventListener('DOMContentLoaded', attachHandlers);
setTimeout(attachHandlers, 500);
setTimeout(attachHandlers, 1000);

new MutationObserver(attachHandlers).observe(document.body, { childList: true, subtree: true });
