import json
import time
from contact import Contact

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[LOG] {func.__name__} done in {end - start:.4f}s")
        return result
    return wrapper

class ContactManager:
    def __init__(self):
        self.contacts = []

    @log_action
    def add_contact(self, contact):
        self.contacts.append(contact)

    @log_action
    def list_contacts(self):
        for index, contact in enumerate(self.contacts, start=1):
            print(f"{index}. {contact}")
            
    def save_contacts(self, filename="contacts.json"):
        data = []
        for contact in self.contacts:
            data.append({
                "name": contact.name,
                "phone": contact.phone,
                "email": contact.email
            })
        with open(filename, "w") as f:
            json.dump(data, f)

    def load_contacts(self, filename="contacts.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            for item in data:
                contact = Contact(item["name"], item["phone"], item["email"])
                self.contacts.append(contact)
        except FileNotFoundError:
            pass