from contact import Contact
from premium_contact import PremiumContact
from blocked_contact import BlockedContact
from manager import ContactManager

manager = ContactManager()
manager.load_contacts()  # load saved contacts on startup

while True:
    print("\n1. Add Contact")
    print("2. List Contacts")
    print("3. Exit")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        contact = Contact(name, phone, email)
        if contact.is_valid():
            manager.add_contact(contact)
            manager.save_contacts()  # save immediately after adding
            print("Contact added!")
        else:
            print("Invalid phone or email!")
    elif choice == "2":
        manager.list_contacts()
    elif choice == "3":
        break