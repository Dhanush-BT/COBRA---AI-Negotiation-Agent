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

# Load the buyer/seller configuration data
config_data = load_personality_config(PERSONALITY_FILE)

# ============================================
# DATA STRUCTURES
# ============================================

@dataclass
class Product:
    """Represents the product being negotiated."""
    name: str
    category: str
    quantity: int
    quality_grade: str
    origin: str
    base_market_price: int
    attributes: Dict[str, Any]  # Extra product-specific details (ripeness, etc.)

@dataclass
class NegotiationContext:
    """Keeps track of negotiation state at any round."""
    product: Product
    your_budget: int
    current_round: int
    seller_offers: List[int]
    your_offers: List[int]
    messages: List[Dict[str, str]]  # Conversation history

class DealStatus(Enum):
    """Defines the possible deal outcomes."""
    ONGOING = "ongoing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# ============================================
# BASE BUYER AGENT
# ============================================

class BaseBuyerAgent(ABC):
    """Abstract base class for buyer agents."""

    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()  # Each buyer must define personality
    
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        """Load or define personality (catchphrases, thresholds, etc.)"""
        pass

    @abstractmethod
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        """Generate the first offer of the negotiation."""
        pass

    @abstractmethod
    def respond_to_seller_offer(
        self, context: NegotiationContext, seller_price: int, seller_message: str
    ) -> Tuple[DealStatus, int, str]:
        """Respond to a seller's price with a counter-offer or accept."""
        pass

# ============================================
# COBRA-BUYER
# ============================================

class CobraBuyer(BaseBuyerAgent):
    """A concrete buyer agent using config-defined behavior."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.config = config
        super().__init__(name)

    def define_personality(self) -> Dict[str, Any]:
        """Return buyer's personality config."""
        return self.config

    def build_buyer_prompt(self, context: NegotiationContext) -> str:
        """Builds system prompt describing buyer behavior/personality."""
        return f"""
        You are {self.name}, a buyer agent with this personality:
        {json.dumps(self.config, indent=2)}
        
        Product: {context.product.name}, Category: {context.product.category}, 
        Quantity: {context.product.quantity}, Quality: {context.product.quality_grade},
        Origin: {context.product.origin}, Base Market Price: ₹{context.product.base_market_price}
        
        Your budget: ₹{context.your_budget}, Current round: {context.current_round}.
        Previous seller offers: {context.seller_offers}
        Previous buyer offers: {context.your_offers}
        Messages so far: {context.messages}
        
        Start negotiation using your opening offer and tactics.
        """

    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        """Make the buyer's first move (usually aggressive)."""
        early_mult = float(self.config.get("early_round_multiplier", 0.85))
        offer = min(int(context.product.base_market_price * early_mult), context.your_budget)
        msg_tpl = self.config.get("catchphrases", {}).get("opening", "Starting at ₹{price}.")
        return offer, msg_tpl.format(price=offer)

    def respond_to_seller_offer(
        self, context: NegotiationContext, seller_price: int, seller_message: str
    ) -> Tuple[DealStatus, int, str]:
        """Respond to seller based on round number and thresholds."""
        round_num = context.current_round

        acc_pct = float(self.config.get("accept_threshold_percentage", 0.9))
        early_mult = float(self.config.get("early_round_multiplier", 0.85))
        mid_mult = float(self.config.get("mid_round_multiplier", 0.92))
        force_round = int(self.config.get("force_close_round", 10))
        phrases = self.config.get("catchphrases", {})

        # Buyer threshold for accepting
        threshold = int(context.product.base_market_price * acc_pct)

        # Accept deal if seller price is low enough and within budget
        if seller_price <= threshold and seller_price <= context.your_budget:
            return DealStatus.ACCEPTED, seller_price, f"Deal accepted at ₹{seller_price}! Let's finalize."

        # Last round → make one last counter
        if round_num >= force_round:
            final_offer = min(seller_price, context.your_budget)
            msg = phrases.get("final", "Final from me: ₹{price}. Can we sign today?").format(price=final_offer)
            return DealStatus.ONGOING, final_offer, msg

        # Mid/early round counters
        if round_num >= force_round - 3:  # Late phase
            counter_offer = min(int(seller_price * mid_mult), context.your_budget)
            message = phrases.get("mid_round", "Let’s wrap at ₹{price}.").format(price=counter_offer)
        else:  # Early phase
            counter_offer = min(int(seller_price * early_mult), context.your_budget)
            message = phrases.get("standard", "I can do ₹{price}.").format(price=counter_offer)

        return DealStatus.ONGOING, counter_offer, message

