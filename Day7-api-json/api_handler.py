import requests
import json
import time

API_KEY = "465e24ca89c2412b0a2f97324a114689"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[LOG] {func.__name__} done in {end - start:.4f}s")
        return result
    return wrapper

class WeatherAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.history = []

    @log_action
    def fetch_weather(self, city):
        try:
            url = f"{BASE_URL}?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print("City not found! Check spelling.")
                return None
            elif response.status_code == 401:
                print("Invalid API key!")
                return None
            else:
                print(f"Error: {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            print("No internet connection!")
            return None

    def parse_weather(self, data):
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }

    def display_weather(self, weather):
        print(f"\n=== Weather Report ===")
        print(f"City        : {weather['city']}")
        print(f"Temperature : {weather['temperature']}°C")
        print(f"Feels Like  : {weather['feels_like']}°C")
        print(f"Humidity    : {weather['humidity']}%")
        print(f"Condition   : {weather['condition']}")
        print(f"Wind Speed  : {weather['wind_speed']} m/s")

    def save_to_file(self, weather):
        self.history.append(weather)

        with open("data.json", "w") as f:
            json.dump(weather, f, indent=4)

        with open("output.txt", "a") as f:
            f.write(f"City: {weather['city']}\n")
            f.write(f"Temperature: {weather['temperature']}°C\n")
            f.write(f"Condition: {weather['condition']}\n")
            f.write("---\n")

        print("Saved to data.json ✅")
        print("Saved to output.txt ✅")