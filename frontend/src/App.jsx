import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, User, Bot, Sparkles } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || `http://${window.location.hostname}:8000`;

function App() {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('febe_chat_history');
    return saved ? JSON.parse(saved) : [];
  });
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    localStorage.setItem('febe_chat_history', JSON.stringify(messages));
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          history: messages
        })
      });

      const data = await response.json();
      if (data.response) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      } else {
        throw new Error(data.detail || 'Resposta inválida da API');
      }
    } catch (error) {
      console.error('Erro:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: `Ops! Algo deu errado: ${error.message}. Tente novamente em instantes.` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="logo-section">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            Agente Febe
          </motion.h1>
          <p>CMO de Elite: Maquiagem e Beleza</p>
        </div>
        <div className="status-badge">
          <Sparkles size={20} color="var(--primary)" />
        </div>
      </header>

      <div className="chat-window">
        {messages.length === 0 && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="welcome-msg"
            style={{ textAlign: 'center', marginTop: '40px', color: 'var(--text-dim)' }}
          >
            <Bot size={48} style={{ marginBottom: '16px', color: 'var(--primary)' }} />
            <h2>Olá! Eu sou a Febe.</h2>
            <p>Como posso ajudar a viralizar o seu talento hoje?</p>
          </motion.div>
        )}

        <AnimatePresence>
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.3 }}
              className={`message ${msg.role}`}
            >
              {msg.role === 'user' ? <User size={14} style={{ marginBottom: '4px' }} /> : <Bot size={14} style={{ marginBottom: '4px' }} />}
              <div className="msg-content">
                {msg.content.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <div className="message assistant loading">
            <div className="loading-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form className="input-area" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Peça sua estratégia de marketing de beleza..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          {isLoading ? '...' : <Send size={20} />}
        </button>
      </form>
    </div>
  );
}

export default App;
