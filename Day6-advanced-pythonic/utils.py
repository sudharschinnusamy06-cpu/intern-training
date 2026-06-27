def contact_generator(contacts):
    for contact in contacts:
        yield contact

def search_by_name(contacts, keyword):
    result = filter(lambda c: keyword.lower() in c.name.lower(), contacts)
    return list(result)

def get_contact_names(contacts):
    names = map(lambda c: c.name.upper(), contacts)
    return list(names)

def display_name_phone(contacts):
    names = map(lambda c: c.name, contacts)
    phones = map(lambda c: c.phone, contacts)
    for name, phone in zip(names, phones):
        print(f"{name} --> {phone}")