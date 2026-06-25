# contacts.py

import json
from utils import validate_city, validate_phone, validate_email, format_name, valid_cities


def load_contacts():
    try:
        with open("contacts.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_contacts(contacts):
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)


def add_contact(contacts, cities_in_use):
    name  = format_name(input("Enter name: "))
    phone = input("Enter phone: ").strip()
    email = input("Enter email: ").strip().lower()
    city  = input("Enter city: ").strip().capitalize()

    # Validation
    if not validate_phone(phone):
        print("❌ Invalid phone! Must be 10 digits!")
        return

    if not validate_email(email):
        print("❌ Invalid email! Must contain @ and .")
        return

    if not validate_city(city):
        print(f"❌ Invalid city! Valid: {valid_cities}")
        return

    # Duplicate check
    for c in contacts:
        if c["name"] == name:
            print(f"❌ '{name}' already exists!")
            return

    contacts.append({
        "name" : name,
        "phone": phone,
        "email": email,
        "city" : city
    })
    cities_in_use.add(city)
    save_contacts(contacts)
    print(f"✅ '{name}' added successfully!")


def search_contact(contacts):
    name = format_name(input("Enter name to search: "))

    for c in contacts:
        if c["name"] == name:
            print(f"\n✅ Found!")
            print(f"Name : {c['name']}")
            print(f"Phone: {c['phone']}")
            print(f"Email: {c['email']}")
            print(f"City : {c['city']}")
            return

    print(f"❌ '{name}' not found!")


def update_contact(contacts):
    name = format_name(input("Enter name to update: "))

    for c in contacts:
        if c["name"] == name:
            print("1. Phone  2. Email  3. City")
            choice = input("What to update? ")

            if choice == "1":
                phone = input("New phone: ").strip()
                if not validate_phone(phone):
                    print("❌ Invalid phone! Must be 10 digits!")
                    return
                c["phone"] = phone

            elif choice == "2":
                email = input("New email: ").strip().lower()
                if not validate_email(email):
                    print("❌ Invalid email!")
                    return
                c["email"] = email

            elif choice == "3":
                new_city = input("New city: ").strip().capitalize()
                if not validate_city(new_city):
                    print(f"❌ Invalid city! Valid: {valid_cities}")
                    return
                c["city"] = new_city

            else:
                print("❌ Invalid choice!")
                return

            save_contacts(contacts)
            print(f"✅ '{name}' updated!")
            return

    print(f"❌ '{name}' not found!")


def delete_contact(contacts, cities_in_use):
    name = format_name(input("Enter name to delete: "))

    for c in contacts:
        if c["name"] == name:
            deleted_city = c["city"]
            contacts.remove(c)

            if not any(x["city"] == deleted_city for x in contacts):
                cities_in_use.discard(deleted_city)

            save_contacts(contacts)
            print(f"✅ '{name}' deleted!")
            return

    print(f"❌ '{name}' not found!")


def show_contacts(contacts):
    if not contacts:
        print("❌ No contacts found!")
        return

    for i, c in enumerate(contacts, 1):
        print(f"\n--- Contact {i} ---")
        print(f"Name : {c['name']}")
        print(f"Phone: {c['phone']}")
        print(f"Email: {c['email']}")
        print(f"City : {c['city']}")

    filter_city = input("\nFilter by city? (Enter to skip): ").capitalize()

    if filter_city:
        filtered = [c for c in contacts if c["city"] == filter_city]
        if filtered:
            print(f"\n✅ Contacts in {filter_city}:")
            for i, c in enumerate(filtered, 1):
                print(f"{i}. {c['name']} - {c['phone']}")
        else:
            print(f"❌ No contacts in {filter_city}!")


def show_cities(cities_in_use):
    if not cities_in_use:
        print("❌ No cities found!")
    else:
        print(f"Cities with contacts: {cities_in_use}")