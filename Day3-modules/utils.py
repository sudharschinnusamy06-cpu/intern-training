
valid_cities = ("Chennai", "Coimbatore", "Madurai", "Salem", "Trichy")

def validate_city(city):
    return city.capitalize() in valid_cities

def format_name(name):
    return name.strip().capitalize()