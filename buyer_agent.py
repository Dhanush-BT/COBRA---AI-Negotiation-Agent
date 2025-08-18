import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

# ============================================
# LOAD CONFIG
# ============================================

PERSONALITY_FILE = "personality_config.json"

def load_personality_config(filepath: str) -> Dict[str, Any]:
    """Load personality configuration from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

config_data = load_personality_config(PERSONALITY_FILE)

# ============================================
# DATA STRUCTURES
# ============================================

@dataclass
class Product:
    name: str
    category: str
    quantity: int
    quality_grade: str
    origin: str
    base_market_price: int
    attributes: Dict[str, Any]

@dataclass
class NegotiationContext:
    product: Product
    your_budget: int
    current_round: int
    seller_offers: List[int]
    your_offers: List[int]
    messages: List[Dict[str, str]]

class DealStatus(Enum):
    ONGOING = "ongoing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# ============================================
# BASE BUYER AGENT
# ============================================

class BaseBuyerAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()
        
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        pass

    @abstractmethod
    def respond_to_seller_offer(
        self, context: NegotiationContext, seller_price: int, seller_message: str
    ) -> Tuple[DealStatus, int, str]:
        pass

    @abstractmethod
    def get_personality_prompt(self) -> str:
        pass

# ============================================
# COBRA-BUYER
# ============================================

class CobraBuyer(BaseBuyerAgent):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.config = config
        super().__init__(name)

    def define_personality(self) -> Dict[str, Any]:
        return self.config

    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        offer = min(int(context.product.base_market_price * self.config["early_round_multiplier"]),
                    context.your_budget)
        message = self.config["catchphrases"]["opening"].format(price=offer)
        return offer, message

    def respond_to_seller_offer(
        self, context: NegotiationContext, seller_price: int, seller_message: str
    ) -> Tuple[DealStatus, int, str]:
        round_num = context.current_round
        threshold = int(context.product.base_market_price * self.config["accept_threshold_percentage"])
        if seller_price <= threshold:
            return DealStatus.ACCEPTED, seller_price, f"Deal accepted at ₹{seller_price}! Let's finalize."
        if round_num >= self.config["force_close_round"]:
            final_offer = min(seller_price, context.your_budget)
            return DealStatus.ACCEPTED, final_offer, f"Let's close this at ₹{final_offer}. Can we finalize?"
        if round_num >= self.config["force_close_round"] - 3:
            counter_offer = min(int(seller_price * self.config["mid_round_multiplier"]), context.your_budget)
            message = self.config["catchphrases"]["mid_round"].format(price=counter_offer)
        else:
            counter_offer = min(int(seller_price * self.config["early_round_multiplier"]), context.your_budget)
            message = self.config["catchphrases"]["standard"].format(price=counter_offer)
        return DealStatus.ONGOING, counter_offer, message

    def get_personality_prompt(self) -> str:
        return json.dumps(self.config, indent=4)

# ============================================
# COBRA-SELLER
# ============================================

class CobraSeller:
    def __init__(self, name: str, product_min_price: int, config: Dict[str, Any]):
        self.name = name
        self.min_price = product_min_price
        self.config = config
        self.opening_price = None

    def get_opening_price(self, product: Product) -> Tuple[int, str]:
        self.opening_price = int(product.base_market_price * self.config["opening_multiplier"])
        message = self.config["catchphrases"]["opening"].format(
            quality_grade=product.quality_grade,
            product_name=product.name,
            price=self.opening_price
        )
        return self.opening_price, message

    def respond_to_buyer(self, buyer_offer: int, round_num: int) -> Tuple[int, str, bool]:
        if buyer_offer >= self.min_price:
            return buyer_offer, f"You have a deal at ₹{buyer_offer}!", True
        if round_num >= self.config["force_close_round"]:
            counter = max(self.min_price, buyer_offer)
            message = self.config["catchphrases"]["force_close"].format(price=counter)
            return counter, message, True
        if round_num >= self.config["force_close_round"] - 3:
            counter = max(self.min_price, int(buyer_offer * self.config["mid_round_multiplier"]))
            message = self.config["catchphrases"]["mid_round"].format(
                price=counter, extras=", ".join(self.config["extras"])
            )
        else:
            counter = max(self.min_price, int(buyer_offer * self.config["early_round_multiplier"]))
            message = self.config["catchphrases"]["early_round"].format(
                price=counter, extras=", ".join(self.config["extras"])
            )
        if self.opening_price is not None:
            counter = min(counter, self.opening_price)
        return counter, message, False
    
    def get_personality_prompt(self) -> str:
        return json.dumps(self.config, indent=4)

# ============================================
# NEGOTIATION SIMULATOR
# ============================================

def run_negotiation_test(
    buyer_agent: BaseBuyerAgent,
    product: Product,
    buyer_budget: int,
    seller_min: int,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Run negotiation between buyer and seller and return full conversation."""
    seller = CobraSeller("Cobra-Seller", seller_min, config["Cobra-Seller"])
    context = NegotiationContext(product, buyer_budget, 0, [], [], [])
    seller_price, seller_msg = seller.get_opening_price(product)
    context.seller_offers.append(seller_price)
    context.messages.append({"role": "seller", "message": seller_msg})
    deal_made = False
    final_price = None
    for round_num in range(10):
        context.current_round = round_num + 1
        if round_num == 0:
            buyer_offer, buyer_msg = buyer_agent.generate_opening_offer(context)
            status = DealStatus.ONGOING
        else:
            status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(context, seller_price, seller_msg)
        context.your_offers.append(buyer_offer)
        context.messages.append({"role": "buyer", "message": buyer_msg})
        if status == DealStatus.ACCEPTED:
            deal_made = True
            final_price = min(buyer_offer, buyer_budget)
            break
        seller_price, seller_msg, seller_accepts = seller.respond_to_buyer(buyer_offer, round_num)
        context.seller_offers.append(seller_price)
        context.messages.append({"role": "seller", "message": seller_msg})
        if seller_accepts:
            deal_made = True
            final_price = seller_price
            break
    return {
        "deal_made": deal_made,
        "final_price": final_price,
        "rounds": context.current_round,
        "conversation": context.messages
    }

