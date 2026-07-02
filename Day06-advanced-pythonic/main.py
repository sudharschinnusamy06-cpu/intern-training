from contact import Contact
from premium_contact import PremiumContact
from blocked_contact import BlockedContact
from manager import ContactManager
from utils import contact_generator , search_by_name, get_contact_names,display_name_phone

manager = ContactManager()
manager.load_contacts()

while True:
    print("\n1. Add Contact")
    print("2. List Contacts")
    print("3. Exit")
    print("4. Stream Contacts (Generator)")
    print("5. Search Contact")
    print("6. Show All Names")
    print("7. Show Name & Phone")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        contact = Contact(name, phone, email)
        if contact.is_valid():
            manager.add_contact(contact)
            manager.save_contacts()
            print("Contact added!")
        else:
            print("Invalid phone or email!")
    elif choice == "2":
        manager.list_contacts()

    elif choice == "3":
        break

    elif choice == "4":
        print("\n--- Streaming contacts (generator) ---")
        for contact in contact_generator(manager.contacts):
            print(contact)


    elif choice == "5":
        keyword = input("Enter name to search: ")
        results = search_by_name(manager.contacts, keyword)  # what two args?
        if results:
            for contact in results:
              print(contact)
        else:
            print("No contacts found!")

    elif choice == "6":
        names = get_contact_names(manager.contacts)  # what goes here?
        for name in names:
            print(name)

    elif choice == "7":
        display_name_phone(manager.contacts)