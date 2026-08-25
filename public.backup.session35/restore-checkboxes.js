// Debug visible - affiche les valeurs restaurées
const debugDiv = document.createElement('div');
debugDiv.id = 'restore-debug';
debugDiv.style.cssText = 'position:fixed;top:0;right:0;background:rgba(0,0,0,0.8);color:#0f0;padding:10px;font-size:10px;max-width:200px;z-index:9999;display:none;';
document.body.appendChild(debugDiv);

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

function restoreAllCheckboxes() {
  let debug = 'RESTORE:\n';
  for (const [elementId, storageKey] of Object.entries(checkboxMap)) {
    const element = document.getElementById(elementId);
    if (!element) continue;
    const storedValue = localStorage.getItem(storageKey);
    if (storedValue !== null) {
      element.checked = storedValue === 'true';
      debug += `✅ ${elementId}=${storedValue}\n`;
    }
  }
  debugDiv.textContent = debug;
  debugDiv.style.display = 'block';
  setTimeout(() => debugDiv.style.display = 'none', 5000);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', restoreAllCheckboxes);
} else {
  restoreAllCheckboxes();
}
