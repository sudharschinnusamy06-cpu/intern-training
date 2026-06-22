import random

while True:
    # Show menu
    print("\n=============================")
    print("      WELCOME TO MY APP      ")
    print("=============================")
    print("1. Calculator")
    print("2. Number Guessing Game")
    print("3. Text Analyzer")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        # Calculator
        print("\n--- CALCULATOR ---")

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")

        operation = input("Enter operation choice: ")

        if operation == "1":
            print(f"Result: {num1} + {num2} = {num1 + num2}")

        elif operation == "2":
            print(f"Result: {num1} - {num2} = {num1 - num2}")

        elif operation == "3":
            print(f"Result: {num1} * {num2} = {num1 * num2}")

        elif operation == "4":
            if num2 == 0:
                print("Error: Cannot divide by zero!")
            else:
                print(f"Result: {num1} / {num2} = {num1 / num2}")

        else:
            print("Invalid choice. Try again.")

    elif choice == "2":

        print("\n--- NUMBER GUESSING GAME ---")

        number = random.randint(1, 100)
        count = 0

        while True:
            n = int(input("Enter your guess (1-100): "))
            count += 1

            if n > number:
                print("Too High! Try again.")

            elif n < number:
                print("Too Low! Try again.")

            else:
                print(f"🎉 Correct! You got it in {count} attempts!")
                break

    elif choice == "3":

        print("\n--- TEXT ANALYZER ---")

        text = input("Enter the string: ")

        words = text.split()
        print(f"Word Count: {len(words)}")

        vowels = "aeiouAEIOU"
        vowel_count = 0

        for letter in text:
            if letter in vowels:
                vowel_count += 1

        print(f"Vowel Count: {vowel_count}")

        cleaned = text.lower().replace(" ", "")
        reversed_text = cleaned[::-1]

        if cleaned == reversed_text:
            print(f"✅ '{text}' is a Palindrome!")
        else:
            print(f"❌ '{text}' is NOT a Palindrome!")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")