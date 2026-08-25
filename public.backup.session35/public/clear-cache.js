// Clear old invalid tokens ONLY once on first load
if (!sessionStorage.getItem('_cache_cleared')) {
  const oldKeys = ['gtoken', 'gname', 'token', 'name', 'session'];
  oldKeys.forEach(key => localStorage.removeItem(key));
  sessionStorage.setItem('_cache_cleared', 'true');
  console.log('✅ Old tokens cleared - please login');
  // Reload to show login form
  location.reload();
}