# ============================================
# COBRA-SELLER
# ============================================

class CobraSeller:
    """A seller agent with configurable negotiation strategy."""

    def __init__(self, name: str, product_min_price: int, config: Dict[str, Any]):
        self.name = name
        self.min_price = product_min_price  # Seller won’t go below this
        self.config = config
        self.opening_price = None

    def build_seller_prompt(self, product: Product, context: NegotiationContext) -> str:
        """Builds system prompt describing seller behavior/personality."""
        return f"""
        You are {self.name}, a seller agent with this personality:
        {json.dumps(self.config, indent=2)}
        
        Product: {product.name}, Category: {product.category}, 
        Quantity: {product.quantity}, Quality: {product.quality_grade},
        Origin: {product.origin}, Base Market Price: ₹{product.base_market_price}
        
        Your minimum price: ₹{self.min_price}, Current round: {context.current_round}.
        Previous seller offers: {context.seller_offers}
        Previous buyer offers: {context.your_offers}
        Messages so far: {context.messages}
        
        Start negotiation using your opening offer and extras.
        """

    def get_opening_price(self, product: Product) -> Tuple[int, str]:
        """First seller offer: usually higher than market price."""
        opening_mult = float(self.config.get("opening_multiplier", 1.2))
        self.opening_price = int(product.base_market_price * opening_mult)
        msg_tpl = self.config.get("catchphrases", {}).get(
            "opening", "{quality_grade} {product_name} at ₹{price}."
        )
        message = msg_tpl.format(
            quality_grade=product.quality_grade,
            product_name=product.name,
            price=self.opening_price
        )
        return self.opening_price, message

    def respond_to_buyer(self, buyer_offer: int, round_num: int) -> Tuple[int, str, bool]:
        """Respond to buyer with a counter-offer or accept."""
        early_mult = float(self.config.get("early_round_multiplier", 1.1))
        mid_mult = float(self.config.get("mid_round_multiplier", 1.04))
        force_round = int(self.config.get("force_close_round", 10))
        phrases = self.config.get("catchphrases", {})
        extras_list = self.config.get("extras", [])
        extras = ", ".join(extras_list) if extras_list else ""

        # Accept if buyer offer ≥ min price
        if buyer_offer >= self.min_price:
            return buyer_offer, f"You have a deal at ₹{buyer_offer}!", True

        # Final round → seller forces closure
        if round_num >= force_round:
            counter = max(self.min_price, buyer_offer)
            msg = phrases.get("force_close", "Last price ₹{price}.").format(price=counter)
            if self.opening_price is not None:
                counter = min(counter, self.opening_price)
            return counter, msg, False

        # Mid/early round counters
        if round_num >= force_round - 3:  # Late phase
            counter = max(self.min_price, int(buyer_offer * mid_mult))
            msg = phrases.get("mid_round", "₹{price} including {extras}.").format(price=counter, extras=extras)
        else:  # Early phase
            counter = max(self.min_price, int(buyer_offer * early_mult))
            msg = phrases.get("early_round", "₹{price} including {extras}.").format(price=counter, extras=extras)

        # Ensure seller doesn’t exceed opening price
        if self.opening_price is not None:
            counter = min(counter, self.opening_price)

        return counter, msg, False

# ============================================
# TEST FUNCTIONS (CONVERSATION SIMULATION)
# ============================================

