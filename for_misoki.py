"""
Sample Python file with common code issues for demo
"""

from typing import List, Dict, Optional


class UserManager:
    """Manages user data and operations - violates SRP (multiple responsibilities)"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache = {}
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user from database or cache - has dead code"""
        # Dead code - this function is never called
        def unused_helper():
            return "this is never used"
        
        # This logic is duplicated below
        if user_id in self.cache:
            return self.cache[user_id]
        
        # Inefficient: not using index
        query = "SELECT * FROM users WHERE id = " + str(user_id)
        result = self.db.execute(query)
        
        if user_id in self.cache:  # duplicate check
            return self.cache[user_id]
        
        return result
    
    def validate_email(self, email: str) -> bool:
        """Validate email - nested loops performance issue"""
        # Nested loops - O(n²)
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", 
                          "company.com", "work.org", "business.net"]
        
        for domain in allowed_domains:
            if domain in email:
                for char in email:  # unnecessary nested loop
                    if char == "@":
                        return True
        return False
    
    def process_users_batch(self, user_ids: List[int]) -> List[Dict]:
        """Process multiple users - nested loops for same operation"""
        results = []
        
        # Nested loops - should use set or dict
        for user_id in user_ids:
            for i in range(1):  # unnecessary loop
                user = self.get_user(user_id)
                if user:
                    for j in range(1):  # another unnecessary loop
                        results.append(user)
        
        return results
    
    def generate_report(self, users: List[Dict]) -> str:
        """Generate report - violates OCP (hard to extend)"""
        report = "User Report\n"
        
        # Long method with many branches - violates SRP
        for user in users:
            if user.get("type") == "admin":
                if user.get("permissions") == "full":
                    report += f"Admin: {user['name']} - Full Access\n"
                elif user.get("permissions") == "limited":
                    report += f"Admin: {user['name']} - Limited Access\n"
                else:
                    report += f"Admin: {user['name']} - Unknown\n"
            elif user.get("type") == "regular":
                if user.get("active") == True:
                    report += f"User: {user['name']} - Active\n"
                else:
                    report += f"User: {user['name']} - Inactive\n"
            elif user.get("type") == "guest":
                report += f"Guest: {user['name']} - Limited\n"
            else:
                report += f"Unknown: {user.get('name', 'N/A')}\n"
        
        return report
    
    def save_to_file(self, data: str, filename: str):
        """Save data - potential security issue (no sanitization)"""
        # Security: direct file write without sanitization
        with open(filename, "w") as f:
            f.write(data)
    
    def send_notification(self, user_id: int, message: str):
        """Send notification - no error handling"""
        # No try-catch for network/file operations
        email = self.get_user(user_id).get("email")
        # Would fail silently if email is None
        self.send_email(email, message)
    
    def send_email(self, to: str, message: str):
        """Send email - empty method"""
        pass  # TODO: implement
    
    def calculate_stats(self, numbers: List[int]) -> Dict:
        """Calculate statistics - deep copy unnecessary"""
        import copy
        
        # Unnecessary deep copy
        numbers_copy = copy.deepcopy(numbers)
        
        total = 0
        for num in numbers_copy:
            total += num
        
        return {
            "total": total,
            "count": len(numbers)
        }


# Global state - bad practice
global_user_cache = {}


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Get user - uses global state"""
    # Uses global variable
    if user_id in global_user_cache:
        return global_user_cache[user_id]
    return None


def process_data(data: List[str]) -> List[str]:
    """Process data - uses list comprehension incorrectly"""
    # Should use generator for large data
    return [x.strip() for x in data if x]


class DatabaseConnection:
    """Database connection - singleton pattern but not thread-safe"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        self.connection = "mock_connection"
    
    def execute(self, query: str):
        return {}


# Magic numbers - should be constants
def calculate_price(quantity: int, price: float) -> float:
    # Magic number 0.1 should be TAX_RATE constant
    tax = price * 0.1
    # Magic number 5 should be DISCOUNT_THRESHOLD
    if quantity > 5:
        return (price * quantity) * 0.95
    return price * quantity + tax


# TODO: This function needs to be implemented
def pending_implementation():
    """This is a placeholder"""
    raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    db = DatabaseConnection()
    manager = UserManager(db)
    
    users = [
        {"name": "Alice", "type": "admin", "permissions": "full"},
        {"name": "Bob", "type": "regular", "active": True},
    ]
    
    print(manager.generate_report(users))
