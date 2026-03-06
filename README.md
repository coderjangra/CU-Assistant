<div align="center">
  <img src="https://via.placeholder.com/150/4f46e5/ffffff?text=%F0%9F%A4%96" alt="CU Assistant Logo" width="100"/>
  <h1>🎓 CU Assistant</h1>
  <p><strong>A Highly Intelligent, Premium Virtual Assistant for Chandigarh University</strong></p>
  <p>
    Built with React, Flask, and Deep Semantic Search (sentence-transformers).
  </p>
</div>

---

## ✨ Features
- **🤖 Deep Intelligence:** Custom NLP backend trained on over 72,000+ specific intent variations covering courses, hostels, rules, fests, and campus logistics.
- **💎 Premium UI/UX:** Built with a stunning "Ultra Glass" theme utilizing raw CSS backdrop filters, animated mesh gradients, and bouncy fluid micro-interactions.
- **⚡ Semantic Search:** Uses `all-MiniLM-L6-v2` to understand the *meaning* behind questions, not just hardcoded keywords. Fallbacks are virtually eliminated.
- **🌙 Smart Theme Engine:** Seamless Light & Dark mode that remembers your preference.
- **Sidebar FAQs:** Quick-click common queries (e.g., *75% Attendance Rules, Hostel Timings*) for effortless navigation.

## 🛠️ Tech Stack
**Frontend:** React (Create React App), Vanilla CSS (Glassmorphism), Axios, HTML5  
**Backend:** Python 3, Flask, Flask-CORS, NLTK, Sentence-Transformers, Numpy  

## 🚀 How to Run Locally

### 1. Start the Intelligent Backend
Ensure you have Python installed.
```bash
cd cu-chatbot-backend
python -m venv venv
# Activate venv: .\venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
python app.py
```
*The NLP engine will load and the server will start on `http://127.0.0.1:5000`.*

### 2. Start the Crystal UI
Ensure you have Node.js installed.
```bash
cd cu-chatbot-ui
npm install
npm start
```
*The app will automatically open at `http://localhost:3000`.*

---
*Created by Chirag Jangra*