def test_buyer_scenarios():
    """Simulate negotiation where buyer opens first."""
    print("\n=== BUYER STARTS NEGOTIATION ===")
    buyer_agent = CobraBuyer("Cobra-Buyer", config_data["Cobra-Buyer"])
    seller_agent = CobraSeller("Cobra-Seller", 160000, config_data["Cobra-Seller"])

    product = Product("Alphonso Mangoes", "Mangoes", 100, "A", "Ratnagiri", 180000, {"ripeness": "optimal"})
    context = NegotiationContext(product, 220000, 1, [], [], [])

    # Build prompts (for reference/logging, not used here)
    _ = buyer_agent.build_buyer_prompt(context)
    _ = seller_agent.build_seller_prompt(product, context)

    # Buyer makes opening move
    buyer_offer, buyer_msg = buyer_agent.generate_opening_offer(context)
    print(f"Round {context.current_round} | Buyer: {buyer_msg} (₹{buyer_offer})")
    context.your_offers.append(buyer_offer)
    context.messages.append({"role": "buyer", "message": buyer_msg})

    # Seller responds
    seller_offer, seller_msg, accepted = seller_agent.respond_to_buyer(buyer_offer, context.current_round)
    print(f"Round {context.current_round} | Seller: {seller_msg} (₹{seller_offer})")
    context.seller_offers.append(seller_offer)
    context.messages.append({"role": "seller", "message": seller_msg})

    # Continue negotiation loop
    while not accepted and context.current_round < 10:
        context.current_round += 1

        # Buyer responds to seller
        status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(
            context, seller_offer, seller_msg
        )
        print(f"Round {context.current_round} | Buyer: {buyer_msg} (₹{buyer_offer})")
        context.your_offers.append(buyer_offer)
        context.messages.append({"role": "buyer", "message": buyer_msg})

        if status == DealStatus.ACCEPTED:
            print(" Deal closed by buyer!")
            break

        # Seller responds to buyer
        seller_offer, seller_msg, accepted = seller_agent.respond_to_buyer(buyer_offer, context.current_round)
        print(f"Round {context.current_round} | Seller: {seller_msg} (₹{seller_offer})")
        context.seller_offers.append(seller_offer)
        context.messages.append({"role": "seller", "message": seller_msg})

        if accepted:
            print(" Deal closed by seller!")
            break


def test_seller_scenarios():
    """Simulate negotiation where seller opens first."""
    print("\n=== SELLER STARTS NEGOTIATION ===")
    buyer_agent = CobraBuyer("Cobra-Buyer", config_data["Cobra-Buyer"])
    seller_agent = CobraSeller("Cobra-Seller", 160000, config_data["Cobra-Seller"])

    product = Product("Alphonso Mangoes", "Mangoes", 100, "A", "Ratnagiri", 180000, {"ripeness": "optimal"})
    context = NegotiationContext(product, 220000, 1, [], [], [])

    _ = buyer_agent.build_buyer_prompt(context)
    _ = seller_agent.build_seller_prompt(product, context)

    # Seller makes opening move
    seller_offer, seller_msg = seller_agent.get_opening_price(product)
    print(f"Round {context.current_round} | Seller: {seller_msg} (₹{seller_offer})")
    context.seller_offers.append(seller_offer)
    context.messages.append({"role": "seller", "message": seller_msg})

    # Buyer responds
    status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(
        context, seller_offer, seller_msg
    )
    print(f"Round {context.current_round} | Buyer: {buyer_msg} (₹{buyer_offer})")
    context.your_offers.append(buyer_offer)
    context.messages.append({"role": "buyer", "message": buyer_msg})

    if status == DealStatus.ACCEPTED:
        print(" Deal closed by buyer!")
        return

    accepted = False
    while not accepted and context.current_round < 10:
        context.current_round += 1

        # Seller responds to buyer
        seller_offer, seller_msg, accepted = seller_agent.respond_to_buyer(buyer_offer, context.current_round)
        print(f"Round {context.current_round} | Seller: {seller_msg} (₹{seller_offer})")
        context.seller_offers.append(seller_offer)
        context.messages.append({"role": "seller", "message": seller_msg})

        if accepted:
            print(" Deal closed by seller!")
            break

        # Buyer responds
        status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(
            context, seller_offer, seller_msg
        )
        print(f"Round {context.current_round} | Buyer: {buyer_msg} (₹{buyer_offer})")
        context.your_offers.append(buyer_offer)
        context.messages.append({"role": "buyer", "message": buyer_msg})

        if status == DealStatus.ACCEPTED:
            print(" Deal closed by buyer!")
            break

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    # Run both scenarios for testing
    test_buyer_scenarios()
    test_seller_scenarios()
# The above code simulates a negotiation process between a buyer and a seller agent.
