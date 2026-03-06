import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

const COMMON_QUESTIONS = [
  "What is the 75% attendance rule?",
  "Tell me about CSE placements",
  "How to apply for a duplicate ID card?",
  "What are the hostel in-times?",
  "Tell me about CU Fest"
];

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem("cu-chatbot-theme");
    if (saved) return saved === "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });
  const bottomRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", dark ? "dark" : "light");
    localStorage.setItem("cu-chatbot-theme", dark ? "dark" : "light");
  }, [dark]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendMessage = async (textOverride = null) => {
    const textToSend = textOverride || message;
    if (!textToSend.trim() || loading) return;

    const userMsg = { sender: "user", text: textToSend };
    setChat(prev => [...prev, userMsg]);
    if (!textOverride) setMessage("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/chat", { message: textToSend });
      setTimeout(() => {
        const botMsg = { sender: "bot", text: res.data.reply };
        setChat(prev => [...prev, botMsg]);
        setLoading(false);
      }, 600);
    } catch {
      setTimeout(() => {
        setChat(prev => [...prev, { sender: "bot", text: "Sorry, I couldn't connect to the server." }]);
        setLoading(false);
      }, 600);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleFaqClick = (q) => {
    sendMessage(q);
  };

  return (
    <div className="chatbot-root">

      {/* Header outside main layout for cleaner look */}
      <div className="chatbot-header">
        <div>
          <div className="chatbot-title">CU Assistant <span role="img" aria-label="robot" className="title-emoji">🤖</span></div>
          <div className="chatbot-subtitle">Your Intelligent guide to Chandigarh University</div>
        </div>
        <div className="header-actions">
          <button className="about-btn" onClick={() => setShowAbout(true)}>i</button>
          <label className="theme-toggle" title={dark ? "Switch to light mode" : "Switch to dark mode"}>
            <input type="checkbox" checked={dark} onChange={() => setDark(d => !d)} />
            <span className="theme-toggle-track">
              <span className="theme-toggle-thumb">{dark ? "🌙" : "☀️"}</span>
            </span>
          </label>
        </div>
      </div>

      <div className="main-layout">

        {/* Chat Window */}
        <div className="chatbot-window">
          <div className="chatbot-messages">
            {chat.length === 0 && (
              <div className="chatbot-empty">
                <span className="chatbot-empty-icon">🎓</span>
                <p>Start a conversation or click a question!</p>
              </div>
            )}

            {chat.map((c, i) => (
              <div key={i} className={`chat-row ${c.sender}`}>
                <div className="chat-avatar">
                  {c.sender === "user" ? "U" : "🤖"}
                </div>
                <div className="chat-bubble">{c.text}</div>
              </div>
            ))}

            {loading && (
              <div className="chat-row bot">
                <div className="chat-avatar">🤖</div>
                <div className="chat-bubble">
                  <div className="typing-indicator">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          <div className="chatbot-input-row">
            <input
              className="chatbot-input"
              value={message}
              onChange={e => setMessage(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Type a message…"
              disabled={loading}
            />
            <button
              className="chatbot-send-btn"
              onClick={() => sendMessage()}
              disabled={!message.trim() || loading}
            >
              Send
            </button>
          </div>
        </div>

        {/* Sidebar / FAQ Panel */}
        <div className="faq-sidebar">
          <h3>Commonly Asked</h3>
          <div className="faq-list">
            {COMMON_QUESTIONS.map((q, idx) => (
              <button
                key={idx}
                className="faq-pill"
                onClick={() => handleFaqClick(q)}
                disabled={loading}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

      </div>

      {/* About Modal */}
      {showAbout && (
        <div className="modal-overlay" onClick={() => setShowAbout(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowAbout(false)}>×</button>
            <h2>About CU Assistant</h2>
            <div className="modal-body">
              <p>Welcome to the <strong>Chandigarh University Intelligent Assistant</strong>!</p>
              <p>This project was built to help students effortlessly navigate campus life. It is powered by a custom deep learning semantic search engine trained on over 72,000 specific data points related to the university.</p>

              <div className="feature-grid">
                <div className="feature-card">
                  <span className="emoji">🧠</span>
                  <h4>Highly Intelligent</h4>
                  <span>Understands deep context regarding 100+ specific courses, hostels, rules, and timings.</span>
                </div>
                <div className="feature-card">
                  <span className="emoji">✨</span>
                  <h4>Premium UI</h4>
                  <span>Built with React and Glassmorphic Vanilla CSS featuring an intelligent Dark Mode.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;