# ============================================
# TEST SCENARIOS
# ============================================

test_scenarios = [
    {
        "name": "Alphonso Mangoes - Easy",
        "product": Product("Alphonso Mangoes", "Mangoes", 100, "A", "Ratnagiri", 180000, {"ripeness": "optimal"}),
        "buyer_budget": 220000,
        "seller_min": 160000
    },
    {
        "name": "Alphonso Mangoes - Medium",
        "product": Product("Alphonso Mangoes", "Mangoes", 100, "A", "Ratnagiri", 180000, {"ripeness": "optimal"}),
        "buyer_budget": 180000,
        "seller_min": 170000
    },
    {
        "name": "Kesar Mangoes - Hard",
        "product": Product("Kesar Mangoes", "Mangoes", 150, "B", "Gujarat", 150000, {"ripeness": "semi-ripe"}),
        "buyer_budget": 140000,
        "seller_min": 130000
    }
]

# ============================================
# TEST FUNCTIONS (UNIFIED FORMAT)
# ============================================

def test_buyer_scenarios():
    buyer_agent = CobraBuyer("Cobra-Buyer", config_data["Cobra-Buyer"])
    print("\n=== TESTING COBRA-BUYER ===")
    for scenario in test_scenarios:
        print(f"\nScenario: {scenario['name']}")
        result = run_negotiation_test(
            buyer_agent=buyer_agent,
            product=scenario["product"],
            buyer_budget=scenario["buyer_budget"],
            seller_min=scenario["seller_min"],
            config=config_data
        )
        if result["deal_made"]:
            print(f"✅ DEAL at ₹{result['final_price']:,} in {result['rounds']} rounds")
        else:
            print(f"❌ NO DEAL after {result['rounds']} rounds")
        print("Conversation:")
        for msg in result["conversation"]:
            print(f"{msg['role'].capitalize()}: {msg['message']}")

def test_seller_scenarios():
    print("\n=== TESTING COBRA-SELLER ===")
    for scenario in test_scenarios:
        print(f"\nScenario: {scenario['name']}")
        buyer_agent = CobraBuyer("Cobra-Buyer", config_data["Cobra-Buyer"])
        result = run_negotiation_test(
            buyer_agent=buyer_agent,
            product=scenario["product"],
            buyer_budget=scenario["buyer_budget"],
            seller_min=scenario["seller_min"],
            config=config_data
        )
        if result["deal_made"]:
            print(f"✅ DEAL at ₹{result['final_price']:,} in {result['rounds']} rounds")
        else:
            print(f"❌ NO DEAL after {result['rounds']} rounds")
        print("Conversation:")
        for msg in result["conversation"]:
            print(f"{msg['role'].capitalize()}: {msg['message']}")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    test_buyer_scenarios()
    test_seller_scenarios()
