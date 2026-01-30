from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from contextvars import ContextVar
import uuid

# --- 1. Schema Definition (The Database Structure) ---
# 定义您的“数据库”结构。这里使用 Pydantic，因为它自带验证和序列化，非常适合 Agent。

class UserDB(BaseModel):
    """Schema for Database 1: User & Auth"""
    users: Dict[str, dict] = Field(default_factory=dict)
    sessions: List[str] = Field(default_factory=list)
    system_logs: List[str] = Field(default_factory=list)

class EcommerceDB(BaseModel):
    """Schema for Database 2: E-commerce & Inventory"""
    inventory: Dict[str, int] = Field(default_factory=lambda: {"item_001": 100, "item_002": 50})
    orders: List[dict] = Field(default_factory=list)
    cart: Dict[str, int] = Field(default_factory=dict)

# --- 2. State Container (The Storage Engine) ---
# 这是一个容器，持有所有“数据库”的实例。

class GlobalState(BaseModel):
    """Root state container holding all sub-databases."""
    user_db: UserDB = Field(default_factory=UserDB)
    ecommerce_db: EcommerceDB = Field(default_factory=EcommerceDB)

    class Config:
        arbitrary_types_allowed = True

# ContextVar 用于处理并发请求时的状态隔离 (Session Isolation)
_current_state: ContextVar[GlobalState] = ContextVar("current_state", default=GlobalState())

class StateManager:
    """
    Manager to access the correct state instance for the current context.
    """
    @staticmethod
    def get_state() -> GlobalState:
        return _current_state.get()

    @staticmethod
    def init_session():
        """Call this at the start of a request to create a clean state."""
        _current_state.set(GlobalState())

    # Helper to access specific DBs directly
    @property
    def user_db(self) -> UserDB:
        return self.get_state().user_db

    @property
    def commerce_db(self) -> EcommerceDB:
        return self.get_state().ecommerce_db

# Singleton instance of the manager
db = StateManager()


# --- 3. Functional Implementation (The Logic Layer) ---
# 这里是您的具体函数实现，直接操作定义好的数据库字段。

# === Database 1 Functions (User Domain) ===
class UserFunctions:
    @staticmethod
    def register_user(username: str, email: str) -> str:
        """Register a new user (Writes to Database 1)."""
        if username in db.user_db.users:
            return f"Error: User {username} already exists."
        
        user_id = str(uuid.uuid4())[:8]
        db.user_db.users[username] = {"id": user_id, "email": email, "active": True}
        db.user_db.system_logs.append(f"Registered user {username}")
        return f"User {username} created with ID {user_id}"

    @staticmethod
    def login_user(username: str) -> str:
        """Simulate user login (Writes to Database 1)."""
        if username not in db.user_db.users:
            return "Error: User not found."
        
        session_token = f"sess_{uuid.uuid4()}"
        db.user_db.sessions.append(session_token)
        return f"Logged in. Token: {session_token}"

    @staticmethod
    def get_user_count() -> int:
        """Reads from Database 1."""
        return len(db.user_db.users)


# === Database 2 Functions (E-commerce Domain) ===
class CommerceFunctions:
    @staticmethod
    def check_stock(item_id: str) -> int:
        """Check inventory level (Reads Database 2)."""
        return db.commerce_db.inventory.get(item_id, 0)

    @staticmethod
    def add_to_cart(item_id: str, quantity: int) -> str:
        """Add item to cart (Writes to Database 2)."""
        current_stock = db.commerce_db.inventory.get(item_id, 0)
        if current_stock < quantity:
            return f"Error: Not enough stock. Only {current_stock} left."
        
        # In a real app, you might reserve stock here.
        # For this state model, we just update the cart.
        current_in_cart = db.commerce_db.cart.get(item_id, 0)
        db.commerce_db.cart[item_id] = current_in_cart + quantity
        return f"Added {quantity} of {item_id} to cart."

    @staticmethod
    def checkout() -> str:
        """Process order (Reads/Writes Database 2)."""
        cart = db.commerce_db.cart
        if not cart:
            return "Error: Cart is empty."
        
        order_id = str(uuid.uuid4())[:6]
        order_details = {"id": order_id, "items": cart.copy(), "status": "confirmed"}
        
        # Deduct inventory
        for item, qty in cart.items():
            if db.commerce_db.inventory.get(item, 0) < qty:
                 return f"Critical Error: Stock changed during checkout for {item}."
            db.commerce_db.inventory[item] -= qty
            
        db.commerce_db.orders.append(order_details)
        db.commerce_db.cart.clear() # Reset cart
        return f"Order {order_id} placed successfully!"


# --- 4. Demonstration ---

def run_demo():
    print("--- Session 1 Start ---")
    StateManager.init_session() # Explicitly start a fresh session
    
    # 1. User Domain Actions
    print(UserFunctions.register_user("alice", "alice@example.com"))
    print(UserFunctions.login_user("alice"))
    
    # 2. Commerce Domain Actions
    print(CommerceFunctions.add_to_cart("item_001", 5))
    print(f"Stock before checkout: {CommerceFunctions.check_stock('item_001')}")
    print(CommerceFunctions.checkout())
    print(f"Stock after checkout: {CommerceFunctions.check_stock('item_001')}")
    
    # Verify State
    print("\n[Debug] Current Order DB State:", db.commerce_db.orders)
    
    print("\n--- Session 2 Start (Isolation Test) ---")
    # Simulate a new context/request - everything should be reset
    StateManager.init_session()
    
    print(f"User Count in new session: {UserFunctions.get_user_count()} (Should be 0)")
    print(f"Cart in new session: {db.commerce_db.cart} (Should be empty)")

if __name__ == "__main__":
    run_demo()
