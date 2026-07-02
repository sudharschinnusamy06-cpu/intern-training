# main.py

from contacts import (add_contact, search_contact, update_contact,
                      delete_contact, show_contacts, show_cities)

contacts      = []
cities_in_use = set()

while True:
    print("=============================")
    print("      CONTACT MANAGER        ")
    print("=============================")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Show All Contacts")
    print("6. Show Unique Cities")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if   choice == "1": add_contact(contacts, cities_in_use)
    elif choice == "2": search_contact(contacts)
    elif choice == "3": update_contact(contacts)
    elif choice == "4": delete_contact(contacts, cities_in_use)
    elif choice == "5": show_contacts(contacts)
    elif choice == "6": show_cities(cities_in_use)
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("❌ Invalid choice!")