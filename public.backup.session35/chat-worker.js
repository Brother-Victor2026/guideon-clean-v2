let responses = {};

self.onmessage = async (event) => {
  const { type, message, token, id } = event.data;
  
  if (type === 'SEND_MESSAGE') {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, history: [] })
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const text = decoder.decode(value);
        const lines = text.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) fullResponse += data.content;
            } catch(e) {}
          }
        }
      }
      
      responses[id] = fullResponse;
      self.postMessage({ type: 'RESPONSE_READY', id, response: fullResponse });
      
    } catch(e) {
      self.postMessage({ type: 'ERROR', id, error: e.message });
    }
  }
};
