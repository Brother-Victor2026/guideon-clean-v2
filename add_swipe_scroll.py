#!/usr/bin/env python3

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter le script de swipe avant </body>
swipe_script = '''<script>
(function() {
  const chatDiv = document.getElementById('chat');
  if (!chatDiv) return;
  
  let touchStartY = 0;
  let touchEndY = 0;
  
  chatDiv.addEventListener('touchstart', (e) => {
    touchStartY = e.changedTouches[0].screenY;
  }, false);
  
  chatDiv.addEventListener('touchend', (e) => {
    touchEndY = e.changedTouches[0].screenY;
    handleSwipe();
  }, false);
  
  function handleSwipe() {
    const diff = touchStartY - touchEndY;
    const threshold = 50;
    
    if (Math.abs(diff) > threshold) {
      if (diff > 0) {
        // Swipe vers le haut = scroll vers le bas
        chatDiv.scrollTop += 100;
      } else {
        // Swipe vers le bas = scroll vers le haut
        chatDiv.scrollTop -= 100;
      }
    }
  }
})();
</script>'''

content = content.replace('</body>', swipe_script + '\n</body>')

with open('/data/data/com.termux/files/home/my-ai/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Swipe scroll ajouté!")
