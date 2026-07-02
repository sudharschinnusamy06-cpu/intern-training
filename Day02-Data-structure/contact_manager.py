contacts = []
valid_cities = ("Chennai", "Coimbatore", "Madurai", "Salem", "Trichy")
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

    if choice == "1":
        print("\n--- ADD CONTACT ---")

        name = input("Enter name: ").strip().capitalize()
        phone = input("Enter phone: ").strip()
        email = input("Enter email: ").strip().lower()
        city = input("Enter city: ").capitalize()

        if city in valid_cities:
            contact = {
                "name": name,
                "phone": phone,
                "email": email,
                "city": city
            }

            contacts.append(contact)
            cities_in_use.add(city)

            print(f"✅ '{name}' added successfully!")

        else:
            print(f"❌ Invalid city! Valid cities: {valid_cities}")

    elif choice == "2":
        print("\n--- SEARCH CONTACT ---")

        search_name = input("Enter name to search: ").capitalize()
        found = False

        for contact in contacts:
            if contact["name"] == search_name:
                print("\n✅ Contact Found!")
                print(f"Name: {contact['name']}")
                print(f"Phone: {contact['phone']}")
                print(f"Email: {contact['email']}")
                print(f"City: {contact['city']}")

                found = True
                break

        if not found:
            print(f"❌ Contact '{search_name}' not found!")

    elif choice == "3":
         print("\n--- UPDATE CONTACT ---")

         n = input("Enter name to update: ").strip().capitalize()
         found = False

         for contact in contacts:
             if contact["name"] == n:
                print(f"\nUpdating contact: {n}")
                print("1. Phone")
                print("2. Email")
                print("3. City")

                update_choice = input("What to update? ")

                if update_choice == "1":
                    contact["phone"] = input("Enter new phone: ").strip()

                elif update_choice == "2":
                    contact["email"] = input("Enter new email: ").strip().lower()

                elif update_choice == "3":
                    new_city = input("Enter new city: ").capitalize()
                    if new_city in valid_cities:       
                        contact["city"] = new_city
                        print(f"✅ City updated!")
                    else:
                        print(f"❌ Invalid city! Valid: {valid_cities}")
                        found = True
                        break

                else:
                    print("❌ Invalid choice!")

                print(f"✅ '{n}' updated successfully!")
                found = True
                break

         if not found:
            print(f"❌ Contact '{n}' not found!")

    elif choice == "4":
        print("\n--- DELETE CONTACT ---")

        n = input("Enter name to delete: ").strip().capitalize()
        found = False

        for contact in contacts:
            if contact["name"] == n:
                contacts.remove(contact)
                deleted_city = contact["city"]
                still_used = any(c["city"] == deleted_city for c in contacts)
                if not still_used:
                    cities_in_use.discard(deleted_city)

                print(f"✅ '{n}' deleted successfully!")

                found = True
                break

        if not found:
            print(f"❌ Contact '{n}' not found!")


    elif choice == "5":
        print("\n--- ALL CONTACTS ---")

        if len(contacts) == 0:
            print("❌ No contacts found!")

        else:
            for i, contact in enumerate(contacts, 1):
                print(f"\n--- Contact {i} ---")
                print(f"Name: {contact['name']}")
                print(f"Phone: {contact['phone']}")
                print(f"Email: {contact['email']}")
                print(f"City: {contact['city']}")

            filter_city = input("\nFilter by city? (press Enter to skip): ").capitalize()

            if filter_city:                                         
                filtered = [c for c in contacts if c["city"] == filter_city]
                if filtered:                                         
                    print(f"\n✅ Contacts in {filter_city}:")
                    for i, c in enumerate(filtered, 1):
                        print(f"{i}. {c['name']} - {c['phone']}")
                else:
                    print(f"❌ No contacts in {filter_city}!")
    
    
    elif choice == "6":
        print("\n--- UNIQUE CITIES ---")

        if len(cities_in_use) == 0:
            print("❌ No cities found!")

        else:
            print(f"Cities with contacts: {cities_in_use}")

    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("❌ Invalid choice!")