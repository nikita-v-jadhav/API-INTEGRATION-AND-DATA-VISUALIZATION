import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# -----------------------------
# 1. API Configuration
# -----------------------------
API_KEY = "103f89c9326f115a0170bb34ce350e3b"
CITY = "Solapur"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# -----------------------------
# 2. Fetch Data
# -----------------------------
params = {
    "q": CITY,
    "appid": API_KEY,
    "units": "metric"   # Celsius
}

response = requests.get(BASE_URL, params=params)
data = response.json()

# Debug: Print data to check API response
print("API Response:", data)

# -----------------------------
# 3. Parse Data into DataFrame (with error handling)
# -----------------------------
if "list" not in data:
    print(f"Error: {data.get('message', 'No forecast data found.')}")
    exit()

forecast_list = data["list"]

records = []
for entry in forecast_list:
    dt = datetime.datetime.fromtimestamp(entry["dt"])
    temp = entry["main"]["temp"]
    feels_like = entry["main"]["feels_like"]
    humidity = entry["main"]["humidity"]
    wind = entry["wind"]["speed"]

    records.append([dt, temp, feels_like, humidity, wind])

df = pd.DataFrame(records, columns=["datetime", "temp", "feels_like", "humidity", "wind"])

print("\nWeather Data Sample:")
print(df.head())  # check the structure

# -----------------------------
# 4. Visualization Dashboard
# -----------------------------
plt.figure(figsize=(12, 6))
sns.lineplot(x="datetime", y="temp", data=df, marker="o", label="Temperature (°C)")
sns.lineplot(x="datetime", y="feels_like", data=df, marker="o", label="Feels Like (°C)")
plt.xticks(rotation=45)
plt.title(f"5-Day Temperature Forecast for {CITY}")
plt.xlabel("Date/Time")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Humidity & Wind Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df["humidity"], bins=10, ax=axes[0], kde=True, color="blue")
axes[0].set_title("Humidity Distribution")
axes[0].set_xlabel("Humidity (%)")

sns.histplot(df["wind"], bins=10, ax=axes[1], kde=True, color="green")
axes[1].set_title("Wind Speed Distribution")
axes[1].set_xlabel("Wind Speed (m/s)")

plt.tight_layout()
plt.show()