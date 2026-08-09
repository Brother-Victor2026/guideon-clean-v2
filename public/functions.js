async function toggleShare(){if(!confirm("Modifier la permission de partage ?"))return;const tok=localStorage.getItem("gtoken");const share_enabled=document.getElementById("shareControl").checked;try{const r=await fetch("/api/share/preference",{method:"POST",headers:{"Authorization":"Bearer "+tok,"Content-Type":"application/json"},body:JSON.stringify({share_enabled})});const d=await r.json();if(d.success){alert(d.message||"✅ Partage mis à jour");location.reload();}else alert("❌ "+d.error);}catch(e){alert("Erreur: "+e.message);}}
async function createNewAccount(){if(!confirm("Vous allez être déconnecté(e). Continuer ?"))return;const tok=localStorage.getItem("gtoken");try{await fetch("/api/auth/logout",{method:"POST",headers:{"Authorization":"Bearer "+tok}});}catch(e){}localStorage.removeItem("gtoken");localStorage.removeItem("gname");document.getElementById("prof").style.display="none";document.getElementById("authModal").scrollIntoView({behavior:"smooth"});stab("reg");location.reload();}
function switchToRegistration(){if(!confirm("Créer un nouveau compte ? Vous allez être déconnecté(e)."))return;const tok=localStorage.getItem("gtoken");try{fetch("/api/auth/logout",{method:"POST",headers:{"Authorization":"Bearer "+tok}});}catch(e){}localStorage.removeItem("gtoken");localStorage.removeItem("gname");document.getElementById("prof").style.display="none";document.getElementById("authModal").scrollIntoView({behavior:"smooth"});stab("reg");location.reload();}

