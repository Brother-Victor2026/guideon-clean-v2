// Force clear old invalid tokens
const oldKeys = ['gtoken', 'gname', 'token', 'name', 'session'];
oldKeys.forEach(key => localStorage.removeItem(key));
console.log('✅ Old tokens cleared - please login again');
