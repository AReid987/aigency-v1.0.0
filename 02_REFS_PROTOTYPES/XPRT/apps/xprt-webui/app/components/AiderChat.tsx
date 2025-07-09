// apps/lead-agent/components/AiderChat.tsx
'use client';

import { useEffect, useRef, useState } from 'react';

export default function AiderChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const ws = useRef<WebSocket>();

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/aider');
    
    ws.current.onmessage = (event) => {
      setMessages(prev => [...prev, {role: 'ai', content: event.data}]);
    };

    return () => ws.current?.close();
  }, []);

  const sendMessage = () => {
    ws.current?.send(input);
    setMessages(prev => [...prev, {role: 'user', content: input}]);
    setInput('');
  };

  return (
    <div className="aider-chat">
      {/* Chat UI Implementation */}
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
      <div>
        {messages.map((msg, index) => (
          <div key={index} className={msg.role}>{msg.content}</div>
        ))}
      </div>
    </div>
  );
}