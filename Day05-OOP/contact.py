class Contact:
    def __init__(self, name, phone, email):  # ← double underscore, not single
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Contact: {self.name} | {self.email} | {self.phone}"

    def is_valid(self):
        return len(self.phone) == 10 and "@" in self.email