// Afficher le rapport de confidentialité dans un modal
async function downloadPrivacyReport() {
  try {
    const tok = localStorage.getItem("gtoken");
    const res = await fetch('/api/privacy-report', {
      method: 'GET',
      headers: { "Authorization": "Bearer " + tok }
    });
    
    if (!res.ok) {
      alert("❌ Erreur: " + res.statusText);
      return;
    }
    
    const blob = await res.blob();
    const text = await blob.text();
    
    // Afficher les données dans le modal
    const contentDiv = document.getElementById('privacyContent');
    contentDiv.innerHTML = `
      <h4 style="color:#a78bfa;margin:12px 0 8px 0;">👤 Informations Utilisateur</h4>
      <p>${text.split('\n')[1] || 'Email: -'}</p>
      <p>${text.split('\n')[2] || 'Nom: -'}</p>
      
      <h4 style="color:#a78bfa;margin:12px 0 8px 0;">📊 Statistiques</h4>
      <p>${text.split('\n')[4] || 'Total conversations: -'}</p>
      
      <h4 style="color:#a78bfa;margin:12px 0 8px 0;">🔒 Engagement</h4>
      <p>✓ Aucune donnée personnelle vendue à des tiers<br>
      ✓ Chiffrement end-to-end disponible<br>
      ✓ Droits RGPD & CCPA garantis<br>
      ✓ Données supprimées après 90 jours inactifs</p>
    `;
    
    // Afficher le modal
    document.getElementById('privacyModal').style.display = 'flex';
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}

// Télécharger le PDF
async function downloadPrivacyPDF() {
  try {
    const tok = localStorage.getItem("gtoken");
    const res = await fetch('/api/privacy-report', {
      method: 'GET',
      headers: { "Authorization": "Bearer " + tok }
    });
    
    if (!res.ok) {
      alert("❌ Erreur: " + res.statusText);
      return;
    }
    
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'rapport-confidentialite.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}

// Vérifier et afficher les mises à jour
async function checkUpdates() {
  try {
    const tok = localStorage.getItem("gtoken");
    const res = await fetch('/api/version', {
      method: 'GET',
      headers: { "Authorization": "Bearer " + tok }
    });
    
    if (!res.ok) {
      alert("❌ Erreur: " + res.statusText);
      return;
    }
    
    const data = await res.json();
    const tabContent = document.getElementById('tab-updates');
    if (!tabContent) {
      alert("❌ Section mises à jour non trouvée");
      return;
    }
    
    let html = `<h4 style="color:#a78bfa;">📦 Mises à jour</h4>`;
    
    if (data.updateAvailable) {
      html += `
        <div style="background:#0f0f1a;border:1px solid #7c3aed;border-radius:8px;padding:12px;margin-bottom:16px;">
          <p style="color:#a78bfa;font-size:13px;font-weight:bold;margin:0 0 6px 0;">✨ Version ${data.latest} - ${data.releaseDate || 'Date non disponible'}</p>
          <p style="color:#9ca3af;font-size:12px;margin:0 0 8px 0;">🎉 Nouvelles fonctionnalités disponibles</p>
          <ul style="color:#9ca3af;font-size:12px;margin:6px 0;padding-left:20px;">
            ${data.changelog.map(c => `<li>${c}</li>`).join('')}
          </ul>
          <button onclick="location.reload()" style="width:100%;padding:8px;background:#7c3aed;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-top:8px;">🔄 Actualiser</button>
        </div>
      `;
    } else {
      html += `
        <div style="background:#0f0f1a;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:16px;">
          <p style="color:#10b981;font-size:13px;font-weight:bold;">✅ Vous avez la dernière version: ${data.current}</p>
          <p style="color:#9ca3af;font-size:12px;">📅 ${data.releaseDate || 'Date non disponible'}</p>
        </div>
      `;
    }
    
    html += `
      <h4 style="color:#a78bfa;">Vérification</h4>
      <button onclick="checkUpdates()" style="width:100%;padding:10px;background:#1e3a8a;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-bottom:8px;">🔄 Vérifier à nouveau</button>
      <label style="color:#9ca3af;font-size:12px;display:flex;align-items:center;gap:8px;margin-top:12px;">
        <input type="checkbox" id="autoUpdate" checked> Mises à jour automatiques
      </label>
    `;
    
    tabContent.innerHTML = html;
  } catch (e) {
    alert("❌ Erreur: " + e.message);
  }
}

// Variables globales
let selectedCategory = null;
let pendingCategory = null;

// Ouvrir l'interface de création
function createNewProject() {
  document.getElementById('createProjectInterface').style.display = 'flex';
  selectedCategory = null;
  pendingCategory = null;
  document.getElementById('projectMainInput').value = '';
  document.getElementById('projectDesc').value = '';
  document.querySelector('input[name="newProjectMode"][value="default"]').checked = true;
  document.querySelectorAll('.categoryBtn').forEach(btn => {
    btn.style.background = '#2d1b69';
    btn.style.color = '#fff';
  });
}

// Fermer l'interface de création
function closeCreateProjectInterface() {
  document.getElementById('createProjectInterface').style.display = 'none';
}

// Sélectionner une catégorie - afficher modale de confirmation
function selectCategory(category, button) {
  pendingCategory = category;
  const categoryNames = {
    'devoirs': '🏠 Devoirs',
    'investissement': '💰 Investissement',
    'ecriture': '✏️ Écriture',
    'sante': '🏥 Santé',
    'voyages': '✈️ Voyages',
    'autre': '🎯 Autre'
  };
  
  document.getElementById('confirmCategoryText').textContent = 'Sélectionner: ' + categoryNames[category] + ' ?';
  document.getElementById('confirmCategoryModal').style.display = 'flex';
}

// Confirmer la catégorie
function confirmCategory() {
  if (!pendingCategory) return;
  
  selectedCategory = pendingCategory;
  document.getElementById('projectMainInput').value = selectedCategory;
  document.querySelectorAll('.categoryBtn').forEach(btn => {
    btn.style.background = '#2d1b69';
    btn.style.color = '#fff';
  });
  
  const btn = document.querySelector('.categoryBtn[onclick*="' + selectedCategory + '"]');
  if (btn) {
    btn.style.background = '#a78bfa';
    btn.style.color = '#000';
  }
  
  closeConfirmCategory();
}

// Fermer modale confirmation
function closeConfirmCategory() {
  document.getElementById('confirmCategoryModal').style.display = 'none';
  pendingCategory = null;
}

// Sauvegarder le nouveau projet
function saveNewProject() {
  const name = document.getElementById('projectMainInput').value.trim();
  const desc = document.getElementById('projectDesc').value.trim();
  const mode = document.querySelector('input[name="newProjectMode"]:checked').value;
  
  if (!name) {
    alert('❌ Le nom du projet est obligatoire!');
    return;
  }
  
  if (!selectedCategory) {
    alert('❌ Sélectionne une catégorie!');
    return;
  }
  
  let projects = JSON.parse(localStorage.getItem('guideonProjects') || '[]');
  const newProject = {
    id: Date.now(),
    name: name,
    category: selectedCategory,
    description: desc,
    mode: mode,
    createdAt: new Date().toLocaleDateString('fr-FR')
  };
  
  projects.push(newProject);
  localStorage.setItem('guideonProjects', JSON.stringify(projects));
  
  document.getElementById('projectCreatedName').textContent = '📂 Nom: ' + name + ' | 📁 Catégorie: ' + selectedCategory;
  document.getElementById('projectCreatedModal').style.display = 'flex';
}

// Afficher mes projets - VRAIE INTERFACE
function showMyProjects() {
  const projects = JSON.parse(localStorage.getItem('guideonProjects') || '[]');
  const container = document.getElementById('projectsListContainer');
  
  if (projects.length === 0) {
    container.innerHTML = '<p style="color:#9ca3af;font-size:13px;text-align:center;">📂 Aucun projet créé.<br><br>Clique sur "Créer un nouveau projet" pour en créer un!</p>';
    document.getElementById('myProjectsModal').style.display = 'flex';
    return;
  }
  
  let html = '<div style="color:#9ca3af;font-size:12px;">';
  projects.forEach((proj, idx) => {
    html += '<div style="background:#1a1a2e;border:1px solid #2d1b69;border-radius:8px;padding:12px;margin-bottom:10px;">';
    html += '<div style="color:#a78bfa;font-weight:bold;margin-bottom:6px;">' + (idx + 1) + '. ' + proj.name + '</div>';
    html += '<div style="margin-bottom:4px;">📁 <strong>' + proj.category + '</strong> | 📅 ' + proj.createdAt + '</div>';
    if (proj.description) {
      html += '<div style="margin-bottom:4px;">📝 ' + proj.description + '</div>';
    }
    html += '<div style="margin-bottom:8px;">⚙️ Mode: ' + (proj.mode === 'default' ? 'Par défaut' : 'Projet seulement') + '</div>';
    html += '<button onclick="deleteProject(' + proj.id + ')" style="padding:6px 10px;background:#c7372f;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:11px;">🗑️ Supprimer</button>';
    html += '</div>';
  });
  html += '</div>';
  
  container.innerHTML = html;
  document.getElementById('myProjectsModal').style.display = 'flex';
}

// Supprimer un projet
function deleteProject(id) {
  if (confirm('❌ Supprimer ce projet?')) {
    let projects = JSON.parse(localStorage.getItem('guideonProjects') || '[]');
    projects = projects.filter(p => p.id !== id);
    localStorage.setItem('guideonProjects', JSON.stringify(projects));
    showMyProjects();
  }
}

// Fermer modale voir projets
function closeMyProjectsModal() {
  document.getElementById('myProjectsModal').style.display = 'none';
}

// Sauvegarder le mode de projet
function saveProjectMode(mode) {
  localStorage.setItem('projectMode', mode);
}

// Charger le mode au démarrage
document.addEventListener('DOMContentLoaded', () => {
  const savedMode = localStorage.getItem('projectMode') || 'default';
  const radioBtn = document.querySelector('input[name="projectMode"][value="' + savedMode + '"]');
  if (radioBtn) radioBtn.checked = true;
});


// Fermer modale projet créé
function closeProjectCreatedModal() {
  document.getElementById('projectCreatedModal').style.display = 'none';
  closeCreateProjectInterface();
}

// Annuler et revenir à la création
function cancelProjectCreation() {
  document.getElementById('projectCreatedModal').style.display = 'none';
}

