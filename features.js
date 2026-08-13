// Rapport de confidentialité
document.addEventListener('DOMContentLoaded', () => {
  const privacyBtn = document.querySelector('[onclick*="Rapport"]') || 
                     document.querySelector('button:contains("Rapport")');
  
  if (privacyBtn) {
    privacyBtn.onclick = async () => {
      const token = localStorage.getItem('gtoken');
      if (!token) return alert('Token manquant');
      
      const response = await fetch('/api/privacy-report', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'rapport_confidentialite.pdf';
      a.click();
    };
  }
  
  // Vérifier les mises à jour
  const updateBtn = document.querySelector('button:contains("Vérifier")');
  if (updateBtn) {
    updateBtn.onclick = async () => {
      const res = await fetch('/api/version');
      const data = await res.json();
      alert(`Version: ${data.current}\nDernière: ${data.latest}\nMise à jour: ${data.updateAvailable ? 'Oui' : 'Non'}`);
    };
  }
});
