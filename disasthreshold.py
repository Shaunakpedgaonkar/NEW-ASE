import requests
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import MySQLdb

def read_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the configuration
config = read_config('config.json')

# Function to fetch current weather data using OpenWeatherMap API
def fetch_weather_data(latitude, longitude):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "a3e499fb0c6c56d520341619edd158cb"  # Replace with your API key
    params = {
        "lat": latitude,
        "lon": longitude,
        "exclude": "minutely",
        "units": "metric",
        "appid": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        # Re-raise the exception with a more specific message or simply propagate it
        raise requests.RequestException(f"Failed to fetch data from OpenWeatherMap: {e}")

# Function to analyze current weather data for live disaster detection
def analyze_disaster(data, hurricane_threshold, heatwave_threshold, coldwave_threshold, flooding_rainfall_threshold):
    disasters = []
    print(data)
    # Check for Hurricane
    wind_speed_km_h = data['wind']['speed'] * 3.6  # Convert m/s to km/h
    if wind_speed_km_h > hurricane_threshold:
        disasters.append('Hurricane')

    # Check for Heatwave
    if data['main']['temp'] > heatwave_threshold:
        disasters.append('Heatwave')

    # Check for Cold Wave
    if data['main']['temp'] < coldwave_threshold:
        disasters.append('Cold Wave')

    # Check for Flooding
    WarningFlag = ["thunderstorm","snow","rain"]
    if data['weather'][0]['description'] in WarningFlag:
        disasters.append(data['weather'][0]['description'])

    return disasters

# Function to fetch Met Éireann forecast data
def fetch_met_eireann_forecast(latitude, longitude):
    url = f"https://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat={latitude};long={longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        return ET.fromstring(response.content), datetime.utcnow()
    else:
        print("Failed to fetch Met Éireann data:", response.status_code)
        return None, None

# Function to predict future disasters using Met Éireann data
def predict_future_disasters(xml_data, current_date, hurricane_threshold, heatwave_threshold, coldwave_threshold, flooding_rainfall_threshold):
      future_disasters = []
      end_date = current_date + timedelta(days=config['number_of_days'])

      for time_element in xml_data.findall('.//time'):
            time_str = time_element.get('from')
            # Adjust the time string format and convert to datetime
            from_time = datetime.fromisoformat(time_str.replace('Z', '+00:00')).replace(tzinfo=None)


            if from_time > end_date:
                continue

            location_element = time_element.find('.//location')
            if location_element is not None:
                temperature_element = location_element.find('.//temperature')
                wind_speed_element = location_element.find('.//windSpeed')
                precipitation_element = location_element.find('.//precipitation')

                if temperature_element is not None:
                    temperature = float(temperature_element.get('value'))
                    if temperature > heatwave_threshold:
                        future_disasters.append('Heatwave')
                    elif temperature < coldwave_threshold:
                        future_disasters.append('Cold Wave')

                if wind_speed_element is not None:
                    wind_speed = float(wind_speed_element.get('mps')) * 3.6  # Convert m/s to km/h
                    if wind_speed > hurricane_threshold:
                        future_disasters.append('Hurricane')

                if precipitation_element is not None:
                    precipitation = float(precipitation_element.get('value'))
                    if precipitation > flooding_rainfall_threshold:
                        future_disasters.append('Flooding')

      return list(set(future_disasters)) 

def disaster_detection_system(city_coordinates):
    results = {}
    for city, city_data in city_coordinates.items():
        city_results = []
        for coordinate in city_data['coordinates']:
            name = coordinate['name']
            latitude, longitude = coordinate['latitude'], coordinate['longitude']
            thresholds = city_data['thresholds']
            current_weather = fetch_weather_data(latitude, longitude)
            current_disasters = analyze_disaster(
                current_weather, 
                thresholds['hurricane_threshold'], 
                thresholds['heatwave_threshold'], 
                thresholds['coldwave_threshold'], 
                thresholds['flooding_rainfall_threshold']
            )
            forecast_xml, current_date = fetch_met_eireann_forecast(latitude, longitude)
            future_disasters = predict_future_disasters(
                forecast_xml, 
                current_date, 
                thresholds['hurricane_threshold'], 
                thresholds['heatwave_threshold'], 
                thresholds['coldwave_threshold'], 
                thresholds['flooding_rainfall_threshold']
            ) if forecast_xml else []

            result = {
                'location': name,
                'latitude': latitude,
                'longitude': longitude,
                'current_disasters': ', '.join(current_disasters) if current_disasters else 'None',
                'future_disasters': ', '.join(future_disasters) if future_disasters else 'None',
            }
            city_results.append(result)

        results[city] = city_results
    
    # Print final results before returning
    for city, data in results.items():
        print(f"Results for {city}:")
        for location_data in data:
            print(location_data)
        print("\n")

    return results





def insert_disaster_data(all_results):
    HOST = 'disasterrecovery.clyickii62q3.eu-west-1.rds.amazonaws.com'
    USER = 'root_dev'
    PASS = 'QwertY123'
    DB = 'dr_application'
    try:
        db = MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=DB)
        cursor = db.cursor()

        for city, locations in all_results.items():
            for result in locations:
                try:
                    cursor.execute("""
                        SELECT id FROM weather
                        WHERE location = %s AND sub_location = %s;
                        """, (city, result['location']))
                    res = cursor.fetchone()
                    if res is not None:
                        # If record exists, update
                        cursor.execute("""
                            UPDATE weather
                            SET disaster_status = %s, predicted_disaster_status = %s
                            WHERE id = %s;
                            """, (result['current_disasters'], result['future_disasters'], res[0]))
                    else:
                        # If no record exists, insert new
                        cursor.execute("""
                            INSERT INTO weather (id,location, sub_location, disaster_status, predicted_disaster_status)
                            VALUES (%s, %s, %s, %s);
                            """, (city, result['location'], result['current_disasters'], result['future_disasters']))
                    
                    # Commit the transaction
                    
                except Exception as e:
                    print("Error :", e)
                    print("MySQL connection is closed")
                    db.close()
        db.commit()
        db.close()
    except Exception as e:
        print('Error: ', e)

city_coordinates = config['city_coordinates']
all_results = disaster_detection_system(city_coordinates)
insert_disaster_data(all_results)

print(insert_disaster_data)
