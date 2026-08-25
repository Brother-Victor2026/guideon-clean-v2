// Ajoute les listeners de sauvegarde localStorage à TOUTES les checkboxes
const checkboxMap = {
  'tmpChat': 'tmpChat',
  'notifCheck': 'gnotif',
  'shareControl': 'shareControl',
  'allowPublicShare': 'allowPublicShare',
  'allowCollabShare': 'allowCollabShare',
  'analyticsConsent': 'analyticsConsent',
  'cloudBackup': 'cloudBackup',
  'deleteHistoryAuto': 'deleteHistoryAuto',
  'autoUpdate': 'autoUpdate'
};

function attachCheckboxListeners() {
  for (const [elementId, storageKey] of Object.entries(checkboxMap)) {
    const element = document.getElementById(elementId);
    if (element) {
      element.addEventListener('change', function() {
        localStorage.setItem(storageKey, this.checked);
      });
    }
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', attachCheckboxListeners);
} else {
  attachCheckboxListeners();
}
