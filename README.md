# COBRA — AI Negotiation Agent  

Welcome to the **AI Negotiation Simulator**, a project that showcases how Artificial Intelligence can role-play buyers and sellers to negotiate deals dynamically.  

Instead of just hard-coded responses, this simulator uses **Large Language Models (LLMs)** to reason, bargain, and adapt strategies — creating a realistic and interactive negotiation experience.  

---

## 📌 What This Project Does  
- Creates a negotiation environment where two agents (**Buyer & Seller**) try to reach a deal.  
- Allows different negotiation modes:  
  - **Fully Automated** → Buyer and Seller are both AI.  
  - **Human-in-the-Loop** → You can act as Buyer or Seller while the AI takes the opposite role.  
- Tracks offers, counter-offers, concessions, and final outcomes.  
- Simulates real-world bargaining like laptop sales, car purchases, or service agreements.  

---

## 🌟 Key Features  

| Feature | Description | Benefit |
|---------|-------------|---------|
| 🤖 Dual AI Agents | Independent Buyer & Seller personalities | Realistic negotiation flow |
| 🎭 Role-Play Option | User can play as Buyer or Seller | Interactive learning |
| 🔄 Multi-Round Simulation | Negotiation continues for fixed rounds | Studies concession patterns |
| 💰 Flexible Pricing | Adjustable start prices & goals | Customizable scenarios |
| 📊 Outcome Tracking | Records deals, failures, and strategies | Analytics & learning insights |
| 🎓 Educational Use | Demonstrates game theory & strategies | Great for teaching/training |
| 🧠 Adaptive Reasoning | Agents change tactics mid-way | Realistic human-like bargaining |

---

## 🚀 Workflow  

1. **Setup** a negotiation scenario (e.g., Laptop sale starting at $200, Seller asking $500).  
2. **Choose Mode**:  
   - Simulation Mode → AI Buyer vs AI Seller  
   - Interactive Mode → You act as Buyer or Seller  
3. **Run Negotiation Rounds**: Buyer makes an offer, Seller counters, and so on.  
4. **Deal or No Deal**: Agreement is reached (win-win or compromise), or negotiation fails.  

---

## 🔄 Buyer & Seller Workflow (Detailed)  

### 🛒 Buyer Agent Flow  
1. **Personality Call** → `cobra buyer cls` loads buyer personality traits.  
2. **Persona Prompt** → Defines buyer style (e.g., aggressive, conservative, risk-taking).  
3. **Opening Prices** → Buyer’s initial offer is set.  
4. **Response Loops to Seller Offer** → Buyer dynamically adjusts offers based on seller’s counter-offers.  
5. **Structured JSON Data** → Buyer’s state (offers, concessions, satisfaction level) is logged and passed to **LLaMA** for reasoning.  

### 🏷️ Seller Agent Flow  
1. **Personality Call** → `cobra seller cls` loads seller personality traits.  
2. **Persona Prompt** → Defines seller style (e.g., tough negotiator, flexible, opportunistic).  
3. **Opening Prices** → Seller’s initial asking price is set.  
4. **Response Loops to Buyer Offer** → Seller makes counter-offers based on buyer’s moves.  
5. **Structured JSON Data** → Seller’s negotiation log is also passed to **LLaMA** for adaptive reasoning.  

---

## 📊 Key Metrics  

| Metric | Description |
|--------|-------------|
| **Opening Offer Generation** | System creates initial buyer & seller offers automatically. |
| **System Prompting** | Provides structured prompts making it easy to integrate into **Concordia** (AI orchestration framework). |
| **Response Loops** | Tracks concession moves, counter-offers, and agreement zones. |
| **Fairness & Balance** | Ensures neither side has extreme advantage. |
| **Ease of Integration** | Designed to plug into broader platforms like **Concordia** without major rework. |

---

## 🎯 Test Scenarios  

The system is tested under **multiple difficulty levels** for Buyer roles:  

- **Easy Scenario** → Seller is flexible, quick agreement possible.  
- **Medium Scenario** → Seller is moderately tough, requires 5–7 counter rounds.  
- **Hard Scenario** → Seller is rigid, buyer must strategize carefully to close the deal.  

✅ Nothing is “hardcore” — all scenarios are meant to simulate **learning-based negotiations**, not unbeatable opponents.  

---

## 🎮 Example Negotiation Log (Laptop Purchase)  

**Scenario**:  
- Buyer starts at $200  
- Seller asks for $500  
- Max 10 rounds  

| Round | Buyer’s Offer | Seller’s Response | Notes |
|-------|---------------|------------------|-------|
| 1 | $200 | $500 | Starting gap is large |
| 3 | $300 | $450 | Small concessions begin |
| 6 | $370 | $420 | Near compromise zone |
| 9 | $395 | $400 | Close to agreement |
| 10 | $400 + bag | $400 final | Deal made |

✅ **Final Deal**: $400 + free laptop bag  
⚖️ **Rounds Taken**: 10  

---

## 🧩 Use Cases  

- 🎓 **Education** → Teach negotiation & persuasion skills  
- 🧪 **Research** → Study AI bargaining strategies  
- 💼 **Business** → Train sales teams in role-play simulations  
- 🎮 **Entertainment** → Turn negotiation into interactive challenges  

---

## 💡 Why This Project is Unique  

- Agents **adapt strategies in real-time**.  
- Supports **Human + AI collaboration**, not just AI vs AI.  
- Logs negotiations in a **clear JSON + tabular format** for analysis.  
- Designed as both a **research tool** and an **educational playground**.  

---

## 🔮 Future Enhancements  

- Add **win-win scoring system** (fairness, satisfaction, efficiency).  
- Enable **multi-party negotiations** (e.g., 2 buyers vs 1 seller).  
- Support **non-monetary trades** (services, bundles, extras).  
- Add **visual negotiation graphs & trends**.  

---

## 🎯 Success Metrics Followed  

| Metric | Requirement | Weight |
|--------|-------------|--------|
| **Successful Deals** | ≥ 70% of simulations | 40% |
| **Average Savings** | ≥ 10% below buyer budget | 30% |
| **Negotiation Fairness** | ≤ 15% price gap between parties | 20% |
| **Code Quality** | Clean, modular, documented | 10% |

---

