from contact import Contact

class PremiumContact(Contact):
    def __init__(self, name, phone, email, priority):
        super().__init__(name, phone, email)
        self.priority = priority

    def __str__(self):
        return f"[{self.priority}] " + super().__str__()