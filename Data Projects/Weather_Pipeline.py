import requests
import json
import csv
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Master data section
WEATHER_API_KEY = "cbc268df9a5f067a6faaece715df6a48"  # Upewnij się, że klucz jest aktywny!
LAT = "50.0614"
LON = "19.9372"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}&units=metric"
POLLUTION_URL = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}"


# Sprawdzenie odpowiedzi API
def check_api_response(URL, label):
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"Server {label} is responding with 200 status.")
            return response.json()
        else:
            print(f"Server {label} responded with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the  {label} server: {e}")
        return None

# Transform weather data
def transform_weather_data(data):
    try:
        response = requests.get(WEATHER_URL)
        response.raise_for_status()  # Sprawdza, czy nie ma błędu HTTP
        data = response.json()

        transformed_data = {
            "city": data.get("name", "Unknown").encode().decode("unicode_escape"),
            "temperature": data.get("main", {}).get("temp", "N/A"),
            "humidity": data.get("main", {}).get("humidity", "N/A"),
            "weather": data.get("weather", [{}])[0].get("description", "N/A").encode().decode("unicode_escape"),
            "timestamp": datetime.now().isoformat()
        }
        return transformed_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

#Validate weather data
def validate_weather_data(data):
    if not data:
        return False
    required_fields = ["city", "temperature", "humidity", "weather", "timestamp"]
    for field in required_fields:
        if field not in data or data[field] == "N/A":
            print(f"Invalid data: Missing or invalid '{field}'")
            return False
    return True

#Anlyze data
def analyze_weather_data(filename="weather_data.csv"):
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            temperatures = []
            for row in reader:
                try:
                    temperatures.append(float(row["temperature"]))
                except ValueError:
                    continue
            if temperatures:
                avg_temp = sum(temperatures) / len(temperatures)
                print(f"Average temperature: {avg_temp: .2f}°C")
            else:
                print("No valid temperature data found.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Visualizing the data
def plot_temperature_trends(filename="weather_data.csv"):
    dates = []
    temperatures = []

    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    dates.append(row["timestamp"])
                    temperatures.append(float(row["temperature"]))
                except ValueError:
                    continue

        if dates and temperatures:
            plt.figure(figsize=(10,5))
            plt.plot(dates, temperatures, marker="o", linestyle="-", color = "b")
            plt.title("Temperature Trends Over Time")
            plt.xlabel("Date and Time")
            plt.ylabel("Temperature (°C)")
            plt.xticks(rotation=45)
            plt.show()
        else:
            print("No valid data to plot.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Air pollution data
def fetch_air_pollution():
    try:
        response = requests.get(POLLUTION_URL)
        response.raise_for_status()
        data = response.json()

        # Wybieramy pierwszy element z listy (jeśli istnieje)
        air_quality_data = data["list"][0]
        
        # Wskaźnik AQI
        aqi = air_quality_data["main"].get("aqi", "N/A")
        
        # Komponenty zanieczyszczeń
        components = air_quality_data.get("components", {})

        return components
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching air pollution data: {e}")
        return {}

def save_to_csv(data, filename="weather_data.csv"):
    if data:
        fieldnames = ["city", "temperature", "humidity", "weather", "timestamp"]
        try:
            with open(filename, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)
            print(f"Data saved to CSV: {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    else:
        print("No data save")


if __name__ == "__main__":
    
    # while True:
    #     raw_data = check_api_response()
    #     transformed = transform_weather_data(raw_data)
        # if validate_weather_data(transformed):
        #     save_to_csv(transformed)
        #     analyze_weather_data()
        #     plot_temperature_trends()
        # else:
        #     print("Invalid data. Skipping save and analysis.")
        # time.sleep(900) #wait 15 minutes before next request


    raw_weather_data = check_api_response(WEATHER_URL, "weather")
    raw_pollution_data = check_api_response(POLLUTION_URL, "pollution")

    # transformed = transform_weather_data(raw_weather_data)
    # pollution = fetch_air_pollution()
    # if pollution:
    #     print("Air Pollution Data:\n", json.dumps(pollution))
    # else:
    #     print("No air pollution data available.")