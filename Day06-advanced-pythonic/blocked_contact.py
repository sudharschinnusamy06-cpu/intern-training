from contact import Contact

class BlockedContact(Contact):
    def __str__(self):
        return f"[BLOCKED] " + super().__str__()