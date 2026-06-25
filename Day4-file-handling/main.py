# main.py

import csv
from contacts import (add_contact, search_contact, update_contact,
                      delete_contact, show_contacts, show_cities,
                      load_contacts, save_contacts)
from utils import validate_city, validate_phone, validate_email, valid_cities

contacts      = load_contacts()        # ✅ JSON-லயிருந்து load பண்றோம்
cities_in_use = set(c["city"] for c in contacts)  # ✅ existing cities set-ல போடுறோம்

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
    print("7. Import from CSV")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if   choice == "1": add_contact(contacts, cities_in_use)
    elif choice == "2": search_contact(contacts)
    elif choice == "3": update_contact(contacts)
    elif choice == "4": delete_contact(contacts, cities_in_use)
    elif choice == "5": show_contacts(contacts)
    elif choice == "6": show_cities(cities_in_use)

    elif choice == "7":
        print("\n--- CSV IMPORT ---")
        try:
            with open("contacts.csv", "r") as f:
                reader = csv.DictReader(f)
                imported = 0
                skipped  = 0

                for row in reader:
                    name  = row["name"].strip().capitalize()
                    phone = row["phone"].strip()
                    email = row["email"].strip().lower()
                    city  = row["city"].strip().capitalize()

                    # ✅ validate every row
                    if not validate_phone(phone):
                        print(f"⚠️  Skipped '{name}' — invalid phone!")
                        skipped += 1
                        continue

                    if not validate_email(email):
                        print(f"⚠️  Skipped '{name}' — invalid email!")
                        skipped += 1
                        continue

                    if not validate_city(city):
                        print(f"⚠️  Skipped '{name}' — invalid city!")
                        skipped += 1
                        continue

                    # ✅ duplicate check
                    if any(c["name"] == name for c in contacts):
                        print(f"⚠️  Skipped '{name}' — already exists!")
                        skipped += 1
                        continue

                    contacts.append({
                        "name" : name,
                        "phone": phone,
                        "email": email,
                        "city" : city
                    })
                    cities_in_use.add(city)
                    imported += 1

                save_contacts(contacts)
                print(f"\n✅ Imported: {imported} | Skipped: {skipped}")

        except FileNotFoundError:
            print("❌ contacts.csv not found!")

    elif choice == "8":
        print("Goodbye!")
        break

    else:
        print("❌ Invalid choice!")