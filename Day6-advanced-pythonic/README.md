# Day 6 — Advanced Pythonic Features

## Before (Day 5 style)
def list_contacts(self):
    for contact in self.contacts:
        print(contact)

## After (Day 6 style)
# Using generator
for contact in contact_generator(manager.contacts):
    print(contact)

# Using filter + lambda
results = filter(lambda c: keyword.lower() in c.name.lower(), contacts)

# Using map + lambda
names = map(lambda c: c.name.upper(), contacts)