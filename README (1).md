# COBRA---AI-Negotiation-Agent

Welcome to the **AI Negotiation Simulator**, a project that showcases how Artificial Intelligence can role-play **buyers and sellers** to negotiate deals dynamically.

Instead of just hard-coded responses, this simulator uses **Large Language Models (LLMs)** to **reason, bargain, and adapt strategies** — creating a realistic and interactive negotiation experience.

---

## 📌 What This Project Does

- Creates a **negotiation environment** where two agents (Buyer & Seller) try to reach a deal.  
- Allows **different negotiation modes**:
  - **Fully Automated** → Buyer and Seller are both AI.  
  - **Human-in-the-Loop** → You can act as Buyer or Seller while the AI takes the opposite role.  
- Tracks **offers, counter-offers, concessions, and final outcomes**.  
- Simulates **real-world bargaining** like laptop sales, car purchases, or service agreements.  

---

## 🌟 Key Features

- **🤖 Dual AI Agents** → Independent Buyer and Seller personalities.  
- **🎭 Role-Play Option** → Play as Buyer or Seller and negotiate with the AI.  
- **🔄 Multi-Round Simulation** → Negotiations can run for any number of rounds.  
- **💰 Flexible Pricing** → Define starting offers and observe concession strategies.  
- **📊 Outcome Tracking** → Understand how deals evolve and at what point compromises are made.  
- **🎓 Learning Tool** → Demonstrates **game theory, decision-making, and strategy adaptation**.  

---

## 🌟 Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| 🤖 **Dual AI Agents** | Independent Buyer & Seller personalities | Realistic negotiation flow |
| 🎭 **Role-Play Option** | User can play as Buyer or Seller | Interactive learning |
| 🔄 **Multi-Round Simulation** | Negotiation continues for fixed rounds | Studies concession patterns |
| 💰 **Flexible Pricing** | Adjustable start prices & goals | Customizable scenarios |
| 📊 **Outcome Tracking** | Records deals, failures, and strategies | Analytics & learning insights |
| 🎓 **Educational Use** | Demonstrates game theory & strategies | Great for teaching/training |
| 🧠 **Adaptive Reasoning** | Agents change tactics mid-way | Realistic human-like bargaining |

---

## 🚀 Workflow

1. **Setup a negotiation scenario** (e.g., *Laptop sale starting at $200, Seller asking $500*).  
2. **Choose the mode**:
   - *Simulation Mode* → AI Buyer vs AI Seller  
   - *Interactive Mode* → You act as Buyer or Seller  
3. **Run negotiation rounds**: Buyer makes an offer, Seller counters, and so on.  
4. **Deal or No Deal**: Agreement is reached (win-win or compromise), or negotiation fails.  

---

## 🎮 Example Negotiation Log (Laptop Purchase)

**Scenario:**  
- Buyer starts at **$200**  
- Seller asks for **$500**  
- Max **10 rounds**  

| Round | Buyer’s Offer | Seller’s Response | Notes |
|-------|---------------|-------------------|-------|
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

- Unlike static simulations, **our agents adapt strategies** in real-time.  
- Allows **human + AI collaboration**, not just AI vs AI.  
- Logs negotiations in a **clear tabular format** for analysis.  
- Designed as both a **research tool** and an **educational playground**.  
## 🔮 Future Enhancements

---

- Add **win-win scoring system** (fairness, satisfaction, efficiency).  
- Multi-party negotiations (e.g., 2 buyers vs 1 seller).  
- Support for **non-monetary trades** (services, bundles, extras).  
- Visualization of **negotiation graphs & trends**.  

---

## 🎯 Success Metrics Followed

| Metric | Requirement | Weight |
| --- | --- | --- |
| Successful Deals | ≥ 70% of simulations | 40% |
| Average Savings | ≥ 10% below buyer budget | 30% |
| Negotiation Fairness | ≤ 15% price gap between parties | 20% |
| Code Quality | Clean, modular, documented | 10% |
