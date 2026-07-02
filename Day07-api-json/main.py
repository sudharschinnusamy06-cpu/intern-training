from api_handler import WeatherAPI

weather_api = WeatherAPI()

while True:
    print("\n=== Weather App ===")
    print("1. Get Current Weather")
    print("2. View Search History")
    print("3. Search History by City")
    print("4. Show All Searched Cities")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        city = input("Enter city name: ")

        data = weather_api.fetch_weather(city)      # Fetch

        if data:
            weather = weather_api.parse_weather(data)   # Parse
            weather_api.display_weather(weather)        # Display
            weather_api.save_to_file(weather)           # Save

    elif choice == "2":
        for i, w in enumerate(weather_api.history, start=1):
            print(f"{i}. {w['city']} — {w['temperature']}°C — {w['condition']}")

    elif choice == "3":
        keyword = input("Enter city to search: ")

        results = list(
            filter(
                lambda w: keyword.lower() in w["city"].lower(),
                weather_api.history
            )
        )

        if results:
            for w in results:
                print(f"{w['city']} — {w['temperature']}°C")
        else:
            print("Not found in history!")

    elif choice == "4":
        cities = list(map(lambda w: w["city"], weather_api.history))
        print("Searched cities:", cities)

    elif choice == "5":
        break

    else:
        print("Invalid choice!")