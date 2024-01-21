import requests
import pandas as pd
# program should ask user for these query parameters
# latitude, longitude
# user input validation -> sanity check

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_user_input():
    """
    This function asks user for latitude and longitude
    :returns latitude, longitude
    """
    try:
        latitude_input = float(input("Enter latitude: "))
        longitude_input = float(input("Enter longitude: "))
        return (latitude_input, longitude_input)
    except ValueError as error:
        print(f"Error: {error}")
        exit(1)

def get_url(latitude: float, longitude: float):
    """
    This function returns the url for the API call
    :param latitude: latitude of the location
    :param longitude: longitude of the location
    :returns url: url for the API call
    """
    required_params = "current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    url = f"{BASE_URL}?latitude={latitude}&longitude={longitude}&{required_params}"
    return url

def make_api_request(url: str):
    """
    This function makes the API call
    :param url: url for the API call
    :returns response_json: response from the API call
    """
    response = requests.get(url)
    status_code = response.status_code
    response_json = response.json()
    if status_code != 200:
        print(f"Error: API returned {status_code} code with mesage: {response_json}")
        exit(1)
    return response_json

def convert_response_to_csv(response_json: dict):
    """
    This function converts the response from the API call to csv format into a data.csv file
    :param response_json: response from the API call
    """
    current_data = response_json.get('current', {})
    hourly_data = response_json.get('hourly', [])

    # Create a DataFrame
    df_current = pd.DataFrame([current_data])
    df_hourly = pd.DataFrame(hourly_data)

    # Concatenate DataFrames
    df_combined = pd.concat([df_current, df_hourly], axis=1)

    # Save to CSV
    df_combined.to_csv('data.csv', index=False)



# run the program
# 54.5742, 1.2350
if __name__ == "__main__":
    latitude, longitude = get_user_input()
    url = get_url(latitude, longitude)

    # make the API call
    response_json = make_api_request(url)
    convert_response_to_csv(response_json)
