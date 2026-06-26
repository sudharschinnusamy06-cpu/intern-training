import json
from contact import Contact

class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def list_contacts(self):
        for contact in self.contacts:
            print(contact)

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