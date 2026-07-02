# Day 7 — APIs, JSON & Consolidation

## What I built
A Weather CLI app that fetches real-time weather data
using OpenWeatherMap API — tying together all Week 1 skills.

## Skills used from previous days
- Day 1 — CLI menu driven app
- Day 2 — Dictionary to store weather data
- Day 3 — Separate module (api_handler.py)
- Day 4 — JSON save/load, error handling
- Day 5 — OOP (WeatherAPI class)
- Day 6 — Decorator (log_action), lambda, filter, map

## Setup
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Verify email
4. Go to "API Keys" tab
5. Copy your default API key
6. Paste it in api_handler.py → API_KEY variable

## Install dependencies
pip install requests
pip freeze > requirements.txt

## How to run
cd Day7-api-json
venv\Scripts\activate
python main.py

## Features
1. Get Current Weather — fetches live data by city name
2. View Search History — shows all searched cities
3. Search History by City — filter + lambda search
4. Show All Searched Cities — map + lambda
5. Exit

## Error Handling
- Wrong city name → "City not found! Check spelling."
- No internet → "No internet connection!"
- Wrong API key → "Invalid API key!"

## How it works
1. main.py takes city input
2. fetch_weather() builds URL + calls OpenWeatherMap API
3. parse_weather() extracts needed fields from JSON
4. display_weather() prints formatted output
5. save_to_file() saves to data.json + output.txt

## Files
- api_handler.py — WeatherAPI class, API calls, parsing
- main.py — CLI menu
- data.json — latest weather result (auto generated)
- output.txt — all search history (auto generated)
- requirements.txt — pip dependencies

## API Used
OpenWeatherMap — https://openweathermap.org
Endpoint: /data/2.5/weather
Free tier: 1000 calls/day