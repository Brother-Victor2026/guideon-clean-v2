// Ajoute les listeners de sauvegarde localStorage APRÈS le chargement du DOM
document.addEventListener('DOMContentLoaded', function() {
  const checkboxMap = {
    'tmpChat': 'tmpChat',
    'shareControl': 'shareControl',
    'allowPublicShare': 'allowPublicShare',
    'allowCollabShare': 'allowCollabShare',
    'analyticsConsent': 'analyticsConsent',
    'cloudBackup': 'cloudBackup',
    'deleteHistoryAuto': 'deleteHistoryAuto',
    'autoUpdate': 'autoUpdate'
  };

  for (const [elementId, storageKey] of Object.entries(checkboxMap)) {
    const element = document.getElementById(elementId);
    if (element) {
      element.addEventListener('change', function() {
        localStorage.setItem(storageKey, this.checked);
      });
    }
  }
});
