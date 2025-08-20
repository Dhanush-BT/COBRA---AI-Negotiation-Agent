# 🧠 Negotiation Strategy 

This document explains the **thought process, design, and strategies** used in the AI Negotiation Simulator project.  
The goal is to simulate **realistic buyer-seller negotiations** using configurable personalities, adaptive reasoning, and structured negotiation frameworks.  

---

## 🌟 Why This Strategy Works  
- **LLM-friendly JSON pipeline** → reduces ambiguity & errors.  
- **Chris Voss' techniques** → realistic human-style negotiation.  
- **BAFO integration** → ensures closure phase has clarity.  
- **Round-structured growth** → keeps negotiations realistic and non-random.  
- **Consistency in character** → Buyer and Seller personalities remain stable across rounds.

---

## 🎯 Core Objective  
To build a realistic negotiation simulator where both Buyer and Seller have:  
- Unique personalities (aggressive, defensive, balanced, opportunistic).  
- Adaptive strategies that evolve during the negotiation rounds.  
- A decision-making process for **deal or no-deal** outcomes.  
- Strategies inspired by **Chris Voss negotiation principles** and **BAFO (Best and Final Offer)** techniques.  

---

## 🏗 Design Principles  
- **Modularity** → Separate logic for Buyer, Seller, and Negotiation Engine.  
- **Configurable Personalities** → Stored in `personality_config.json`.  
- **Round-based Interaction** → Simulation progresses step by step.  
- **Dynamic Strategy** → Opening, mid, and late round tactics differ.  
- **Outcome Tracking** → Logs paths (offers, counters, thresholds, results).  
- **Adaptive Patience Strategy** → Moves depend on perceived patience of the other party.  
- **JSON-first Decisioning** → LLMs process structured JSON logs → faster reasoning, fewer errors, easier consistency checks.  

---

## ⚔ Buyer & Seller Strategies  

| Role   | Strategy Layer | Early Rounds (1–4) | Mid Rounds (5–8) | Late Rounds (9–10) |
|--------|---------------|---------------------|------------------|--------------------|
| Buyer  | Aggressive cost-cutting | Very low offers, slow moves | Pushes more firmly with concessions | Moves closer to BAFO and closes deal |
| Seller | Defensive value-preserving | High anchor price | Moderate concessions | Drops to near BAFO if deal possible |
| Shared | **Chris Voss Strategy** | Anchoring with high/low offers | Tactical empathy + calibrated questions | “That’s my best and final offer” (BAFO) |
| Unique | **Adaptive Patience** | Responds slowly if buyer/seller looks patient | Speeds up concessions if urgency detected | Sharp final adjustment to close |

---

## 🌀 Flow of Negotiation  

### Initialization  
1. Load **Buyer/Seller personalities**.  
2. Define **initial price, thresholds, and max rounds**.  

### Offer Generation  
- Seller proposes opening anchor.  
- Buyer counters with lowball offer.  
- Both update via structured **JSON → LLM** pipeline.  

### Adaptive Patience & Personality  
- If opponent moves slowly → assume patience → respond with smaller increments.  
- If opponent jumps quickly → assume urgency → respond with larger concessions.  
- Personality (aggressive vs conservative) decides speed of movement.  

### Round-based Tactics  
- **Rounds 1–4** → Small incremental changes, testing the waters.  
- **Rounds 5–8** → Push harder, signaling willingness but protecting margin.  
- **Rounds 9–10** → Enter **closing phase**, both shift towards **BAFO**.  

### Decision Making  
- If offer within acceptable range → **Deal**.  
- If not → proceed to next round.  

### Termination Conditions  
- Rounds exceeded → No Deal.  
- Thresholds not met → Walk Away.  
- Deal struck → Log Success.  

---

## 📊 Example Strategy in Action  

**Scenario: Laptop Sale (10 rounds, Seller starts $500, Buyer starts $200)**  

| Round | Buyer’s Offer | Seller’s Offer | Strategy Applied |
|-------|---------------|----------------|-----------------|
| 1 | $200 | $500 | Buyer anchors low, Seller anchors high |
| 3 | $250 | $480 | Small increases → Testing patience |
| 5 | $300 | $440 | Mid-phase push (Chris Voss: tactical empathy) |
| 7 | $350 | $410 | Urgency detected → Faster concessions |
| 9 | $380 | $400 | Both near BAFO range |
| 10 | $395 | $400 | BAFO strategy → Deal closed |

✅ **Final Deal**: $400  
⚖️ **Rounds Taken**: 10  

---


---
