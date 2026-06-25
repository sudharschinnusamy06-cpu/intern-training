# utils.py

valid_cities = ("Chennai", "Coimbatore", "Madurai", "Salem", "Trichy")

def validate_city(city):
    return city.capitalize() in valid_cities

def format_name(name):
    return name.strip().capitalize()

def validate_phone(phone):
    return phone.strip().isdigit() and len(phone.strip()) == 10

def validate_email(email):
    return "@" in email and "." in email