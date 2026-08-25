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

function initCheckboxes() {
  // Restaurer depuis localStorage
  for (const [elementId, storageKey] of Object.entries(checkboxMap)) {
    const element = document.getElementById(elementId);
    if (element) {
      const stored = localStorage.getItem(storageKey);
      if (stored === 'true') element.checked = true;
      if (stored === 'false') element.checked = false;
      
      // Ajouter listener de sauvegarde
      element.addEventListener('change', function() {
        localStorage.setItem(storageKey, this.checked);
      });
    }
  }
}

// Exécuter au bon moment
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCheckboxes);
} else {
  setTimeout(initCheckboxes, 100);
}
