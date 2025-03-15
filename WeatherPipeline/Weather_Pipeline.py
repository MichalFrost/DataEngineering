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

# Transform air pollution data
def transform_pollution_data(data):
    try:
        # Choosing the first item from the list (if exists)
        air_quality_data = data["list"][0]

        transformed_data = {
            "AQI" : air_quality_data["main"].get("aqi", "N/A"),
            "CO" : air_quality_data.get("components", {}).get("co", {}),
            "NO" : air_quality_data.get("components", {}).get("no", {}),
            "NO2" : air_quality_data.get("components", {}).get("no2", {}),
            "O3" : air_quality_data.get("components", {}).get("o3", {}),
            "SO2" : air_quality_data.get("components", {}).get("so2", {}),
            "PM2_5" : air_quality_data.get("components", {}).get("pm2_5", {})
        }


        return transformed_data
    
    except requests.exceptions.RequestException as e:
        print(f"Error transforming air pollution data: {e}")
        return {}

#Validate weather data
def validate_data(data, fields):
    if not data:
        return False
    required_fields = fields
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


def save_to_csv(data, fieldnames, filename="weather_data.csv"):
    if data:
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
    
    while True:
        
        # Weather
        raw_weather_data = check_api_response(WEATHER_URL, "weather")
        results_weather = transform_weather_data(raw_weather_data)
        weather_fieldnames = ["city", "temperature", "humidity", "weather", "timestamp"]

        if validate_data(results_weather, weather_fieldnames):
            save_to_csv(results_weather, weather_fieldnames, "weather.csv")
            # analyze_weather_data()
            # plot_temperature_trends()
        else:
            print("Invalid data. Skipping save and analysis.")



         #Air pollution
        raw_pollution_data = check_api_response(POLLUTION_URL, "pollution")
        results_pollution = transform_pollution_data(raw_pollution_data)
        pollution_fieldnames = ["AQI", "CO", "NO", "NO2", "O3", "SO2", "PM2_5"]

        if validate_data(results_pollution, pollution_fieldnames):
            save_to_csv(results_pollution, pollution_fieldnames, "air_pollution.csv")
            # analyze_pollution_data()
            # plot_pollution_trends()
        else:
            print("Invalid data. Skipping save and analysis.")
        
        print(datetime.now())
        time.sleep(60) #wait 15 minutes before next request

    
    

   
