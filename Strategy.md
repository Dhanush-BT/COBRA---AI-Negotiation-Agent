# 🧠 Negotiation Strategy Document

This document explains the thought process, design, and strategies used in the *AI Negotiation Simulator* project.  
The goal is to simulate realistic buyer-seller negotiations using configurable personalities and adaptive multipliers.

---

## 🎯 Core Objective
To build a *realistic negotiation simulator* where both buyer and seller have:
- Unique *personalities* (aggressive, defensive, balanced, opportunistic).
- Adaptive *strategies* that evolve during the negotiation rounds.
- A decision-making process for *deal* or *no-deal* outcomes.

---

## 🏗 Design Principles
1. *Modularity* → Separate logic for Buyer, Seller, and Negotiation engine.  
2. *Configurable Personalities* → Personality traits stored in personality_config.json.  
3. *Round-based Interaction* → Simulation progresses over multiple rounds.  
4. *Dynamic Strategy* → Early, mid, and late round tactics differ.  
5. *Outcome Tracking* → Logs negotiation path (offers, counters, thresholds, results).  
6. *Unique Layer: Adaptive Patience Strategy* → Offers are influenced by both urgency and perceived patience of the opponent.  

---

## ⚔ Buyer & Seller Strategies

| Role        | Strategy | Early Rounds | Mid Rounds | Late Rounds |
|-------------|----------|--------------|------------|-------------|
| *Buyer*   | Aggressive cost-cutting | Very low offers | Slight increase | Near threshold if desperate |
| *Seller*  | Defensive value-preserving | High anchor price | Adjust moderately | Final discounts if needed |
| *Unique Strategy* | Adaptive Patience | Small, slow moves if opponent seems patient | Faster concessions if opponent shows urgency | Final sharp move if deal is close |

---

## 🔄 Flow of Negotiation
1. *Initialization*  
   - Load buyer/seller personalities.  
   - Define initial price, min/max thresholds, and round limit.  

2. *Offer Generation*  
   - Seller proposes price based on multiplier & personality.  
   - Buyer counters based on willingness and budget.  

3. *Adaptive Patience Strategy (Unique)*  
   - Both buyer & seller estimate how patient the other party is by observing *offer increments*.  
   - If offers are moving *slowly*, they assume the other side is patient → respond with smaller concessions.  
   - If offers move *quickly*, they assume urgency → respond with sharper concessions to avoid losing the deal.  

4. *Decision Making*  
   - If offer within acceptable range → *Deal*.  
   - If not → proceed to next round.  

5. *Termination Conditions*  
   - Rounds exceeded → No Deal.  
   - Thresholds not met → Walk Away.  
   - Deal struck → Log success.  

---

## 📊 Example Strategy in Action
*Scenario:* Negotiating for a Laptop (10 rounds, Seller starts at $200)  

- Round 1 → Seller asks $200, Buyer counters $120.  
- Round 3 → Buyer moves only $5 (to $125) → Seller interprets as patience, reduces slowly to $195.  
- Round 5 → Buyer suddenly jumps to $140 → Seller interprets as urgency, drops quickly to $160.  
- Round 8 → Buyer at $150, Seller at $150 → *Deal closed!*  

--
