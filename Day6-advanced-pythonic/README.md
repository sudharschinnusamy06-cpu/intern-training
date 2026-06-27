# Day 6 — Advanced Pythonic Features

## Before (Day 5 style)
for contact in self.contacts:
    print(contact)

## After (Day 6 style)
# enumerate
for index, contact in enumerate(self.contacts, start=1):
    print(f"{index}. {contact}")

# filter + lambda
filter(lambda c: keyword.lower() in c.name.lower(), contacts)

# map + lambda
map(lambda c: c.name.upper(), contacts)

# generator
def contact_generator(contacts):
    for contact in contacts:
        yield contact

# zip
for name, phone in zip(names, phones):
    print(f"{name} --> {phone}")